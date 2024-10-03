from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .constants import DB_CONNECTION

# Создание движка для базы данных
engine = create_engine(
    'postgresql://{user}:{password}@{host}:5432/{dbname}'.format(**DB_CONNECTION),
    echo=True,
)

# Создание фабрики сессий
Session = sessionmaker(bind=engine)

from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
