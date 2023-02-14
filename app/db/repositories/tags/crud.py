from app.db.repositories.common import BaseCrud
from app.models.domain.tag import TagsInDB

from .model import Tags


class TagsCRUD(BaseCrud[Tags, TagsInDB, TagsInDB]):
	model = Tags

