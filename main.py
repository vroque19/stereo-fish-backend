from fastapi import FastAPI, File, UploadFile, Header, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated, List, Tuple
from dotenv import load_dotenv
import os
from dlc import compute_points_from_image
from pydantic import BaseModel

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
async def whoami(
    user_agent: Annotated[str | None, Header()] = None,
    _auth: bool = Depends(verify_token),
):
    return {"User agent": user_agent}


class DimResponse(BaseModel):
    points: List[Tuple[float, float]]
    dimensions: List[Tuple[float, float]]  # Changed from List[float]


@app.post("/upload-image/")
async def upload_image(
    file: UploadFile = File(...), _auth: bool = Depends(verify_token)
):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=415, detail="Unsupported media type.")

        print("Uploading image...")
        if file.size > 10**9:
            raise HTTPException(status_code=413, detail="Payload too large")

        # Save the file
        try:
            contents = await file.read()
            filepath = f"static/uploaded_images/{file.filename}"
            with open(filepath, "wb") as f:
                f.write(contents)
            print(f"Image saved to {filepath}")
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"File save error: {str(e)}")

        try:
            points, dimensions = compute_points_from_image()
            response = DimResponse(points=points, dimensions=dimensions)
            return response
        except Exception as e:
            import traceback

            print(f"Error in compute_points_from_image: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

    except Exception as e:
        import traceback

        print(f"Unhandled exception: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/test")
def compute_pose_from_image():
    # return the vertex data
    pass
    return {"Pose points": "points"}
