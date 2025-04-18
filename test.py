from fastapi.testclient import TestClient
from main import app, get_secret
import io


client = TestClient(app)

def test_whoami():
    SECRET = get_secret()
    response = client.get(
        "/whoami",
        headers={"Authorization": f"Bearer {SECRET}"}
    )
    print(SECRET)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)
    assert response.status_code == 200

def test_upload_image():
    SECRET = get_secret()
    with open("static/fish/FISH1.jpg", "rb") as f:
      file = {"file": ("FISH1.jpg", f, "image/jpg")}
      response = client.post("/upload-image/", files = file, headers={"Authorization": f"Bearer {SECRET}"})
      print(response.text)
      print("Status Code:", response.status_code)
      print("Response Body:", response.json())

test_whoami()
test_upload_image()
