import requests
from main import get_secret


url = "https://api.vanessa.codes"

def send_image():
  # print(SECRET)
  SECRET = get_secret()
  endpoint = url+"/upload-image/"
  header = {'Authorization': f'Bearer {SECRET}'}
  with open("static/fish/FISH1.jpg", "rb") as f:
      file = {"file": ("FISH1.jpg", f, "image/jpg")}
      response = requests.post(endpoint, headers=header, files=file)
      print(response.text)
      print("Status Code:", response.status_code)
      print("Response Body:", response.json())


send_image()
