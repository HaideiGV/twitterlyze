from aiopg.sa import create_engine
import sqlalchemy as sa

metadata = sa.MetaData()

CONNECTION = 'dbname=postgres user=postgres password=admin host=127.0.0.1'


async def get_pool():
    return await create_engine(
        user='postgres',
        database='postgres',
        host='127.0.0.1',
        password='admin'
    )


async def init_pg(app):
    app['db'] = await create_engine(
        user='postgres',
        database='postgres',
        host='127.0.0.1',
        password='admin'
    )


posts_analytic = sa.Table(
    'posts_analytic',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('executed_at', sa.DateTime),
    sa.Column('interval', sa.Integer),
    sa.Column('search_phrase', sa.String),
    sa.Column('top_hashtags', sa.ARRAY(sa.String)),
    sa.Column('top_phrases', sa.ARRAY(sa.String)),
    sa.Column('top_publisher', sa.Integer),
    sa.Column('tweet_count', sa.Integer)
)

search_settings = sa.Table(
    'search_settings',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('search_phrase', sa.String),
    sa.Column('search_interval', sa.Integer)
)
