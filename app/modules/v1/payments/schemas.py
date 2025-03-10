from typing import Literal, Optional

from pydantic import BaseModel


class PayosGenerateResponse(BaseModel):
    status: Literal["success", "failed"]
    qr_code: Optional[str] = None
    qr_data_url: Optional[str] = None
