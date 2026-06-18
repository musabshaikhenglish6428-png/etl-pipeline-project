# Setup Guide

## Prerequisites

- Docker
- Docker Compose
- Git

## Clone Repository

git clone <repo-url>

cd etl-pipeline-project

## Create Environment File

cp .env.example .env

## Start Application

docker-compose up --build

## Verify Logs

cat logs/pipeline.log

## Stop Application

docker-compose down