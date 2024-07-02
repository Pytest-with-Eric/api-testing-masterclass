from app.custom.calculations import (
    calculate_interest_only_payment,
    calculate_repayment_mortgage_payment,
)


def test_interest_only_payment():
    loan_amount = 100000
    annual_interest_rate = 3
    expected_payment = 250
    payment = calculate_interest_only_payment(loan_amount, annual_interest_rate)
    assert payment == expected_payment


def test_repayment_payment():
    loan_amount = 100000
    annual_interest_rate = 3
    loan_term_years = 30
    expected_payment = 421.60
    payment = calculate_repayment_mortgage_payment(
        loan_amount, annual_interest_rate, loan_term_years
    )
    assert payment == expected_payment


def test_mortgage_payment_endpoint(
    test_client, db_session, property_payload, mortgage_payload
):
    # Create a property
    create_response = test_client.post("/api/v1/property/", json=property_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created property id
    property_id = create_response_json["data"]["id"]

    # Create a Repayment mortgage
    mortgage_payload["property_id"] = property_id
    create_response = test_client.post("/api/v1/mortgage/", json=mortgage_payload)
    create_response_json = create_response.json()
    assert create_response.status_code == 201

    # Get the created mortgage id
    mortgage_id = create_response_json["data"]["id"]

    # Get the mortgage payment
    get_response = test_client.post(f"/api/v1/mortgage/{mortgage_id}/payment")
    mortgage_payment = get_response.json()
    assert get_response.status_code == 200
    assert (
        mortgage_payment["mortgage_id"] is not None
        and float(mortgage_payment["monthly_payment"])
        > 0  # TODO - Return this field as a float
    )
