from .response import ResponseSchema

from .cv import (
    CVBase,
    CVCreate,
    CVUpdate,
    CVResponse
)


from .job import (
    JobBase,
    JobCreate,
    JobUpdate,
    JobResponse
)

from .skill import (
    SkillBase,
    SkillCreate,
    SkillUpdate,
    SkillResponse
)

from .education import (
    EducationBase,
    EducationCreate,
    EducationUpdate,
    EducationResponse
)
from .experience import (
    ExperienceBase,
    ExperienceCreate,
    ExperienceUpdate,
    ExperienceResponse
)

from .cv_embedding import (
    CVEmbeddingBase,
    CVEmbeddingCreate,
    CVEmbeddingResponse
)
from .job_embedding import (
    JobEmbeddingBase,
    JobEmbeddingCreate,
    JobEmbeddingUpdate,
    JobEmbeddingResponse
)

from .cv_skill import (
    CVSkillBase,
    CVSkillCreate,
    CVSkillUpdate,
    CVSkillResponse
)
from .job_skill import (
    JobSkillBase,
    JobSkillCreate,
    JobSkillUpdate,
    JobSkillResponse
)

from .screen_batch import (
    ScreeningBatchBase,
    ScreeningBatchCreate,
    ScreeningBatchUpdate,
    ScreeningBatchResponse
)

from .match_result import (
    MatchResultBase,
    MatchResultCreate,
    MatchResultUpdate,
    MatchResultResponse
)