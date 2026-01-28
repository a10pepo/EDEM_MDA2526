project_id = "e2e-gemma-balaguer"
region     = "europe-west1"
zone       = "europe-west1-b"
subnetwork = "projects/e2e-gemma-balaguer/regions/europe-west1/subnetworks/default"
service_account_email = "667771392106-compute@developer.gserviceaccount.com"
 metabase como lo he hecjho yo 
gcloud iam service-accounts create metabase-sa \
  --display-name="Metabase BigQuery"

gcloud projects add-iam-policy-binding e2e-gemma-balaguer \
  --member="serviceAccount:metabase-sa@e2e-gemma-balaguer.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding e2e-gemma-balaguer \
  --member="serviceAccount:metabase-sa@e2e-gemma-balaguer.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

gcloud run deploy metabase \
  --image=metabase/metabase:latest \
  --platform=managed \
  --region=europe-west1 \
  --allow-unauthenticated \
  --service-account=metabase-sa@e2e-gemma-balaguer.iam.gserviceaccount.com \
  --memory=2Gi \
  --port=3000
