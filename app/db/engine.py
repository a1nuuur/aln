import asyncio

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker


__all__ = "get_db", "get_meta", "get_current_session"

# here will be some global variables,
# not intended to be used in routes, use dependencies instead.
Meta = MetaData()
Base = declarative_base(metadata=Meta)
Session = async_sessionmaker(expire_on_commit=False, autoflush=False, class_=AsyncSession)  # noqa
current_session = async_scoped_session(Session, asyncio.current_task)


def get_db() -> AsyncSession:
	"""
	You had to use get_db function
	instead of directly using Session variable

	:return:
	"""
	return Session()


def get_current_session() -> async_scoped_session:
	return current_session


def get_meta() -> MetaData:
	return Meta
