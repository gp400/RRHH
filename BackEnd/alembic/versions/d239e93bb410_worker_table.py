"""Worker table

Revision ID: d239e93bb410
Revises: 14cc4fcf943e
Create Date: 2026-02-14 19:19:11.547774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd239e93bb410'
down_revision: Union[str, Sequence[str], None] = '14cc4fcf943e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add new FK column to Experience
    with op.batch_alter_table('Experience', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_experience_worker_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_experience_worker_id_worker',
            'Worker',
            ['fk_experience_worker_id'],
            ['id']
        )

    # Update Worker table — add new FK columns and drop old ones
    with op.batch_alter_table('Worker', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_worker_position_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('fk_worker_department_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('fk_worker_recommended_id', sa.Integer(), nullable=True))

        # Create new FKs with explicit names
        batch_op.create_foreign_key(
            'fk_worker_recommended_id_worker',
            'Worker',
            ['fk_worker_recommended_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_worker_position_id_positions',
            'Positions',
            ['fk_worker_position_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_worker_department_id_department',
            'Department',
            ['fk_worker_department_id'],
            ['id']
        )

        # Drop old FK columns
        batch_op.drop_column('recommended_id')
        batch_op.drop_column('department_id')
        batch_op.drop_column('position_id')

    # Update WorkerCompetence — drop old columns and add FKs
    with op.batch_alter_table('WorkerCompetence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_workercompetence_worker_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('fk_workercompetence_competence_id', sa.Integer(), nullable=True))

        batch_op.create_foreign_key(
            'fk_workercompetence_worker_id_worker',
            'Worker',
            ['fk_workercompetence_worker_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_workercompetence_competence_id_competence',
            'Competence',
            ['fk_workercompetence_competence_id'],
            ['id']
        )

        batch_op.drop_column('worker_id')
        batch_op.drop_column('competence_id')

    # Update WorkerTraining — drop old columns and add FKs
    with op.batch_alter_table('WorkerTraining', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_workertraining_worker_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('fk_workertraining_competence_id', sa.Integer(), nullable=True))

        batch_op.create_foreign_key(
            'fk_workertraining_worker_id_worker',
            'Worker',
            ['fk_workertraining_worker_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_workertraining_competence_id_training',
            'Training',
            ['fk_workertraining_competence_id'],
            ['id']
        )

        batch_op.drop_column('worker_id')
        batch_op.drop_column('training_id')


def downgrade() -> None:
    """Downgrade schema."""

    # Reverse WorkerTraining
    with op.batch_alter_table('WorkerTraining', schema=None) as batch_op:
        batch_op.add_column(sa.Column('training_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('worker_id', sa.INTEGER(), nullable=True))

        batch_op.create_foreign_key(
            'fk_workertraining_worker_id_worker',
            'Worker',
            ['worker_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_workertraining_competence_id_training',
            'Training',
            ['training_id'],
            ['id']
        )

        batch_op.drop_column('fk_workertraining_competence_id')
        batch_op.drop_column('fk_workertraining_worker_id')

    # Reverse WorkerCompetence
    with op.batch_alter_table('WorkerCompetence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('competence_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('worker_id', sa.INTEGER(), nullable=True))

        batch_op.create_foreign_key(
            'fk_workercompetence_worker_id_worker',
            'Worker',
            ['worker_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_workercompetence_competence_id_competence',
            'Competence',
            ['competence_id'],
            ['id']
        )

        batch_op.drop_column('fk_workercompetence_competence_id')
        batch_op.drop_column('fk_workercompetence_worker_id')

    # Reverse Worker
    with op.batch_alter_table('Worker', schema=None) as batch_op:
        batch_op.add_column(sa.Column('position_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('department_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('recommended_id', sa.INTEGER(), nullable=True))

        batch_op.create_foreign_key(
            'fk_worker_recommended_id_worker',
            'Worker',
            ['recommended_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_worker_department_id_department',
            'Department',
            ['department_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_worker_position_id_positions',
            'Positions',
            ['position_id'],
            ['id']
        )

        batch_op.drop_column('fk_worker_recommended_id')
        batch_op.drop_column('fk_worker_department_id')
        batch_op.drop_column('fk_worker_position_id')

    # Reverse Experience
    with op.batch_alter_table('Experience', schema=None) as batch_op:
        batch_op.drop_constraint('fk_experience_worker_id_worker', type_='foreignkey')
        batch_op.drop_column('fk_experience_worker_id')
