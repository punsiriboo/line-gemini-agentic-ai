import os
from google.cloud import storage


def upload_blob_from_memory(contents, type, user_id, message_id):
    """Uploads a file to the bucket."""
    bucket_name = os.environ["GCS_BUCKET_STORAGE"]
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    if type == "image":
        ext = "jpg"
    if type == "audio":
        ext = "m4a"

    destination_blob_name = f"LINE_USERS/{user_id}/{type}/{message_id}.{ext}"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)

    gsc_image_path = "gs://{}/{}".format(bucket_name, destination_blob_name)
    return gsc_image_path
