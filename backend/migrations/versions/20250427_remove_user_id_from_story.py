"""Remove user_id from story table

Revision ID: 20250427_remove_user_id_from_story
Revises: 237d19008a5f
Create Date: 2025-04-27
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('story', schema=None) as batch_op:
        batch_op.drop_column('user_id')

def downgrade():
    with op.batch_alter_table('story', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_story_user_id_user', 'user', ['user_id'], ['id'])
