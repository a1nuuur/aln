"""Added tsvector to tags

Revision ID: 7189e29bcf08
Revises: 03958e791158
Create Date: 2023-04-22 17:15:35.316270

"""
from alembic import op
import sqlalchemy as sa

from app.db.repositories.helpers import TSVector


revision = '7189e29bcf08'
down_revision = '03958e791158'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_tags', sa.Column('ts_vector', TSVector(), sa.Computed("to_tsvector('russian', name || ' ' || short_description)", persisted=True), nullable=True))
    op.alter_column('product_tags', 'name',
               existing_type=sa.VARCHAR(length=72),
               nullable=False)
    op.create_index('ix_tag___ts_vector__', 'product_tags', ['ts_vector'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_tag___ts_vector__', table_name='product_tags', postgresql_using='gin')
    op.alter_column('product_tags', 'name',
               existing_type=sa.VARCHAR(length=72),
               nullable=True)
    op.drop_column('product_tags', 'ts_vector')
    # ### end Alembic commands ###