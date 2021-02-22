# atmosphere-transformer-base

Folder containing the base code to implement a transformer.
It contains useful code that we require each time we need a transformer.

## Dockerfile

```dockerfile
###################
# Transformer image
###################

FROM python:3.8.5-slim AS transformer

RUN apt-get update && apt-get install -y git 
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

## Install requirements
COPY requirements.txt /app/requirements.txt
RUN --mount=type=ssh pip install --no-cache-dir -r /app/requirements.txt --upgrade

COPY {ROOT_FOLDER}/ /app/{ROOT_FOLDER}/

WORKDIR /app

EXPOSE 5000

ENV API_TYPE REST
ENV SERVICE_TYPE TRANSFORMER
ENV PERSISTENCE 0

CMD seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE
```


Example:
```
class XGBoostInputTransformer(FeatureTransformer):

    def apply_transformation(self, msg):
        # transform data here
        return numpy_array
```

The pip command is:
```shell script
pip install git+https://github.com/ambiata/atmosphere-python-sdk.git@{tag}
```

## Docker Build
```bash
DOCKER_BUILDKIT=1 docker build -f Dockerfile --ssh default --target transformer -t {sample_tag} .
```

## Docker Run
```bash
docker run --env MODEL_NAME="{my_custom_repo_here}.transformers.xgboost_input_transformer.XGBoostInputTransformer" -p 5000:5000 {sample_tag} 
```

## Seldon Graph
(To add)

Remember to set the env var
`MODEL_NAME` to your transformer module file / class

## Tests
```shell script
./test-script.sh
```
