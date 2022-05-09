import secrets
import io
import base64

from flask import Flask, render_template, request

from google.cloud import storage
from google.cloud import vision
from io import BytesIO


GCS_BUCKET_NAME = "aretheysimilarapp-images"

app = Flask(__name__)

#limit file size - 7Mb
app.config['MAX_CONTENT_LENGTH'] = 7 * 1024 * 1024 

@app.route("/", methods=["GET", "POST"])
def index():
    image_data= dict()

    if request.method == 'POST': #on file upload
        file = request.files['file']
        if file.filename != "":
            _store_file_in_gcs(image_data, file)
            _retrieve_simmilar_image_urls(image_data)

    return render_template("index.html", image_data=image_data)

def _store_file_in_gcs(image_data, file):
    # Create GCS client
    storage_client = storage.Client()

    # Get bucket where the image will be uploaded to
    bucket = storage_client.get_bucket(GCS_BUCKET_NAME)

    # Create a new blob and upload the file's content.
    # add random hext to file name as prefix
    blob = bucket.blob(secrets.token_hex(4) + " " + file.filename)
    blob.upload_from_string(file.read(), content_type=file.content_type)
    image_data["image_gcs_link"] = "gs://{}/{}".format(GCS_BUCKET_NAME, blob.name)

    #get stored original image contents for visualisation
    imgBytes = BytesIO(blob.download_as_bytes())
    imgBytesEncoded = base64.b64encode(imgBytes.getvalue()).decode()
    image_data["original_image"] = 'data:{};base64,{}'.format(blob.content_type, imgBytesEncoded)

def _retrieve_simmilar_image_urls(image_data):
    # Create a Cloud Vision client.
    vision_client = vision.ImageAnnotatorClient()

    # Create image from provided gcs link
    image = vision.Image()
    image.source.gcs_image_uri = image_data["image_gcs_link"]

    # Use the Cloud Vision client for collecting 8 visually similar images to the given one
    web_detection_annotations = vision_client.web_detection(image=image, max_results=8).web_detection

    image_data['best_guess_labels'] = []
    image_data['similar_image_urls'] = []

    # collect best guess labels
    if web_detection_annotations.best_guess_labels:
        image_data['best_guess_labels'] = [label.label for label in web_detection_annotations.best_guess_labels]

    #collect list of visually similar urls
    if web_detection_annotations.visually_similar_images:
        image_data['similar_image_urls'] = [img.url for img in web_detection_annotations.visually_similar_images]



@app.errorhandler(500)
def server_error(e):
    return ("<h2>Oh no!</h2><br>An internal error occurred <pre>{}</pre>".format(e), 500)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

