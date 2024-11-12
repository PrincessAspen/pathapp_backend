"""Modified some more tables for easier reference.

Revision ID: ead21e6ade9b
Revises: 298322ec3e5c
Create Date: 2024-11-08 13:32:19.200995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'ead21e6ade9b'
down_revision: Union[str, None] = '298322ec3e5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('alignments', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('alignments', 'abbreviation',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_index(op.f('ix_caster_types_type_id'), 'caster_types', ['type_id'], unique=False)
    op.alter_column('characters', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('class_abilities', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('class_abilities', 'level_requirement',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('class_abilities', 'numeric_modifier',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('class_abilities', 'category',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('equipment', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('equipment', 'weight',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('feats', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('languages', 'learned_by_races',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True)
    op.add_column('skills', sa.Column('modifying_stat_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'skills', 'stats', ['modifying_stat_id'], ['id'])
    op.drop_column('skills', 'modifying_stat')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('skills', sa.Column('modifying_stat', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'skills', type_='foreignkey')
    op.drop_column('skills', 'modifying_stat_id')
    op.alter_column('languages', 'learned_by_races',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('feats', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('equipment', 'weight',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('equipment', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('class_abilities', 'category',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('class_abilities', 'numeric_modifier',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('class_abilities', 'level_requirement',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('class_abilities', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('characters', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_caster_types_type_id'), table_name='caster_types')
    op.alter_column('alignments', 'abbreviation',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('alignments', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    