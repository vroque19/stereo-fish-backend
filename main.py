from fastapi import FastAPI, File, UploadFile, Header, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated


app = FastAPI()
SECRET = "secret-key"



@app.get("/")
def read_root():
  return {"Hello": "World"}

# Dependency to check token
def verify_token(authorization: Annotated[str | None, Header()] = None):
    print(f"Received Authorization header: {authorization}")
    if authorization != f"Bearer {SECRET}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
@app.get("/whoami")
async def read_items(user_agent: Annotated[str | None, Header()] = None,
    _auth: bool = Depends(verify_token)):
   return {"User agent": user_agent}


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"error": "File is not an image."}, status_code=400)

    # Save the file (optional)
    contents = await file.read()
    with open(f"uploaded_images/{file.filename}", "wb") as f:
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
