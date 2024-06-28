def test_create_mortgage(test_client, property_payload, mortgage_payload):

    # Create a property
    create_response = test_client.post("/api/v1/property/", json=property_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created property id
    property_id = create_response_json["data"]["id"]

    # Add the property id to the mortgage payload
    mortgage_payload["property_id"] = property_id

    # Create a mortgage
    create_response = test_client.post("/api/v1/mortgage/", json=mortgage_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created mortgage id
    mortgage_id = create_response_json["data"]["id"]
    get_response = test_client.get(f"/api/v1/mortgage/{mortgage_id}")
    mortgage_data = get_response.json()["data"]
    assert get_response.status_code == 200
    assert mortgage_data["loan_to_value"] == mortgage_payload["loan_to_value"]
    assert mortgage_data["interest_rate"] == mortgage_payload["interest_rate"]
    assert mortgage_data["mortgage_type"] == mortgage_payload["mortgage_type"]
    assert mortgage_data["loan_term"] == mortgage_payload["loan_term"]
    assert mortgage_data["property_id"] == property_id
    assert mortgage_data["updatedAt"] is None


def test_update_mortgage(
    test_client, property_payload, mortgage_payload, update_mortgage_payload
):

    # Create a property
    create_response = test_client.post("/api/v1/property/", json=property_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created property id
    property_id = create_response_json["data"]["id"]

    # Add the property id to the mortgage payload
    mortgage_payload["property_id"] = property_id

    # Create a mortgage
    create_response = test_client.post("/api/v1/mortgage/", json=mortgage_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created mortgage id
    mortgage_id = create_response_json["data"]["id"]

    # Update the mortgage
    update_response = test_client.patch(
        f"/api/v1/mortgage/{mortgage_id}", json=update_mortgage_payload
    )
    assert update_response.status_code == 202

    get_response = test_client.get(f"/api/v1/mortgage/{mortgage_id}")
    mortgage_data = get_response.json()["data"]
    assert get_response.status_code == 200
    assert mortgage_data["interest_rate"] == update_mortgage_payload["interest_rate"]
    assert mortgage_data["loan_term"] == mortgage_payload["loan_term"]
    assert mortgage_data["loan_to_value"] == mortgage_payload["loan_to_value"]
    assert mortgage_data["mortgage_type"] == mortgage_payload["mortgage_type"]
    assert mortgage_data["property_id"] == property_id
    assert mortgage_data["updatedAt"] is not None


def test_delete_mortgage(test_client, property_payload, mortgage_payload):

    # Create a property
    create_response = test_client.post("/api/v1/property/", json=property_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created property id
    property_id = create_response_json["data"]["id"]

    # Add the property id to the mortgage payload
    mortgage_payload["property_id"] = property_id

    # Create a mortgage
    create_response = test_client.post("/api/v1/mortgage/", json=mortgage_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created mortgage id
    mortgage_id = create_response_json["data"]["id"]

    # Delete the mortgage
    delete_response = test_client.delete(f"/api/v1/mortgage/{mortgage_id}")
    assert delete_response.status_code == 202

    # Get the deleted mortgage
    get_response = test_client.get(f"/api/v1/mortgage/{mortgage_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Mortgage not found."
