from core.schemas import CommonsDependencies, ObjectIdStr
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from . import schemas
from .controllers import payment_controllers

router = InferringRouter(
    prefix="/v1",
    tags=["v1/payments"],
)


@cbv(router)
class RoutersCBV:
    commons: CommonsDependencies = Depends(CommonsDependencies)  # type: ignore

    @router.get("/payments/payos/generate", status_code=200, responses={200: {"model": schemas.PayosGenerateResponse, "description": "Get items success"}})
    async def generate_qr(self, order_id: ObjectIdStr):
        result = await payment_controllers.generate_qr(order_id)
        return schemas.PayosGenerateResponse(**result)
