from fastapi import FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.settings.app import AppSettings
from app.db.engine import Session, current_session
from app.db.repositories.groups import GroupsCRUD
from app.models.schemas.permissions import PermissionInCreate
from app.services.enums import GlobalGroups, GlobalPermissions
from app.db.repositories.permissions import PermissionsCrud


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
	logger.info("Connecting to PostgreSQL")

	engine = create_async_engine(settings.database_url)
	Session.configure(bind=engine)
	current_session.configure(bind=engine)

	# очень вредный кусок кода
	# async with engine.begin() as conn:
	# 	await conn.run_sync(Meta.create_all)

	app.state.engine = engine
	app.state.session = Session

	logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
	logger.info("Closing connection to database")

	await app.state.engine.dispose()

	logger.info("Connection closed")


async def create_default_permissions(app: FastAPI) -> None:
	logger.info("Creating default permissions...")
	# horrible mess...
	async with app.state.session() as session:
		session: AsyncSession
		try:
			for perm in GlobalPermissions:
				perm_mdl = PermissionInCreate(
					name=perm.name,
					code=perm.value,
				)
				_, created = await PermissionsCrud.get_or_create(session, perm_mdl, id_name="name")
				if created:
					logger.info(f"Created permission: {perm.name}")
		except Exception:
			await session.rollback()
			raise


async def create_default_groups(app: FastAPI) -> None:
	"""
	Note: Use after permissions creation

	:param app:
	:return:
	"""
	logger.info("Creating default groups...")

	async with app.state.session() as session:
		try:
			for group in GlobalGroups:
				gr, created = await GroupsCRUD.create_default(session, group)
				if created:
					logger.info(f"Group {group.name} created", extra={"groups": gr})
		except Exception:
			await session.rollback()
			raise
