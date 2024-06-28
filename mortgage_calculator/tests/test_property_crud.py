def test_create_property(test_client, property_payload):
    create_response = test_client.post("/api/v1/property/", json=property_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created property id
    property_id = create_response_json["data"]["id"]
    get_response = test_client.get(f"/api/v1/property/{property_id}")
    property_data = get_response.json()["data"]
    assert get_response.status_code == 200
    assert property_data["purchase_price"] == property_payload["purchase_price"]
    assert property_data["rental_income"] == property_payload["rental_income"]
    assert property_data["renovation_cost"] == property_payload["renovation_cost"]
    assert property_data["property_name"] == property_payload["property_name"]
    assert property_data["updatedAt"] is None


def test_update_property(test_client, property_payload, update_property_payload):
    create_response = test_client.post("/api/v1/property/", json=property_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created property id
    property_id = create_response_json["data"]["id"]
    update_response = test_client.patch(
        f"/api/v1/property/{property_id}", json=update_property_payload
    )
    property_data = update_response.json()["data"]
    assert update_response.status_code == 202
    assert property_data["rental_income"] == update_property_payload["rental_income"]
    assert property_data["property_name"] == update_property_payload["property_name"]
    assert (
        property_data["purchase_price"] == property_payload["purchase_price"]
    )  # Check purchase price is not updated
    assert (
        property_data["renovation_cost"] == property_payload["renovation_cost"]
    )  # Check renovation cost is not updated
    assert property_data["updatedAt"] is not None


def test_delete_property(test_client, property_payload):
    create_response = test_client.post("/api/v1/property/", json=property_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created property id
    property_id = create_response_json["data"]["id"]

    # Delete the property
    delete_response = test_client.delete(f"/api/v1/property/{property_id}")
    assert delete_response.status_code == 202

    # Get the deleted property
    get_response = test_client.get(f"/api/v1/property/{property_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Property not found."


# TODO - Test cases for error handling
