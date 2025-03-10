from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from modules.v1.permissions.controllers import permission_controllers
from modules.v1.role_permissions.controllers import role_permission_controllers

from . import schemas
from .services import role_services


class RoleControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def get_permissions_by_role(self, role: dict) -> list:
        # Recursively get permissions in parent role
        permissions = await role_permission_controllers.get_permissions_by_role_id(role_id=role["_id"], is_inherited_from_parent_role=False)
        while role.get("parent_role_id"):
            permission = await role_permission_controllers.get_permissions_by_role_id(role_id=role["parent_role_id"], is_inherited_from_parent_role=True)
            permissions.extend(permission)
            role = await self.get_by_id(_id=role["parent_role_id"])
        return permissions

    async def get_role_name_by_id(self, _id: str, commons: CommonsDependencies) -> str:
        result = await self.get_by_id(_id=_id, commons=commons)
        return result["name"]

    async def get_all(
        self,
        query: dict = None,
        search: str = None,
        search_in: list = None,
        page: int = 1,
        limit: int = 20,
        fields_limit: list | str = None,
        sort_by: str = "created_at",
        order_by: str = "desc",
        include_deleted: bool = False,
        commons: CommonsDependencies = None,
    ) -> dict:
        results = await super().get_all(query, search, search_in, page, limit, fields_limit, sort_by, order_by, include_deleted, commons)
        for result in results["results"]:
            if result.get("parent_role_id"):
                result["parent_role_name"] = await self.get_role_name_by_id(_id=result["parent_role_id"], commons=commons)
            result["permissions"] = await self.get_permissions_by_role(role=result)
        return results

    async def get_by_id(self, _id, fields_limit: list | str = None, ignore_error: bool = False, include_deleted: bool = False, commons: CommonsDependencies = None) -> dict:
        result = await super().get_by_id(_id, fields_limit, ignore_error, include_deleted, commons)
        if result.get("parent_role_id"):
            result["parent_role_name"] = await self.get_role_name_by_id(_id=result["parent_role_id"], commons=commons)
        result["permissions"] = await self.get_permissions_by_role(role=result)
        return result

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data = data.model_dump(by_alias=True)
        if data.get("parent_role_id"):
            await self.get_by_id(_id=data["parent_role_id"], commons=commons)
        for permission in data["permissions"]:
            await permission_controllers.get_by_id(_id=permission["_id"], commons=commons)
        role = await self.service.create(data=data, commons=commons)
        await role_permission_controllers.create_from_role(role_id=role["_id"], data=data, commons=commons)
        return await self.get_by_id(_id=role["_id"], commons=commons)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        await self.get_by_id(_id=_id, commons=commons)
        data = data.model_dump(by_alias=True, exclude_none=True)
        if data.get("permissions"):
            await role_permission_controllers.edit_from_role(role_id=_id, data=data, commons=commons)
        await self.service.edit(_id=_id, data=data, commons=commons)
        return await self.get_by_id(_id=_id, commons=commons)

    async def soft_delete_by_id(self, _id: str, ignore_error: bool = False, commons: CommonsDependencies = None) -> dict:
        await role_permission_controllers.delete_from_role(role_id=_id, commons=commons)
        return await super().soft_delete_by_id(_id, ignore_error, commons)


role_controllers = RoleControllers(controller_name="roles", service=role_services)
