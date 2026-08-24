from typing import List
from playwright.sync_api import APIRequestContext
from api.models.request_models import PetCreateRequest, OrderCreateRequest
from api.models.response_models import PetResponse, OrderResponse, ApiResponse
from utils.logger import logger

class PetstoreClient:
    """
    PetstoreClient interacts with the Swagger Petstore API endpoints.
    It encapsulates APIRequestContext, logs queries, validates status codes,
    and converts requests/responses using strongly-typed Pydantic models.
    """
    def __init__(self, request_context: APIRequestContext, base_url: str):
        self.request = request_context
        self.base_url = base_url

    # --- Pet Endpoints ---

    def add_pet(self, payload: PetCreateRequest) -> PetResponse:
        """POST /pet - Add a new pet to the store."""
        endpoint = f"{self.base_url}/pet"
        payload_data = payload.model_dump(by_alias=True, exclude_none=True)
        
        logger.info(f"API POST Request -> {endpoint}")
        logger.debug(f"Payload: {payload_data}")
        
        response = self.request.post(endpoint, data=payload_data)
        logger.info(f"API POST Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return PetResponse(**response.json())

    def get_pet(self, pet_id: int) -> PetResponse:
        """GET /pet/{petId} - Find pet by ID."""
        endpoint = f"{self.base_url}/pet/{pet_id}"
        logger.info(f"API GET Request -> {endpoint}")
        
        response = self.request.get(endpoint)
        logger.info(f"API GET Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return PetResponse(**response.json())

    def update_pet(self, payload: PetCreateRequest) -> PetResponse:
        """PUT /pet - Update an existing pet."""
        endpoint = f"{self.base_url}/pet"
        payload_data = payload.model_dump(by_alias=True, exclude_none=True)
        
        logger.info(f"API PUT Request -> {endpoint}")
        logger.debug(f"Payload: {payload_data}")
        
        response = self.request.put(endpoint, data=payload_data)
        logger.info(f"API PUT Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return PetResponse(**response.json())

    def find_pets_by_status(self, status: str) -> List[PetResponse]:
        """GET /pet/findByStatus - Finds pets by status."""
        endpoint = f"{self.base_url}/pet/findByStatus"
        logger.info(f"API GET Request -> {endpoint}?status={status}")
        
        response = self.request.get(endpoint, params={"status": status})
        logger.info(f"API GET Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return [PetResponse(**item) for item in response.json()]

    def delete_pet(self, pet_id: int) -> ApiResponse:
        """DELETE /pet/{petId} - Deletes a pet."""
        endpoint = f"{self.base_url}/pet/{pet_id}"
        logger.info(f"API DELETE Request -> {endpoint}")
        
        response = self.request.delete(endpoint)
        logger.info(f"API DELETE Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return ApiResponse(**response.json())

    # --- Store Endpoints ---

    def place_order(self, payload: OrderCreateRequest) -> OrderResponse:
        """POST /store/order - Place an order for a pet."""
        endpoint = f"{self.base_url}/store/order"
        payload_data = payload.model_dump(by_alias=True, exclude_none=True)
        
        logger.info(f"API POST Request -> {endpoint}")
        logger.debug(f"Payload: {payload_data}")
        
        response = self.request.post(endpoint, data=payload_data)
        logger.info(f"API POST Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return OrderResponse(**response.json())

    def get_order(self, order_id: int) -> OrderResponse:
        """GET /store/order/{orderId} - Find purchase order by ID."""
        endpoint = f"{self.base_url}/store/order/{order_id}"
        logger.info(f"API GET Request -> {endpoint}")
        
        response = self.request.get(endpoint)
        logger.info(f"API GET Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return OrderResponse(**response.json())

    def delete_order(self, order_id: int) -> ApiResponse:
        """DELETE /store/order/{orderId} - Delete purchase order by ID."""
        endpoint = f"{self.base_url}/store/order/{order_id}"
        logger.info(f"API DELETE Request -> {endpoint}")
        
        response = self.request.delete(endpoint)
        logger.info(f"API DELETE Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return ApiResponse(**response.json())

    # --- User / Auth Endpoints ---

    def login_user(self, username: str, password: str) -> str:
        """GET /user/login - Logs user into the system."""
        endpoint = f"{self.base_url}/user/login"
        logger.info(f"API GET Request (Login) -> {endpoint} with username: '{username}'")
        
        response = self.request.get(endpoint, params={"username": username, "password": password})
        logger.info(f"API Login Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return response.text()

    def logout_user(self) -> str:
        """GET /user/logout - Logs out current logged in user session."""
        endpoint = f"{self.base_url}/user/logout"
        logger.info(f"API GET Request (Logout) -> {endpoint}")
        
        response = self.request.get(endpoint)
        logger.info(f"API Logout Response Status: {response.status}")
        assert response.status == 200, f"Expected 200 OK, got {response.status}. Response: {response.text()}"
        
        return response.text()
