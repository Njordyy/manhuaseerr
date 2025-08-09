from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('series',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('source', sa.String, index=True),
        sa.Column('remote_id', sa.String, index=True),
        sa.Column('title', sa.String),
        sa.Column('cover', sa.String, nullable=True)
    )

def downgrade():
    op.drop_table('series')
