"""Update organization model to new schema

Revision ID: 002_new_org_schema
Revises: 001_update_org
Create Date: 2025-11-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_new_org_schema'
down_revision = '001_update_org'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop old columns that are no longer needed
    op.drop_column('organizations', 'business_name', if_exists=True)
    op.drop_column('organizations', 'business_stage', if_exists=True)
    op.drop_column('organizations', 'description', if_exists=True)
    op.drop_column('organizations', 'industry', if_exists=True)
    op.drop_column('organizations', 'business_sector', if_exists=True)
    op.drop_column('organizations', 'business_location', if_exists=True)
    op.drop_column('organizations', 'legal_structure', if_exists=True)
    op.drop_column('organizations', 'business_status', if_exists=True)
    op.drop_column('organizations', 'email', if_exists=True)
    op.drop_column('organizations', 'social_media', if_exists=True)
    op.drop_column('organizations', 'additional_contact_info', if_exists=True)
    op.drop_column('organizations', 'updated_at', if_exists=True)
    
    # Add new columns
    op.add_column('organizations', sa.Column('organization_name', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('city', sa.String(length=100), nullable=True))
    op.add_column('organizations', sa.Column('address', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('latitude', sa.Numeric(precision=9, scale=6), nullable=True))
    op.add_column('organizations', sa.Column('longitude', sa.Numeric(precision=9, scale=6), nullable=True))
    op.add_column('organizations', sa.Column('province_state', sa.String(length=50), nullable=True))
    op.add_column('organizations', sa.Column('sector_type', sa.String(length=200), nullable=True))
    op.add_column('organizations', sa.Column('services_offered', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('email_address', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('contact_name', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('notes', sa.Text(), nullable=True))
    
    # Create index on organization_name
    op.create_index(op.f('ix_organizations_organization_name'), 'organizations', ['organization_name'], unique=False)


def downgrade() -> None:
    # Drop new columns
    op.drop_index(op.f('ix_organizations_organization_name'), table_name='organizations')
    op.drop_column('organizations', 'organization_name')
    op.drop_column('organizations', 'city')
    op.drop_column('organizations', 'address')
    op.drop_column('organizations', 'latitude')
    op.drop_column('organizations', 'longitude')
    op.drop_column('organizations', 'province_state')
    op.drop_column('organizations', 'sector_type')
    op.drop_column('organizations', 'services_offered')
    op.drop_column('organizations', 'email_address')
    op.drop_column('organizations', 'contact_name')
    op.drop_column('organizations', 'notes')
    
    # Re-add old columns (simplified - you may need to adjust based on your needs)
    op.add_column('organizations', sa.Column('business_name', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('business_stage', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('industry', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('business_sector', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('business_location', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('legal_structure', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('business_status', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('email', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('social_media', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('organizations', sa.Column('additional_contact_info', sa.Text(), nullable=True))
    op.add_column('organizations', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))


