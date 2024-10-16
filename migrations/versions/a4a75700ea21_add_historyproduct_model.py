"""add HistoryProduct model

Revision ID: a4a75700ea21
Revises: 72011cecc65e
Create Date: 2024-10-07 21:52:44.936426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4a75700ea21'
down_revision = '72011cecc65e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history_product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_user', sa.String(length=300), nullable=False),
    sa.Column('email_user', sa.String(length=300), nullable=False),
    sa.Column('phone_user', sa.String(length=300), nullable=False),
    sa.Column('name_product', sa.String(length=300), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('img_link', sa.String(length=100), nullable=False),
    sa.Column('section', sa.String(length=300), nullable=False),
    sa.Column('sub_section', sa.String(length=300), nullable=False),
    sa.Column('link_to_product', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('history_product')
    # ### end Alembic commands ###
