from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('SetupID', INTEGER, primary_key=True, nullable=False),
    Column('RelayScenarioID', INTEGER),
    Column('RelayID', INTEGER),
    Column('State', BOOLEAN),
)

RelayScenarioSetup = Table('RelayScenarioSetup', post_meta,
    Column('RelayScenarioID', Integer, primary_key=True, nullable=False),
    Column('RelayID', Integer, primary_key=True, nullable=False),
    Column('State', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['RelayScenarioSetup'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['RelayScenarioSetup'].drop()
