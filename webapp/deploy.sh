#!/bin/bash
# Execute this script from the root of this repo.

cp ./notebooks/output/raw_councillor_df.csv ./webapp/

# See: https://cloud.google.com/sdk/gcloud/reference/run/deploy
gcloud run deploy toronto-councillor-clustering-p \
    --allow-unauthenticated \
    --cpu-throttling \
    --cpu 1 \
    --memory 1Gi \
    --source webapp \
    --max-instances 2 \
    --region us-east1

rm ./webapp/raw_councillor_df.csv
