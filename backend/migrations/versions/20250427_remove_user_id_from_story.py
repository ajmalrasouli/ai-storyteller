# backend/migrations/versions/20250427_remove_user_id_from_story.py

"""Remove user_id from story table

Revision ID: 20250427_remove_user_id_from_story # <-- This is just a description now
Revises: 237d19008a5f
Create Date: 2025-04-27 # <-- This is just a description now
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250427_remove_user_id_from_story' # <--- ADD THIS LINE (Use the filename part or generate a new hex ID)
down_revision = '237d19008a5f'               # <--- Ensure this points to the previous migration ID
branch_labels = None
depends_on = None


def upgrade():
    # Ensure schema is None for default schema operations
    with op.batch_alter_table('story', schema=None) as batch_op:
        # Use the actual column name if different
        batch_op.drop_column('user_id')

def downgrade():
     # Ensure schema is None for default schema operations
    with op.batch_alter_table('story', schema=None) as batch_op:
        # Ensure column type and foreign key match the original state
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        # Optional: Recreate foreign key if it existed. Adjust names/columns if needed.
        # batch_op.create_foreign_key('fk_story_user_id_user', 'user', ['user_id'], ['id'])