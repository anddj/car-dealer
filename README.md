# Serverless REST API

This application demonstrates usage of serverless to implement RESTful API.
The CRUD operations will be performed on cars list.

## Setup

```bash
npm install
```

## Deploy

In order to deploy the endpoint simply run

```bash
serverless deploy --region eu-central-1 --stage dev
```

The expected result should be similar to:
```bash
Serverless: Parsing Python requirements.txt
Serverless: Installing required Python packages for runtime python2.7...
Serverless: Linking required Python packages...
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Unlinking required Python packages...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service .zip file to S3 (8.75 MB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
......................................................................................................
Serverless: Stack update finished...
Service Information
service: serverless-rest-api-with-pynamodb
stage: dev
region: eu-central-1
stack: serverless-rest-api-with-pynamodb-dev
api keys:
  None
endpoints:
  POST - https://qfsxuwpr26.execute-api.eu-central-1.amazonaws.com/dev/cars
  GET - https://qfsxuwpr26.execute-api.eu-central-1.amazonaws.com/dev/cars
  GET - https://qfsxuwpr26.execute-api.eu-central-1.amazonaws.com/dev/cars/{car_id}
  PUT - https://qfsxuwpr26.execute-api.eu-central-1.amazonaws.com/dev/cars/{car_id}
  DELETE - https://qfsxuwpr26.execute-api.eu-central-1.amazonaws.com/dev/cars/{car_id}
```

## Usage

You can create, retrieve, update, or delete cars with the following commands:

### Create a Car

```bash
curl -X POST https://XXXXXXX.execute-api.eu-central-1.amazonaws.com/dev/cars --data @example_car.json
```

### List all Cars

```bash
curl https://XXXXXXX.execute-api.eu-central-1.amazonaws.com/dev/cars
```

### Get one Car

```bash
# Replace the <id> part with a real id from your cars table
curl https://XXXXXXX.execute-api.eu-central-1.amazonaws.com/dev/cars/<id>
```

### Update a Car

```bash
# Replace the <id> part with a real id from your cars table
curl -X PUT https://XXXXXXX.execute-api.eu-central-1.amazonaws.com/dev/cars/<id> --data @example_car.json
```

### Delete a Car

```bash
# Replace the <id> part with a real id from your cars table
curl -X DELETE https://XXXXXXX.execute-api.eu-central-1.amazonaws.com/dev/cars/<id>
```
