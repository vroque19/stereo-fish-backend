from fastapi import FastAPI, File, UploadFile, Header, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
SECRET = os.environ.get("SECRET_KEY")
UPLOAD_DIRECTORY = "./static/uploaded_images"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def get_secret():
    return os.environ.get("SECRET_KEY")


@app.get("/")
def read_root():
  return {"Hello": "World"}

def verify_token(authorization: Annotated[str | None, Header()] = None):
    print(f"Received Authorization header: {authorization}")
    if authorization != f"Bearer {SECRET}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
# @app.get("/whoami")
# async def read_items(user_agent: Annotated[str | None, Header()] = None,
#     _auth: bool = Depends(verify_token)):
#    return {"User agent": user_agent}


# query parameter <-- less secure
@app.get("/whoami")
async def whoami(user_agent: Annotated[str | None, Header()] = None,
                 _auth: bool = Depends(verify_token)):
    return {"User agent": user_agent}


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), _auth: bool = Depends(verify_token)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Unsupported media type.")

    # if file is larger than 1GB
    if file.size > 10**9:
       raise HTTPException(status_code=413, detail="Payload too large")
    
    # Save the file
    contents = await file.read()
    with open(f"static/uploaded_images/{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename, "content_type": file.content_type}

@app.get("/compute_pose")
def compute_pose_from_image(img: bytes):
  # return the vertex data
  pass
  return {"Pose points": "points"}

@app.get("/test")
def compute_pose_from_image():
  # return the vertex data
  pass
  return {"Pose points": "points"}
