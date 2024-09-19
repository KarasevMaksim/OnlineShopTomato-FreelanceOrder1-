"""add sub sections

Revision ID: 1062278828cb
Revises: 6139711169b2
Create Date: 2024-09-19 22:30:12.084050

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1062278828cb'
down_revision = '6139711169b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sub_section',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sub_section_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('product_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'sub_section', ['sub_section_id'], ['id'], ondelete='CASCADE')
        batch_op.drop_column('section_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('section_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('product_ibfk_1', 'section', ['section_id'], ['id'], ondelete='CASCADE')
        batch_op.drop_column('sub_section_id')

    op.drop_table('sub_section')
    # ### end Alembic commands ###
