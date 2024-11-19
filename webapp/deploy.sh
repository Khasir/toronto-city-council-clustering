#!/bin/bash
# Execute this script from the root of this repo.

if [ -d ./webapp/.cache ]; then
    rm -r ./webapp/.cache
fi
if [ -d ./webapp/__pycache__ ]; then
    rm -r ./webapp/__pycache__
fi

if [ ! -f ./webapp/raw_councillor_df.csv ]; then
    echo "File not found: ./webapp/raw_councillor_df.csv"
    echo "Run: python -m scripts.regenerate_dataframe "
    exit 1
fi

# See: https://cloud.google.com/sdk/gcloud/reference/run/deploy
# use --cpu-throttling to save cost
gcloud run deploy toronto-councillor-clustering-p \
    --allow-unauthenticated \
    --cpu 1 \
    --memory 1Gi \
    --source webapp \
    --min-instances 1 \
    --max-instances 5 \
    --region us-east1

