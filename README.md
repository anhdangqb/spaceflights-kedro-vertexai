# GCP-Kedro-spaceflight

## Customize for GCP

Configuration to run the kedro on GCP is specified in `GCP-Kedro-spaceflight/conf/gcp`.
Switching to run on GCP by specify the environment in Kedro CLI
```
kedro run --env=gcp
```


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

