from core.controllers import BaseControllers
from core.schemas import CommonsDependencies
from core.services import BaseServices
from modules.v1.roles import schemas as role_schemas

from .exceptions import ErrorCode as RolePermissionErrorCode
from .services import role_permission_services


class PermissionControllers(BaseControllers):
    def __init__(self, controller_name: str, service: BaseServices = None) -> None:
        super().__init__(controller_name, service)

    async def create_from_role(self, role_id: str, data: role_schemas.CreateRequest, commons: CommonsDependencies) -> list:
        results = []
        for permission in data["permissions"]:
            result = await self.service.create(role_id=role_id, data=permission, commons=commons)
            results.append(result)
        return results

    async def edit_from_role(self, role_id: str, data: role_schemas.EditRequest, commons: CommonsDependencies) -> list:
        results = []
        for permission in data["permissions"]:
            query = {"role_id": role_id, "permission_id": permission["_id"]}
            role_permission = await self.get_all(query=query, limit=1)
            if role_permission["total_items"] == 0:
                raise RolePermissionErrorCode.NotFound(role_id=role_id, permission_id=permission["_id"])
            role_permission = role_permission["results"][0]
            del permission["_id"]
            result = await self.service.edit(_id=role_permission["_id"], data=permission, commons=commons)
            results.append(result)
        return results

    async def get_permissions_by_role_id(self, role_id: str, is_inherited_from_parent_role: bool) -> list:
        return await self.service.get_permissions_by_role_id(role_id=role_id, is_inherited_from_parent_role=is_inherited_from_parent_role)

    async def delete_from_role(self, role_id: str, commons: CommonsDependencies) -> None:
        query = {"role_id": role_id}
        results = await self.get_all(query=query, limit=self.max_record_limit)
        for result in results["results"]:
            await self.service.soft_delete_by_id(_id=result["_id"], commons=commons)


role_permission_controllers = PermissionControllers(controller_name="role permissions", service=role_permission_services)
