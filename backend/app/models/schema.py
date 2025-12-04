from pydantic import BaseModel

class UploadResp(BaseModel):
    ok: bool
    meta: dict

class QueryReq(BaseModel):
    query: str
