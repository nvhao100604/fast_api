"""fix_userrole_enum_lowercase_add_admin

Revision ID: 84b1a759bbaa
Revises: 34b6ca55ae8d
Create Date: 2026-02-23 20:07:29.673593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = '84b1a759bbaa'
down_revision: Union[str, Sequence[str], None] = '34b6ca55ae8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Đổi tên enum cũ
    op.execute("ALTER TYPE userrole RENAME TO userrole_old")
    
    # Tạo enum mới chữ thường + có admin
    op.execute("CREATE TYPE userrole AS ENUM ('applicant', 'hr', 'admin')")
    
    # Convert dữ liệu cũ sang enum mới
    op.execute("""
        ALTER TABLE users 
        ALTER COLUMN role TYPE userrole 
        USING (lower(role::text)::userrole)
    """)
    
    # Xóa enum cũ
    op.execute("DROP TYPE userrole_old")


def downgrade() -> None:
    # Rollback về enum cũ nếu cần
    op.execute("ALTER TYPE userrole RENAME TO userrole_new")
    op.execute("CREATE TYPE userrole AS ENUM ('HR', 'APPLICANT')")
    op.execute("""
        ALTER TABLE users 
        ALTER COLUMN role TYPE userrole 
        USING (upper(role::text)::userrole)
    """)
    op.execute("DROP TYPE userrole_new")