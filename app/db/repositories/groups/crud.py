import enum
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.common import BaseCrud
from app.models.domain import GroupInDB, PermissionsInDB
from app.db.repositories.permissions import PermissionsCrud
from app.services.utils import convert_list_obj_to_model

from .model import Groups


class GroupsCRUD(BaseCrud[Groups, GroupInDB, GroupInDB]):
	model = Groups

	@classmethod
	async def create_default(cls, db: AsyncSession, group_enum: enum.Flag) -> Tuple[Groups, bool]:
		"""
		ONLY used by events.create_default_permissions
		and in future will be used in testing purposes.

		:param db: session
		:param group_enum: value of the GlobalGroups enum
		:return:
		"""
		does_not_exists_err = "permissions with name: {name} does not exists"

		if " " in group_enum.value and len(group_enum.value.split()) > 1:
			# better don't look at this...
			# permissions split up by spaces
			permission_names = group_enum.value.split()
			perms = []

			for name in permission_names:
				_temp = await PermissionsCrud.get_by_kwargs(db, name=name)
				if not _temp:
					raise ValueError(does_not_exists_err.format(_temp.name))
				perms.append(_temp)
		else:
			perms = await PermissionsCrud.get_by_kwargs(db, name=group_enum.value)
			if not perms:
				raise ValueError(does_not_exists_err.format(perms.name))
			perms = [perms]

		perms = convert_list_obj_to_model(perms, PermissionsInDB)

		group_mdl = GroupInDB(
			name=group_enum.name,
			users=[],
			permissions=[*perms],
		)

		group, created = await GroupsCRUD.get_or_create(db, group_mdl, id_name="name")
		if created:
			return group, True
		return group, False
