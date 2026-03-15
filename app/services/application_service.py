from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models.application import Application, ApplicationHistory, ApplicationStatus
from app.models.job import Job, JobStatus
from app.models.cv import CV
from app.api.v1.schemas.application_schemas import ApplicationCreate, ApplicationStatusUpdate


class ApplicationService:

    # ── Nộp CV vào vị trí ────────────────────────────────────────────────────
    @staticmethod
    async def apply(
        db: AsyncSession,
        data: ApplicationCreate,
        applicant_id: int,
    ) -> Application:
        # Kiểm tra job tồn tại và đang mở
        job = (await db.execute(
            select(Job).where(Job.Id == data.job_id)
        )).scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=404, detail="Không tìm thấy job")
        if job.Status != JobStatus.OPEN:
            raise HTTPException(status_code=400, detail="Job này không còn nhận hồ sơ")

        # Kiểm tra CV thuộc về user
        cv = (await db.execute(
            select(CV).where(CV.Id == data.cv_id)
        )).scalar_one_or_none()
        if not cv:
            raise HTTPException(status_code=404, detail="Không tìm thấy CV")
        if cv.UserId != applicant_id:
            raise HTTPException(status_code=403, detail="CV không thuộc về bạn")

        # Kiểm tra đã nộp chưa
        existing = (await db.execute(
            select(Application).where(
                Application.JobId == data.job_id,
                Application.ApplicantId == applicant_id,
            )
        )).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="Bạn đã nộp đơn vào vị trí này rồi")

        app = Application(
            JobId=data.job_id,
            CVId=data.cv_id,
            ApplicantId=applicant_id,
            CoverLetter=data.cover_letter,
            Status=ApplicationStatus.APPLIED,
        )
        db.add(app)
        await db.flush()

        # Ghi lịch sử
        db.add(ApplicationHistory(
            ApplicationId=app.Id,
            Status=ApplicationStatus.APPLIED,
            Note="Nộp đơn ứng tuyển",
            ChangedById=applicant_id,
        ))

        await db.commit()
        return await ApplicationService._get_application_detail(db, app.Id)

    # ── Lấy lịch sử ứng tuyển của user ───────────────────────────────────────
    @staticmethod
    async def get_my_applications(
        db: AsyncSession,
        applicant_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Application], int]:
        query = (
            select(Application)
            .where(Application.ApplicantId == applicant_id)
            .options(selectinload(Application.job))
        )
        total = (await db.execute(
            select(func.count()).select_from(query.subquery())
        )).scalar_one()

        result = await db.execute(
            query.offset(skip).limit(limit).order_by(Application.AppliedAt.desc())
        )
        return result.scalars().all(), total

    # ── Lấy chi tiết application ──────────────────────────────────────────────
    @staticmethod
    async def get_application(db: AsyncSession, application_id: int) -> Application:
        return await ApplicationService._get_application_detail(db, application_id)

    # ── Cập nhật trạng thái (HR/Admin) ───────────────────────────────────────
    @staticmethod
    async def update_status(
        db: AsyncSession,
        application_id: int,
        data: ApplicationStatusUpdate,
        changed_by_id: int,
    ) -> Application:
        app = await ApplicationService._get_or_404(db, application_id)

        old_status = app.Status
        new_status = ApplicationStatus(data.status)

        if old_status == new_status:
            raise HTTPException(status_code=400, detail="Trạng thái không thay đổi")

        app.Status = new_status

        # Ghi lịch sử
        db.add(ApplicationHistory(
            ApplicationId=application_id,
            Status=new_status,
            Note=data.note,
            ChangedById=changed_by_id,
        ))

        await db.commit()
        return await ApplicationService._get_application_detail(db, application_id)

    # ── Lấy lịch sử của 1 application ────────────────────────────────────────
    @staticmethod
    async def get_history(
        db: AsyncSession, application_id: int
    ) -> List[ApplicationHistory]:
        await ApplicationService._get_or_404(db, application_id)
        result = await db.execute(
            select(ApplicationHistory)
            .where(ApplicationHistory.ApplicationId == application_id)
            .options(selectinload(ApplicationHistory.changed_by_user))
            .order_by(ApplicationHistory.ChangedAt)
        )
        return result.scalars().all()

    # ── Helpers ───────────────────────────────────────────────────────────────
    @staticmethod
    async def _get_or_404(db: AsyncSession, application_id: int) -> Application:
        app = (await db.execute(
            select(Application).where(Application.Id == application_id)
        )).scalar_one_or_none()
        if not app:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn ứng tuyển")
        return app

    @staticmethod
    async def _get_application_detail(db: AsyncSession, application_id: int) -> Application:
        result = await db.execute(
            select(Application)
            .where(Application.Id == application_id)
            .options(
                selectinload(Application.job),
                selectinload(Application.applicant),
                selectinload(Application.history).selectinload(ApplicationHistory.changed_by_user),
            )
        )
        app = result.scalar_one_or_none()
        if not app:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn ứng tuyển")
        return app
