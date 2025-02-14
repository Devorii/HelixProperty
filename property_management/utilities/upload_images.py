from fastapi import UploadFile, Request




async def upload_image(file:UploadFile, num, bucket):
    file_name = f"{num}-{file.filename}"
    content_type=file.content_type or "application/octet-stream"
    blob=bucket.blob(file_name)

    try: 
        blob.upload_from_file(file.file, content_type=content_type)
        print(content_type)

        # makes the file public in firebase
        blob.make_public()
        file_url=blob.public_url

        return file_url
    except Exception as e: 
        raise Exception('Error uploading file.')
    

async def send_files(file, ticket_num, bucket):
    file_urls = []

    for image in file:
        img_url=await upload_image(image, ticket_num, bucket)
        file_urls.append(img_url)
    return file_urls

