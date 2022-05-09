from google.cloud import vision
from google.cloud import firestore
import secrets

def on_image_upload(event, context):
    file_name = event['name']
    file_bucket = event['bucket']
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.gcs_image_uri = f"gs://{file_bucket}/{file_name}"
    response = client.label_detection(image=image)
    labels = response.label_annotations
    ### TBD ###

