import asyncio
from fastapi import APIRouter, UploadFile, File, Request
from firebase_admin import storage
from property_management.utilities.upload_images import upload_image

firebase=APIRouter(
    prefix="/firebase",
    tags=["firebase"],
    responses={404: {"description": "Not found"}}
    
)

@firebase.post('/upload-images')
async def upload_files(file: list[UploadFile]=File(...), request:Request=Request):
    '''
    Upload images to firebase
    '''
    bucket = request.app.state.bucket
    file_urls = []

    for image in file:
        img_url=await upload_image(image, bucket)
        file_urls.append(img_url)

    return file_urls

