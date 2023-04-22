"""Added tsvector to products

Revision ID: 03958e791158
Revises: 2895228a1bad
Create Date: 2023-04-22 16:49:37.349159

"""
from alembic import op
import sqlalchemy as sa
from app.db.repositories.helpers import TSVector



revision = '03958e791158'
down_revision = '2895228a1bad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('ts_vector', TSVector(), sa.Computed("to_tsvector('russian', name || ' ' || slug || ' ' || description)", persisted=True), nullable=True))
    op.create_index('ix_video___ts_vector__', 'products', ['ts_vector'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_video___ts_vector__', table_name='products', postgresql_using='gin')
    op.drop_column('products', 'ts_vector')
    # ### end Alembic commands ###
