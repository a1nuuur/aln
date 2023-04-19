"""My god

Revision ID: edcccf9cc464
Revises: e3304d236843
Create Date: 2023-04-13 00:38:09.402410

"""
from alembic import op
import sqlalchemy as sa


revision = 'edcccf9cc464'
down_revision = 'e3304d236843'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_tags_parent_tag_id_fkey', 'product_tags', type_='foreignkey')
    op.drop_column('product_tags', 'parent_tag_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_tags', sa.Column('parent_tag_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.create_foreign_key('product_tags_parent_tag_id_fkey', 'product_tags', 'product_tags', ['parent_tag_id'], ['id'])
    # ### end Alembic commands ###