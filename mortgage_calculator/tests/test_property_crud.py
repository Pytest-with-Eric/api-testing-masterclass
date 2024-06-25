def test_create_property(test_client, property_payload):
    response = test_client.post("/api/mortgage/property/", json=property_payload)
    print(response.json())
    assert response.status_code == 201

    # Get the created property
    print(property_payload)
    response = test_client.get(f"/api/mortgage/property/{property_payload['id']}")
    # assert response.status_code == 200
    response_json = response.json()
    print(response_json)

    # TODO - Get the Property ID from the response and Query it.
