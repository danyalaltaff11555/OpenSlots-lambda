import pytest
from utils.response import success_response, error_response


def test_success_response():
    response = success_response({"key": "value"})

    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    assert "data" in response["body"]


def test_success_response_custom_status():
    response = success_response({"key": "value"}, status_code=201)

    assert response["statusCode"] == 201


def test_error_response():
    response = error_response("Something went wrong", status_code=400)

    assert response["statusCode"] == 400
    assert "error" in response["body"]
