# Are They Similar?
Image analysis example application created by using GCP components and Vision AI.

## Are They Similar? application description
Application allows you to upload the image and then returns up to 8 visually similar images from internet.

## Pre-reqs
- Go to https://console.cloud.google.com/, select the project where app will be deployed
-  Check if Cloud Vision API is enabled for your project.
    * Navigate to APIs & Services -> [Library](https://console.cloud.google.com/apis/library/browse)
    * Find Cloud Vision API and if it is not enabled, do so.
    * Otherwise execute below command in Cloud shell
        ```shell
        gcloud services enable vision.googleapis.com
        ```
        If command fails - most probably API have been enabled already (check error message).
- Open Cloud Shell and set project id variable
```shell
export PROJECT_ID=$(gcloud config get-value core/project)
echo $PROJECT_ID
```
- Create Google cloud storage bucktet. Uploaded images will be stored there.
```shell
export ATS_IMAGES_BUCKET = {PROJECT_ID}-aretheysimilar-images
gsutil mb -l eu gs://$ATS_IMAGES_BUCKET
```
Flag **-l** defines that bucket location is Europe.
- Change bucket name in are-they-similar-app/main.py. Find variable <i>GCS_BUCKET_NAME</i> and change its value to your buckets name.
```shell
GCS_BUCKET_NAME = "aretheysimilarapp-images"
```
- Ensure that you are using service account with proper principles. I used default App engine service account and added <i>Storage admin</i> principle. E.g. you can do this by following command
```shell
        gcloud projects add-iam-policy-binding ${PROJECT_ID} \
        --member serviceAccount:${PROJECT_ID}@appspot.gserviceaccount.com \
        --role roles/storage.admin
```
For lab purposes this approach is OK.
## Deployment
App can be deployed to Google App Engine. Standard enviroment is used by default. navigate to where app.yaml is located (<i>are-they-similar-app</i>) and execute command below
```shell
gcloud app deploy
```
