"""Changed permission name colum type to PK

Revision ID: a4e89935ce3d
Revises: ebe41d7846a8
Create Date: 2023-03-03 20:57:39.156130

"""
from alembic import op
import sqlalchemy as sa


revision = 'a4e89935ce3d'
down_revision = 'ebe41d7846a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('permissions', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('permissions', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
