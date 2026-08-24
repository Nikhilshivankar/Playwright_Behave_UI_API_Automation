from pydantic import BaseModel, Field
from typing import List, Optional
from api.models.request_models import CategoryModel, TagModel

class PetResponse(BaseModel):
    id: Optional[int] = None
    category: Optional[CategoryModel] = None
    name: Optional[str] = None
    photoUrls: Optional[List[Optional[str]]] = None
    tags: Optional[List[TagModel]] = None
    status: Optional[str] = None

class OrderResponse(BaseModel):
    id: Optional[int] = None
    pet_id: Optional[int] = Field(default=None, validation_alias="petId", serialization_alias="petId")
    quantity: Optional[int] = None
    ship_date: Optional[str] = Field(default=None, validation_alias="shipDate", serialization_alias="shipDate")
    status: Optional[str] = None
    complete: Optional[bool] = None

class ApiResponse(BaseModel):
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None
