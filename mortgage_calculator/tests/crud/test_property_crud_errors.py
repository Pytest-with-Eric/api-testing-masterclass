import pytest
import uuid

@pytest.mark.api
@pytest.mark.integration
def test_create_property_missing_payload(
    test_client, property_endpoint, property_payload
):
    # Remove the purchase price from the payload
    del property_payload["purchase_price"]

    # Create a property
    create_response = test_client.post(property_endpoint, json=property_payload)
    assert create_response.status_code == 422  # Unprocessable Entity, Client Error
    assert create_response.json() == {  # You can choose to assert the actual error message but comes with maintainance overhead
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "purchase_price"],
                "msg": "Field required",
                "input": {
                    "rental_income": 2500,
                    "renovation_cost": 50000,
                    "property_name": "123 Elm Steet",
                    "admin_costs": 3000,
                    "management_fees": 200,
                },
            }
        ]
    }

@pytest.mark.api
@pytest.mark.integration
def test_updated_property_not_found(
    test_client, property_endpoint, update_property_payload
):

    tmp_property_id = str(uuid.uuid4())
    # Update a property that does not exist
    update_response = test_client.patch(
        f"{property_endpoint}{tmp_property_id}", json=update_property_payload
    )
    assert update_response.status_code == 404  # Not Found, Client Error
    assert update_response.json() == {"detail": "Property not found."}
