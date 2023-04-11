from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os

app = FastAPI()

# Replace with your AWS S3 credentials
s3 = boto3.client('s3',
                  aws_access_key_id='INSERT_HERE',
                  aws_secret_access_key='ALSO_THIS_ONE')

BUCKET_NAME = 'your-bucket-name'
BASE_URL = 'https://yourdomain.com'

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_audio(audio: UploadFile = File(...)):
    file_key = f"audio/{audio.filename}"
    try:
        s3.upload_fileobj(audio.file, BUCKET_NAME, file_key)
        return {"status": "success", "url": f"{BASE_URL}/{file_key}"}
    except Exception as e:
        print(e)
        return {"status": "error", "message": "Failed to upload audio"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

