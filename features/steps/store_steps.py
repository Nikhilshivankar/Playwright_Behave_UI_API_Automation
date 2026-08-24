from behave import given, when, then
from api.models.request_models import OrderCreateRequest

@given("I place an order for pet ID {pet_id:d} with quantity {quantity:d}")
def step_place_order(context, pet_id, quantity):
    payload = OrderCreateRequest(
        petId=pet_id,
        quantity=quantity,
        status="placed",
        complete=False
    )
    context.order = context.petstore_client.place_order(payload)
    assert context.order.id is not None, "Order ID missing"

@when("I mirror the order record in the local database")
def step_mirror_order_db(context):
    context.db_helper.execute(
        "INSERT INTO orders (id, pet_id, quantity, status, complete) VALUES (?, ?, ?, ?, ?)",
        (context.order.id, context.order.pet_id, context.order.quantity, context.order.status, context.order.complete)
    )

@then("the order in the database should match the order API response")
def step_verify_order_db(context):
    db_record = context.db_helper.fetch_one("SELECT * FROM orders WHERE id = ?", (context.order.id,))
    assert db_record is not None, "Order record not found in local DB"
    assert db_record["id"] == context.order.id
    assert db_record["pet_id"] == context.order.pet_id
    assert db_record["quantity"] == context.order.quantity
    assert db_record["status"] == context.order.status
    assert bool(db_record["complete"]) == context.order.complete

@then("I should be able to fetch the order details via API")
def step_fetch_order_api(context):
    fetched = context.petstore_client.get_order(context.order.id)
    assert fetched.id == context.order.id

@then("I delete the order via API")
def step_delete_order_api(context):
    delete_res = context.petstore_client.delete_order(context.order.id)
    assert delete_res.code == 200 or str(delete_res.message) == str(context.order.id)

@then("the local database order record should be cleaned up")
def step_cleanup_order_db(context):
    context.db_helper.execute("DELETE FROM orders WHERE id = ?", (context.order.id,))
    db_record = context.db_helper.fetch_one("SELECT * FROM orders WHERE id = ?", (context.order.id,))
    assert db_record is None, "Order record was not deleted from local DB"
