"""Add last_visit column

Revision ID: c28818ff36fa
Revises: be890ecfbb2b
Create Date: 2025-04-11 19:12:47.811590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c28818ff36fa'
down_revision: Union[str, None] = 'be890ecfbb2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animals', sa.Column('last_visit', sa.DateTime(timezone=True), nullable=True, comment='Data ostatniej wizyty zwierzęcia u weterynarza'))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('animals', 'last_visit')
    # ### end Alembic commands ###
