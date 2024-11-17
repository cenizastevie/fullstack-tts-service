"""Initial migration

Revision ID: b70be3d2bf8e
Revises: 
Create Date: 2024-11-17 10:52:43.730387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b70be3d2bf8e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image_metadata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('patient_id', sa.String(length=50), nullable=True),
    sa.Column('source_id', sa.String(length=50), nullable=True),
    sa.Column('diagnosis', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_metadata_filename'), 'image_metadata', ['filename'], unique=False)
    op.create_index(op.f('ix_image_metadata_id'), 'image_metadata', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_image_metadata_id'), table_name='image_metadata')
    op.drop_index(op.f('ix_image_metadata_filename'), table_name='image_metadata')
    op.drop_table('image_metadata')
    # ### end Alembic commands ###