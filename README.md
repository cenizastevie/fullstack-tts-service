# Fullstack TTS Service

This repository contains a full-stack application with a **FastAPI backend** for text-to-speech (TTS) and an **Angular frontend**. The application is containerized using **Docker** and deployed on **AWS ECS**, with **API Gateway** providing access to the backend. The infrastructure is managed using **AWS CloudFormation** to ensure scalable deployment and automation of resources.

## Running the Backend

To run the FastAPI backend locally, use the following command:

```bash
uvicorn main:app --reload


## Running the Localstack

To run localstack, use the following command:

```bash
docker run -d -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack


### Installing terraform

```bash
terraform init

## LocalStack S3 Commands

### Planning terraform in dev mode
```bash
terraform plan -var-file="dev.tfvars"

### Applying changes in dev mode
```bash
terraform apply -var-file="dev.tfvars"   


