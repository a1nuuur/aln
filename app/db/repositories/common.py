from typing import Generic, TypeVar, List, Union, Dict, Any, Optional, Iterator, Tuple

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import sqlalchemy as sa
from loguru import logger
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.base import BaseModel as DBBaseModel


ExModelType = TypeVar("ExModelType", bound=DBBaseModel)
ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
	"""
	Provides basic CRUD support system,
	with extra method support - get_multi, create_with_relationship, get_or_create

	Usages:
	Crud.create_with_relationship(CreateSchemaType)

	"""
	model: sa.Table

	@classmethod
	async def get(cls, db: AsyncSession, id: Any) -> Optional[ModelType]:
		result = await db.execute(sa.select(cls.model).where(cls.model.id == id))
		return result.first()

	@classmethod
	async def get_multi(
			cls, db: AsyncSession, skip: int = 0, limit: int = 100
	) -> List[ModelType]:
		return await db.run_sync(db.query(cls.model).offset(skip).limit(limit).all())

	@classmethod
	async def get_by_values(
			cls, db: AsyncSession, values: list[Any], key: str = "id"
	) -> Optional[Iterator[ModelType]]:
		stmt = sa.select(cls.model).filter_by(**{key: x for x in values})
		result = await db.execute(stmt)
		return result.all()

	@classmethod
	async def get_by_kwargs(
			cls, db: AsyncSession, **kwargs: Any
	) -> Optional[ModelType]:
		stmt = sa.select(cls.model).filter_by(**kwargs)
		result = await db.execute(stmt)
		return result.scalar_one()

	@classmethod
	async def get_or_create(
			cls, db: AsyncSession, obj_in: CreateSchemaType, id_name: str = "id"
	) -> Tuple[ModelType, bool]:
		kw = {id_name: getattr(obj_in, id_name)}
		try:
			group = await cls.get_by_kwargs(db, **kw)
			return group, False
		except NoResultFound:
			return await cls.create(db, obj_in.copy()), True

	@classmethod
	async def create_list(cls, db: AsyncSession, obj_in: List[CreateSchemaType]) -> List[ModelType]:
		ret_models = []
		for obj in obj_in:
			obj_data = jsonable_encoder(obj, exclude_unset=True)
			model_obj = cls.model(**obj_data)
			db.add(model_obj)
			ret_models.append(model_obj)
		await db.commit()

		return ret_models

	@classmethod
	async def create(cls, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
		obj_in_data = jsonable_encoder(obj_in, exclude_unset=True)
		db_obj = cls.model(**obj_in_data)
		# InstrumentedAttribute.type
		db.add(db_obj)
		await db.commit()
		await db.refresh(db_obj)  # is it detached?
		return db_obj

	@classmethod
	async def create_with_relationship(
			cls,
			db: AsyncSession,
			obj_in: CreateSchemaType,
			additional_opts: Dict[str, Any] = None,
			**relationships: Union[List[sa.Table], sa.Table],
	) -> ModelType:
		obj_in_data: dict = jsonable_encoder(obj_in, exclude_unset=True)
		if additional_opts:
			obj_in_data.update(**additional_opts)
		db_obj = cls.model(**obj_in_data)
		for key, value in relationships.items():
			if isinstance(value, list):
				rel = getattr(db_obj, key)
				for val in value:
					rel.add(val)
			setattr(db_obj, key, value)
		db.add(db_obj)
		await db.commit()
		await db.refresh(db_obj)  # WARNING: is it detached?
		return db_obj

	@classmethod
	async def update(
			cls,
			db: AsyncSession,
			db_obj: ModelType,
			obj_in: Union[UpdateSchemaType, Dict[str, Any]]
	) -> ModelType:
		logger.info(
			f"Changed object: {cls.model.__tablename__}")
		obj_data = jsonable_encoder(db_obj)
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)
		for field in obj_data:
			if field in update_data:
				setattr(db_obj, field, update_data[field])
		db.add(db_obj)
		await db.commit()
		await db.refresh(db_obj)  # Is it detached?
		return db_obj

	@classmethod
	async def delete(cls, db: AsyncSession, id: int) -> ModelType:
		logger.info(
			f"Removed object: {cls.model.__tablename__} from database data.")

		obj = await db.get(cls.model, id)
		await db.delete(obj)
		await db.commit()
		return obj
