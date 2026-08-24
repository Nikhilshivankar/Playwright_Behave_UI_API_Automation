from pydantic import BaseModel, Field
from typing import List, Optional

class CategoryModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class TagModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class PetCreateRequest(BaseModel):
    id: Optional[int] = None
    category: Optional[CategoryModel] = None
    name: str
    photoUrls: List[str]
    tags: Optional[List[TagModel]] = None
    status: Optional[str] = None

class OrderCreateRequest(BaseModel):
    id: Optional[int] = None
    pet_id: Optional[int] = Field(default=None, serialization_alias="petId", validation_alias="petId")
    quantity: Optional[int] = None
    ship_date: Optional[str] = Field(default=None, serialization_alias="shipDate", validation_alias="shipDate")
    status: Optional[str] = None
    complete: Optional[bool] = None
