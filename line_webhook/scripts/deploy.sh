source ./scripts/init.sh

gcloud config set account "punsiri.boo@gmail.com"
echo "GCP Project ID: $PROJECT_ID"
echo "Function Name: $FUNCTION_NAME"
echo "Entry Point: $ENTRY_POINT"

gcloud config set project $PROJECT_ID

gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --trigger-http \
    --region=asia-southeast1 \
    --runtime=python311 \
    --source=. \
    --entry-point=$ENTRY_POINT \
    --env-vars-file=privates/line_secret.yml \
    --memory=1GB \
    --timeout=150s 
