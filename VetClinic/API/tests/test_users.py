from fastapi.testclient import TestClient
from vetclinic_api.main import app
from vetclinic_api.main import app
import uuid

client = TestClient(app)

def test_create_client():
    # Przykładowe dane dla klienta
    user_data = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": f"jan.kowalsky+{uuid.uuid4()}@example.com",
        "password": "tajnehaslo",
        "role": "klient",
        "phone_number": "+48123456789",
        "address": "ul. Przykładowa 1",
        "postal_code": "00-001 Warszawa"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201, f"Status code: {response.status_code}, response: {response.text}"
