import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers
from sqlalchemy.orm import sessionmaker

from allocation.adapters.orm import metadata
from allocation.adapters.orm import start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
