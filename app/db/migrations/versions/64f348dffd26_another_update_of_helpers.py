"""Another update of helpers

Revision ID: 64f348dffd26
Revises: 3b181c524e82
Create Date: 2023-03-04 22:10:42.913020

"""
from alembic import op
import sqlalchemy as sa


revision = '64f348dffd26'
down_revision = '3b181c524e82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_lists_to_products_id', table_name='lists_to_products')
    op.drop_column('lists_to_products', 'id')
    op.drop_index('ix_user_to_groups_id', table_name='user_to_groups')
    op.drop_column('user_to_groups', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_to_groups', sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False))
    op.create_index('ix_user_to_groups_id', 'user_to_groups', ['id'], unique=False)
    op.add_column('lists_to_products', sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False))
    op.create_index('ix_lists_to_products_id', 'lists_to_products', ['id'], unique=False)
    # ### end Alembic commands ###
