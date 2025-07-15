from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from decouple import config

engine = create_engine(config("DATABASE_URL_SYNC"))

SessionLocal = sessionmaker(bind=engine)
