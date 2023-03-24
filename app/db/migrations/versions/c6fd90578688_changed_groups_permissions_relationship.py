"""Changed groups permissions relationship

Revision ID: c6fd90578688
Revises: 84a0107276ed
Create Date: 2023-03-08 13:30:58.785518

"""
from alembic import op
import sqlalchemy as sa


revision = 'c6fd90578688'
down_revision = '84a0107276ed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions_to_groups',
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.Column('permission_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.PrimaryKeyConstraint('group_id', 'permission_id')
    )
    op.drop_constraint('groups_permission_id_fkey', 'groups', type_='foreignkey')
    op.drop_column('groups', 'permission_id')
    op.alter_column('money_transactions', 'money_change',
               existing_type=sa.NUMERIC(),
               nullable=False)
    op.alter_column('money_transactions', 'approved',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('money_transactions', 'wallet_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('money_transactions', 'wallet_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('money_transactions', 'approved',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('money_transactions', 'money_change',
               existing_type=sa.NUMERIC(),
               nullable=True)
    op.add_column('groups', sa.Column('permission_id', sa.BIGINT(), autoincrement=False, nullable=False))
    op.create_foreign_key('groups_permission_id_fkey', 'groups', 'permissions', ['permission_id'], ['id'], ondelete='CASCADE')
    op.drop_table('permissions_to_groups')
    # ### end Alembic commands ###
