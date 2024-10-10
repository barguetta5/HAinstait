"""initial migration

Revision ID: 9ef2317d25ae
Revises: 
Create Date: 2024-10-07 12:23:59.945309

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ef2317d25ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create chat_history table
    op.create_table(
        'chat_history',
        sa.Column('user_id', sa.String(length=200), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('user_id')
    )

def downgrade() -> None:
    # Drop chat_history table
    op.drop_table('chat_history')
