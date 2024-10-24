# Fullstack TTS Service

This repository contains a full-stack application with a **FastAPI backend** for text-to-speech (TTS) and an **Angular frontend**. The application is containerized using **Docker** and deployed on **AWS ECS**, with **API Gateway** providing access to the backend. The infrastructure is managed using **AWS CloudFormation** to ensure scalable deployment and automation of resources.

## Running the Backend

To run the FastAPI backend locally, use the following command:

```bash
uvicorn main:app --reload
