from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine
from modules.v1.permissions.services import permission_services

from . import models, schemas


class PermissionServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create(self, role_id: str, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data["permission_id"] = data["_id"]
        data["role_id"] = role_id
        data["created_by"] = self.get_current_user(commons=commons)
        data["created_at"] = self.get_current_datetime()
        data_save = models.RolePermissions(**data).model_dump()
        return await self.save_unique(data=data_save, unique_field=["role_id", "permission_id"])

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        data["updated_by"] = self.get_current_user(commons=commons)
        data["updated_at"] = self.get_current_datetime()
        return await self.update_by_id(_id=_id, data=data)

    async def get_permissions_by_role_id(self, role_id: str, is_inherited_from_parent_role: bool) -> list:
        query = {"role_id": role_id}
        results = await self.get_all(query=query, limit=self.maximum_document_limit)
        for result in results["results"]:
            result["is_inherited_from_parent_role"] = is_inherited_from_parent_role
            permission = await permission_services.get_by_id(_id=result["permission_id"])
            result["name"] = permission["name"]
            result["scope"] = permission["scope"]
            result["group"] = permission["group"]
            result["description"] = permission["description"]
        return results["results"]


role_permission_crud = BaseCRUD(database_engine=app_engine, collection="role_permissions")
role_permission_services = PermissionServices(service_name="role permissions", crud=role_permission_crud)
