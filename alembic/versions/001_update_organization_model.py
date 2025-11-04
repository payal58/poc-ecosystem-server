"""Update organization model to new structure

Revision ID: 001_update_org
Revises: 
Create Date: 2025-01-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_update_org'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename existing columns and add new ones
    op.alter_column('organizations', 'name', new_column_name='business_name', existing_type=sa.String())
    op.alter_column('organizations', 'category', new_column_name='industry', existing_type=sa.String())
    op.alter_column('organizations', 'contact_email', new_column_name='email', existing_type=sa.String())
    
    # Add new required columns
    op.add_column('organizations', sa.Column('business_stage', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('business_sector', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('business_location', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('legal_structure', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('business_status', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('social_media', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('organizations', sa.Column('additional_contact_info', sa.Text(), nullable=True))
    
    # Set default values for new required fields
    op.execute("UPDATE organizations SET business_stage = 'Established Business' WHERE business_stage IS NULL")
    op.execute("UPDATE organizations SET business_location = 'Windsor-Essex' WHERE business_location IS NULL")
    op.execute("UPDATE organizations SET legal_structure = 'Other' WHERE legal_structure IS NULL")
    op.execute("UPDATE organizations SET business_status = 'Active' WHERE business_status IS NULL")
    op.execute("UPDATE organizations SET phone_number = '' WHERE phone_number IS NULL")
    
    # Make fields required
    op.alter_column('organizations', 'business_stage', nullable=False)
    op.alter_column('organizations', 'business_location', nullable=False)
    op.alter_column('organizations', 'legal_structure', nullable=False)
    op.alter_column('organizations', 'business_status', nullable=False)
    op.alter_column('organizations', 'phone_number', nullable=False)
    op.alter_column('organizations', 'description', nullable=False)
    op.alter_column('organizations', 'industry', nullable=False)
    op.alter_column('organizations', 'email', nullable=False)
    
    # Drop old column if it exists
    try:
        op.drop_column('organizations', 'eligibility')
    except:
        pass


def downgrade() -> None:
    # Revert changes
    op.alter_column('organizations', 'business_name', new_column_name='name', existing_type=sa.String())
    op.alter_column('organizations', 'industry', new_column_name='category', existing_type=sa.String())
    op.alter_column('organizations', 'email', new_column_name='contact_email', existing_type=sa.String())
    
    op.drop_column('organizations', 'business_stage')
    op.drop_column('organizations', 'business_sector')
    op.drop_column('organizations', 'business_location')
    op.drop_column('organizations', 'legal_structure')
    op.drop_column('organizations', 'business_status')
    op.drop_column('organizations', 'phone_number')
    op.drop_column('organizations', 'social_media')
    op.drop_column('organizations', 'additional_contact_info')
    
    op.alter_column('organizations', 'description', nullable=True)
    op.alter_column('organizations', 'category', nullable=True)
    op.alter_column('organizations', 'contact_email', nullable=True)

