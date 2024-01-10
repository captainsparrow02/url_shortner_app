from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str

class URL(URLBase):
    clicks: int
    is_active: bool

    class Config:
        from_attributes: True

class URLInfo(URL):
    url: str
    admin_url: str

    class Config:
        from_attributes: True