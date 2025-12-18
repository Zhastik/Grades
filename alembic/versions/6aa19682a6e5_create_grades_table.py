"""create grades table

Revision ID: 6aa19682a6e5
Revises: 
Create Date: 2025-12-18 04:24:56.442931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6aa19682a6e5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id BIGSERIAL PRIMARY KEY,
        grade_date DATE NOT NULL,
        group_number TEXT NOT NULL,
        full_name TEXT NOT NULL,
        grade SMALLINT NOT NULL,
        CONSTRAINT grade_range_chk CHECK (grade IN (2,3,4,5))
    );

    CREATE INDEX IF NOT EXISTS ix_grades_full_name ON grades(full_name);
    CREATE INDEX IF NOT EXISTS ix_grades_grade_full_name ON grades(grade, full_name);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS grades;
    """)
    pass
