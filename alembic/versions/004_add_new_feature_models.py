"""add new feature models

Revision ID: 004
Revises: 003
Create Date: 2025-11-10 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to users table
    op.add_column('users', sa.Column('business_stage', sa.String(), nullable=True))
    op.add_column('users', sa.Column('sector', sa.String(), nullable=True))
    op.add_column('users', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('profile_image', sa.String(), nullable=True))
    op.add_column('users', sa.Column('language_preference', sa.String(), server_default='en', nullable=False))
    
    # Create programs table
    op.create_table(
        'programs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('program_type', sa.String(), nullable=False),
        sa.Column('stage', sa.String(), nullable=True),
        sa.Column('sector', sa.String(), nullable=True),
        sa.Column('eligibility_criteria', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('cost', sa.String(), nullable=True),
        sa.Column('duration', sa.String(), nullable=True),
        sa.Column('application_deadline', sa.Date(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('website', sa.Text(), nullable=True),
        sa.Column('application_link', sa.Text(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_programs_id'), 'programs', ['id'], unique=False)
    op.create_index(op.f('ix_programs_title'), 'programs', ['title'], unique=False)
    
    # Create mentors table
    op.create_table(
        'mentors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('expertise_tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sector_focus', sa.String(), nullable=True),
        sa.Column('stage_focus', sa.String(), nullable=True),
        sa.Column('profile_image', sa.String(), nullable=True),
        sa.Column('office_hours', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_approved', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mentors_id'), 'mentors', ['id'], unique=False)
    op.create_index(op.f('ix_mentors_full_name'), 'mentors', ['full_name'], unique=False)
    
    # Create grants table
    op.create_table(
        'grants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('grant_type', sa.String(), nullable=False),
        sa.Column('amount_min', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('amount_max', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('eligibility_criteria', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sector', sa.String(), nullable=True),
        sa.Column('application_deadline', sa.Date(), nullable=True),
        sa.Column('application_link', sa.Text(), nullable=True),
        sa.Column('requirements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_grants_id'), 'grants', ['id'], unique=False)
    op.create_index(op.f('ix_grants_title'), 'grants', ['title'], unique=False)
    op.create_index(op.f('ix_grants_application_deadline'), 'grants', ['application_deadline'], unique=False)
    
    # Create resources table
    op.create_table(
        'resources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('resource_type', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('file_url', sa.Text(), nullable=True),
        sa.Column('video_url', sa.Text(), nullable=True),
        sa.Column('external_link', sa.Text(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_id'), 'resources', ['id'], unique=False)
    op.create_index(op.f('ix_resources_title'), 'resources', ['title'], unique=False)
    
    # Create saved_programs table
    op.create_table(
        'saved_programs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('reminder_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_saved_programs_id'), 'saved_programs', ['id'], unique=False)
    
    # Create saved_grants table
    op.create_table(
        'saved_grants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('grant_id', sa.Integer(), nullable=False),
        sa.Column('application_status', sa.String(), nullable=True),
        sa.Column('reminder_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['grant_id'], ['grants.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_saved_grants_id'), 'saved_grants', ['id'], unique=False)
    
    # Create mentor_bookings table
    op.create_table(
        'mentor_bookings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('mentor_id', sa.Integer(), nullable=False),
        sa.Column('booking_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), server_default='30', nullable=False),
        sa.Column('status', sa.String(), server_default='pending', nullable=False),
        sa.Column('meeting_link', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['mentor_id'], ['mentors.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mentor_bookings_id'), 'mentor_bookings', ['id'], unique=False)
    
    # Create user_programs table
    op.create_table(
        'user_programs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('enrollment_status', sa.String(), server_default='enrolled', nullable=False),
        sa.Column('enrollment_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('completion_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_programs_id'), 'user_programs', ['id'], unique=False)
    
    # Create referrals table
    op.create_table(
        'referrals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('referring_org_id', sa.Integer(), nullable=False),
        sa.Column('receiving_org_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('referral_type', sa.String(), nullable=False),
        sa.Column('related_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), server_default='pending', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('shared_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['receiving_org_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['referring_org_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_referrals_id'), 'referrals', ['id'], unique=False)
    
    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('admin_id', sa.Integer(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_from_user', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_bot_response', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('status', sa.String(), server_default='unanswered', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['admin_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_messages_id'), 'chat_messages', ['id'], unique=False)
    
    # Create user_achievements table
    op.create_table(
        'user_achievements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_type', sa.String(), nullable=False),
        sa.Column('achievement_name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('earned_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_achievements_id'), 'user_achievements', ['id'], unique=False)


def downgrade():
    # Drop tables in reverse order
    op.drop_index(op.f('ix_user_achievements_id'), table_name='user_achievements')
    op.drop_table('user_achievements')
    
    op.drop_index(op.f('ix_chat_messages_id'), table_name='chat_messages')
    op.drop_table('chat_messages')
    
    op.drop_index(op.f('ix_referrals_id'), table_name='referrals')
    op.drop_table('referrals')
    
    op.drop_index(op.f('ix_user_programs_id'), table_name='user_programs')
    op.drop_table('user_programs')
    
    op.drop_index(op.f('ix_mentor_bookings_id'), table_name='mentor_bookings')
    op.drop_table('mentor_bookings')
    
    op.drop_index(op.f('ix_saved_grants_id'), table_name='saved_grants')
    op.drop_table('saved_grants')
    
    op.drop_index(op.f('ix_saved_programs_id'), table_name='saved_programs')
    op.drop_table('saved_programs')
    
    op.drop_index(op.f('ix_resources_title'), table_name='resources')
    op.drop_index(op.f('ix_resources_id'), table_name='resources')
    op.drop_table('resources')
    
    op.drop_index(op.f('ix_grants_application_deadline'), table_name='grants')
    op.drop_index(op.f('ix_grants_title'), table_name='grants')
    op.drop_index(op.f('ix_grants_id'), table_name='grants')
    op.drop_table('grants')
    
    op.drop_index(op.f('ix_mentors_full_name'), table_name='mentors')
    op.drop_index(op.f('ix_mentors_id'), table_name='mentors')
    op.drop_table('mentors')
    
    op.drop_index(op.f('ix_programs_title'), table_name='programs')
    op.drop_index(op.f('ix_programs_id'), table_name='programs')
    op.drop_table('programs')
    
    # Remove columns from users table
    op.drop_column('users', 'language_preference')
    op.drop_column('users', 'profile_image')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'sector')
    op.drop_column('users', 'business_stage')


