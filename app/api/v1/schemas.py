from pydantic import BaseModel, ConfigDict

# именно Hryak, не HryakClass
class HryakBase(BaseModel):

    hryak_owner_id: str
    hryak_class_id: str
    hryak_user_name: str
    date_owned: str


class HryakCreate(HryakBase):
    pass


class HryakUpdate(HryakCreate):
    pass


class HryakBaseUpdatePartial(HryakCreate):

    hryak_owner_id: str | None = None
    hryak_class_id: str | None = None
    hryak_user_name: str | None = None
    date_owned: str | None = None


class HryakClassBase():
    pass


class Hryak(HryakBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
