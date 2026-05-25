"""FastAPI application entry point."""
from datetime import datetime
import uuid

from botocore.exceptions import ClientError
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.config import settings
from app.s3_client import s3

app = FastAPI(title="S3 Uploader API")


class UploadResponse(BaseModel):
    filename: str
    content_type: str
    s3_key: str
    status: str

class FileInfo(BaseModel):
    s3_key: str
    size_bytes: int
    last_modified: datetime

class DownloadResponse(BaseModel):
    s3_key: str
    download_url: str
    expires_in_seconds: int

class RootResponse(BaseModel):
    status: str = "Ok"
    bucket: str = settings.s3_bucket_name
    region: str = settings.aws_region

class DeleteResponse(BaseModel):
    stayus: str
    s3_key: str

@app.get("/", response_model=RootResponse)
def root():
    return RootResponse


@app.post("/upload", response_model=UploadResponse)
def upload_file(file: UploadFile = File(...)):
    # Reject files that exceed the size limit
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if file.size is not None and file.size > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=(
                f"File too large ({file.size} bytes). "
                f"Max allowed: {settings.max_upload_size_mb} MB."
            ),
        )

    # Build a collision-proof S3 key
    s3_key = f"uploads/{uuid.uuid4()}-{file.filename}"

    try:
        s3.upload_fileobj(file.file, settings.s3_bucket_name, s3_key)
    except ClientError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"S3 upload failed: {exc}",
        )

    return UploadResponse(
        filename=file.filename,
        content_type=file.content_type,
        s3_key=s3_key,
        status="uploaded",
    )

@app.get("/files", response_model=list[FileInfo])
def list_files():
    try:
        response = s3.list_objects_v2(Bucket=settings.s3_bucket_name, Prefix="uploads/")
    except ClientError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list files: {exc}",
        )

    contents = response.get("Contents", [])
    return [
        FileInfo(
            s3_key=obj["Key"],
            size_bytes=obj["Size"],
            last_modified=obj["LastModified"],
        )
        for obj in contents
    ]
@app.get("/download", response_model=DownloadResponse)
def get_download_url(key: str, expires_in: int = 300):
    """Generate a presigned URL for downloading a file from S3.

    The URL is valid for `expires_in` seconds (default 5 minutes).
    """
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": settings.s3_bucket_name,
                "Key": key,
            },
            ExpiresIn=expires_in,
        )
    except ClientError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate download URL: {exc}",
        )

    return DownloadResponse(
        s3_key=key,
        download_url=url,
        expires_in_seconds=expires_in,
    )

@app.delete("/delete", response_model=DeleteResponse)
def delete_file(key:str):
    file_list = list_files()
    print (f"File list: {file_list}")
    for f in file_list:
        if f.s3_key!=key:
            raise HTTPException(status_code=404, detail=f"File not found with key: {key}")  
        else:
            try:
                s3.delete_object(Bucket=settings.s3_bucket_name, Key=key)
            except ClientError as exc:
                raise HTTPException(status_code=500, detail=f"Failed to delete file: {exc}")
    return DeleteResponse(status="deleted", s3_key=key)