from behave import given, when, then
import random
import json
from pathlib import Path
from api.models.request_models import PetCreateRequest
from api.models.response_models import PetResponse

TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "test_data.json"
with open(TEST_DATA_PATH, "r", encoding="utf-8") as file:
    test_data = json.load(file)

PET_PAYLOAD_RAW = test_data["api"]["pet_payload"]

@given("I prepare a request to add a new pet")
def step_prepare_pet_request(context):
    context.pet_id = random.randint(100000000, 999999999)
    context.request_payload = PetCreateRequest(
        id=context.pet_id,
        name=PET_PAYLOAD_RAW["name"],
        status=PET_PAYLOAD_RAW["status"],
        category=PET_PAYLOAD_RAW["category"],
        photoUrls=PET_PAYLOAD_RAW["photoUrls"],
        tags=PET_PAYLOAD_RAW["tags"]
    )

@when("I send the add pet API request")
def step_send_add_pet(context):
    context.created_pet = context.petstore_client.add_pet(context.request_payload)

@then("the API response should contain the pet details")
def step_verify_created_pet(context):
    assert context.created_pet.id is not None, "Created pet ID missing"
    assert context.created_pet.name == context.request_payload.name
    assert context.created_pet.status == context.request_payload.status

@then("I should be able to fetch the pet by ID via API")
def step_fetch_pet_by_id(context):
    context.fetched_pet = context.petstore_client.get_pet(context.created_pet.id)

@then("the fetched pet details should match the created pet")
def step_verify_fetched_pet(context):
    assert context.fetched_pet.id == context.created_pet.id
    assert context.fetched_pet.name == context.created_pet.name
    assert context.fetched_pet.status == context.created_pet.status
    # Cleanup
    context.petstore_client.delete_pet(context.created_pet.id)

@given('I have created a pet with status "{status}"')
def step_create_pet_with_status(context, status):
    context.pet_id = random.randint(100000000, 999999999)
    payload = PetCreateRequest(
        id=context.pet_id,
        name="UpdateTestPet",
        status=status,
        photoUrls=["https://example.com/updatetest.jpg"]
    )
    context.created_pet = context.petstore_client.add_pet(payload)

@when('I update the pet status to "{status}" via API')
def step_update_pet_status(context, status):
    context.created_pet.status = status
    context.updated_pet = context.petstore_client.update_pet(context.created_pet)

@then('the pet status should be updated to "{status}"')
def step_verify_updated_status(context, status):
    assert context.updated_pet.status == status

@then('the pet should be found in the {status} list')
def step_verify_pet_in_list(context, status):
    pets = context.petstore_client.find_pets_by_status(status)
    ids = [p.id for p in pets]
    assert context.created_pet.id in ids, f"Pet {context.created_pet.id} not found in {status} list"
    # Cleanup
    context.petstore_client.delete_pet(context.created_pet.id)

@given("I have created a pet via API")
def step_create_pet_api(context):
    context.pet_id = random.randint(100000000, 999999999)
    payload = PetCreateRequest(
        id=context.pet_id,
        name="DBVerificationPet",
        status="pending",
        photoUrls=["https://example.com/dbverify.jpg"],
        category={"id": 2, "name": "Cats"}
    )
    context.created_pet = context.petstore_client.add_pet(payload)

@when("I mirror the pet record in the local database")
def step_mirror_pet_db(context):
    category_name = context.created_pet.category.name if context.created_pet.category else None
    context.db_helper.execute(
        "INSERT INTO pets (id, name, status, category_name) VALUES (?, ?, ?, ?)",
        (context.created_pet.id, context.created_pet.name, context.created_pet.status, category_name)
    )

@then("the pet details in the database should match the API response")
def step_verify_pet_db(context):
    db_record = context.db_helper.fetch_one("SELECT * FROM pets WHERE id = ?", (context.created_pet.id,))
    assert db_record is not None, "Pet record not found in local database"
    assert db_record["id"] == context.created_pet.id
    assert db_record["name"] == context.created_pet.name
    assert db_record["status"] == context.created_pet.status
    
    category_name = context.created_pet.category.name if context.created_pet.category else None
    assert db_record["category_name"] == category_name
    
    # Cleanup DB and API
    context.db_helper.execute("DELETE FROM pets WHERE id = ?", (context.created_pet.id,))
    context.petstore_client.delete_pet(context.created_pet.id)
