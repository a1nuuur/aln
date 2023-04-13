"""Changed rating type to float

Revision ID: ab85182e194c
Revises: 3e190559676e
Create Date: 2023-04-12 17:50:53.425521

"""
from alembic import op
import sqlalchemy as sa


revision = 'ab85182e194c'
down_revision = '3e190559676e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product_tags', 'parent_tag_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('products', 'rating',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'rating',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('product_tags', 'parent_tag_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###
