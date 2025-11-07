from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parents[1] / ".env"


print(f"ℹ️ Using .env from: {env_path}")

load_dotenv(dotenv_path=env_path)

BASE_URL = os.getenv("PAYPAL_BASE_URL")
CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
SECRET = os.getenv("PAYPAL_SECRET")


if not BASE_URL or not CLIENT_ID or not SECRET:
    raise EnvironmentError("Check .env file: PAYPAL_BASE_URL, CLIENT_ID, SECRET must be set!")


def get_token():
    url = f"{BASE_URL}/v1/oauth2/token"
    auth = (CLIENT_ID, SECRET)
    data = {"grant_type": "client_credentials"}
    headers = {"Accept": "application/json"}
    response = requests.post(url, auth=auth, data=data, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")

@pytest.fixture(scope="session")
def auth_token():
    token = get_token()
    assert token, "Failed to get access token"
    return token

@allure.feature("PayPal Orders API")
@allure.title("TC001: Create Order - Valid Amount")
def test_create_order_valid(auth_token):
    url = f"{BASE_URL}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": "10.00"
            }
        }]
    }

    with allure.step("Send POST to create order"):
        response = requests.post(url, json=payload, headers=headers)

    with allure.step("Verify status code 201"):
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    data = response.json()
    with allure.step("Verify order created"):
        assert data["status"] == "CREATED", f"Expected CREATED, got {data['status']}"