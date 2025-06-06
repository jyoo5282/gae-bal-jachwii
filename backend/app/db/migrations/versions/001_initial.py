"""initial

Revision ID: 001
Revises: 
Create Date: 2024-03-26 16:35:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 뉴스 소스 테이블 생성
    op.create_table(
        'news_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # 뉴스 기사 테이블 생성
    op.create_table(
        'news_articles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['source_id'], ['news_sources.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('url')
    )

    # 인덱스 생성
    op.create_index(op.f('ix_news_articles_published_at'), 'news_articles', ['published_at'], unique=False)
    op.create_index(op.f('ix_news_articles_source_id'), 'news_articles', ['source_id'], unique=False)
    op.create_index(op.f('ix_news_sources_name'), 'news_sources', ['name'], unique=True)

def downgrade() -> None:
    # 인덱스 삭제
    op.drop_index(op.f('ix_news_sources_name'), table_name='news_sources')
    op.drop_index(op.f('ix_news_articles_source_id'), table_name='news_articles')
    op.drop_index(op.f('ix_news_articles_published_at'), table_name='news_articles')
    
    # 테이블 삭제
    op.drop_table('news_articles')
    op.drop_table('news_sources') 