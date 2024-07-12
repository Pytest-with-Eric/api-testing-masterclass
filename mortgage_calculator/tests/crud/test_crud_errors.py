import uuid

import pytest


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
    assert create_response.json() == {
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


@pytest.mark.api
@pytest.mark.integration
def test_create_mortgage_property_doesnt_exist(
    test_client, mortgage_endpoint, mortgage_payload
):
    # Create a mortgage for a property that does not exist
    tmp_property_id = str(uuid.uuid4())
    mortgage_payload["property_id"] = tmp_property_id
    create_response = test_client.post(mortgage_endpoint, json=mortgage_payload)
    assert create_response.status_code == 404
    assert create_response.json() == {"detail": "Property not found."}


@pytest.mark.api
@pytest.mark.integration
def test_create_mortgage_type_not_supported(
    test_client, mortgage_endpoint, property_payload, mortgage_payload
):
    # Create a property
    create_response = test_client.post("/api/v1/property/", json=property_payload)
    assert create_response.status_code == 201

    # Get the created property id
    property_id = create_response.json()["data"]["id"]

    # Create a mortgage with an unsupported mortgage type
    mortgage_payload["property_id"] = property_id
    mortgage_payload["mortgage_type"] = "unsupported"
    create_response = test_client.post(mortgage_endpoint, json=mortgage_payload)
    assert create_response.status_code == 422
    assert create_response.json() == {
        "detail": [
            {
                "type": "enum",
                "loc": ["body", "mortgage_type"],
                "msg": "Input should be 'interest_only' or 'repayment'",
                "input": "unsupported",
                "ctx": {"expected": "'interest_only' or 'repayment'"},
            }
        ]
    }
