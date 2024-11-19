# Fullstack TTS Service

This repository contains a full-stack application with a **FastAPI backend** for text-to-speech (TTS) and an **Angular frontend**. The application is containerized using **Docker** and deployed on **AWS ECS**, with **API Gateway** providing access to the backend. The infrastructure is managed using **AWS CloudFormation** to ensure scalable deployment and automation of resources.

## Running the Backend

To run the FastAPI backend locally, use the following command:

```bash
uvicorn main:app --reload
```

## Running the Localstack

To run localstack, use the following command:

```bash
docker run -d -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
```

### Installing terraform

```bash
terraform init
```
## LocalStack S3 Commands

### Planning terraform in dev mode
```bash
terraform plan -var-file="dev.tfvars"
```

### Applying changes in dev mode
```bash
terraform apply -var-file="dev.tfvars"   
```
### Running unit tests
```
docker-compose run test
```
### Change directory first to use terraform ex:
```bash
cd terraform/dev
```

### Terraform commands dev
```bash
set AWS_ACCESS_KEY_ID=test
set AWS_SECRET_ACCESS_KEY=test
set AWS_DEFAULT_REGION=us-east-1
set AWS_ENDPOINT_URL=http://localhost:4566
``` 
```bash
terraform init
terraform plan
terraform apply
terraform destroy
```

### Terraform commands staging
```bash
terraform init -var-file="staging.tfvars"
terraform plan -var-file="staging.tfvars"
terraform apply -var-file="staging.tfvars"
terraform destroy -var-file="staging.tfvars"
```

### Alembic commands
```bash
alembic init alembic
alembic revision --autogenerate -m "[MEssage]"
alembic upgrade head
alembic history
alembic downgrade -1
```

### Check localstack buckets
```bash
aws --endpoint-url=http://localhost:4566 s3 ls
```

### Bash not running container
```bash
docker-compose run test /bin/bash
```