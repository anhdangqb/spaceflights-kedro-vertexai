# GCP-Kedro-spaceflight

## Containerize Kedro project

1. Build Kedro project container
```
docker build \
 -t gcr.io/$PROJECT_ID/$GCR_REPO_NAME:latest \
 .
```
2. Test the container locally (Vertex notebook)
```
docker run gcr.io/$PROJECT_ID/$GCR_REPO_NAME:latest
```

3. Push to gcr.io (or Artifact Registry)
```
docker push gcr.io/$PROJECT_ID/$GCR_REPO_NAME:latest
```

## Run Vertex job on custom container

This is by Python SDK of `google-cloud-aiplatform` (CLI also available). 
Run on Vertex workbench:

1. Init Vertex client
```
aiplatform.init(project=PROJECT_ID, staging_bucket=BUCKET_URI)
```

2. Create Vertex job
```
job = aiplatform.CustomContainerTrainingJob(
    display_name="trial1_kedro_iris_job",
    container_uri=CONTAINER_URI,
)

print(job)
```

3. Run job
```
model = job.run(
    replica_count=REPLICA_COUNT,
    machine_type=MACHINE_TYPE
)
```

