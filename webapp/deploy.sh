#!/bin/bash

cp ./notebooks/output/plotly_df.csv ./webapp/

# See: https://cloud.google.com/sdk/gcloud/reference/run/deploy
gcloud run deploy toronto-councillor-clustering-p \
    --allow-unauthenticated \
    --cpu-throttling \
    --cpu 1 \
    --memory 1Gi \
    --source webapp \
    --max-instances 2

rm ./webapp/plotly_df.csv
