from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('email', String),
    Column('role', SmallInteger),
)

assertive = Table('assertive', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('question', String(length=64)),
    Column('answer', String(length=120)),
)

negative = Table('negative', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('question', String(length=64)),
    Column('answer', String(length=120)),
)

positive = Table('positive', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('question', String(length=64)),
    Column('answer', String(length=120)),
)

wikipedia = Table('wikipedia', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('question', String(length=64)),
    Column('answer', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].drop()
    post_meta.tables['assertive'].create()
    post_meta.tables['negative'].create()
    post_meta.tables['positive'].create()
    post_meta.tables['wikipedia'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].create()
    post_meta.tables['assertive'].drop()
    post_meta.tables['negative'].drop()
    post_meta.tables['positive'].drop()
    post_meta.tables['wikipedia'].drop()
