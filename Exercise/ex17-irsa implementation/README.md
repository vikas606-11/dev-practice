# Exercise 17 – Implement IRSA for Application Access

## Objective

Allow a Kubernetes application running on Amazon EKS to access DynamoDB without storing AWS Access Keys.

## Components

- IAM Policy
- IAM Role
- OIDC Provider
- Kubernetes Service Account
- Python Application
- DynamoDB

## Workflow

Python Pod

↓

Service Account

↓

OIDC Provider

↓

IAM Role

↓

IAM Policy

↓

DynamoDB

## DynamoDB Operations

- PutItem
- GetItem
- UpdateItem

## Benefits

- No AWS Access Keys stored in the application.
- Temporary credentials provided automatically.
- Least privilege access.
- Secure authentication using IAM Roles for Service Accounts (IRSA).