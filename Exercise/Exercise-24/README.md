# Exercise 24 – DynamoDB Application Deployment

## Objective

Deploy a Python application on Amazon EKS that securely accesses Amazon DynamoDB using **IAM Roles for Service Accounts (IRSA)**.

The application should perform basic CRUD operations on customer records without using AWS Access Keys.

---

# Requirements

The application must implement the following DynamoDB operations:

- Read Customer
- Write Customer
- Update Customer

---

# Constraints

- Do **not** use AWS Access Keys.
- Authentication must be performed using **IAM Roles for Service Accounts (IRSA)**.
- The application should obtain temporary AWS credentials from the assigned IAM Role.

---

# Project Structure

```
Exercise-24
│
├── README.md
│
└── dynamodb-app
    ├── app.py
    ├── Dockerfile
    ├── requirements.txt
    ├── deployment.yaml
    └── service.yaml
```

---

# Architecture

```
                Amazon EKS
                     │
                     ▼
              Python Application
                     │
                     ▼
                    Pod
                     │
                     ▼
        Kubernetes Service Account
                     │
                     ▼
          IAM Role (IRSA Authentication)
                     │
                     ▼
                IAM Policy
                     │
                     ▼
             Amazon DynamoDB
```

---

# Application Workflow

```
Client Request
      │
      ▼
Python Application
      │
      ├── Write Customer
      ├── Read Customer
      └── Update Customer
              │
              ▼
          Amazon DynamoDB
```

---

# DynamoDB Operations

## Write Customer

Creates a new customer record.

Example:

```text
Customer ID : 101
Name        : John Doe
Email       : john@example.com
```

---

## Read Customer

Retrieves customer details using the Customer ID.

Example:

```text
Customer ID : 101
```

Output:

```text
Name  : John Doe
Email : john@example.com
```

---

## Update Customer

Updates an existing customer record.

Example:

Before:

```text
Name : John Doe
```

After:

```text
Name : John Smith
```

---

# Security

The application **does not store AWS credentials**.

Authentication is handled through:

- Kubernetes Service Account
- IAM Role for Service Accounts (IRSA)
- Temporary AWS Security Credentials

This follows AWS security best practices and the Principle of Least Privilege.

---

# Deployment Steps

1. Build the Docker image.
2. Push the image to Amazon ECR.
3. Deploy the application to Amazon EKS.
4. Deploy the Kubernetes Service.
5. Verify the application can:
   - Write Customer
   - Read Customer
   - Update Customer
6. Confirm the application accesses DynamoDB using IRSA.

---

# Verification

Verify that the application can successfully perform:

- Write Customer
- Read Customer
- Update Customer

without configuring:

- AWS Access Key ID
- AWS Secret Access Key

The application should automatically receive temporary AWS credentials through the assigned IAM Role.

---

# Expected Outcome

The deployed application should:

- Successfully connect to Amazon DynamoDB.
- Perform customer data operations.
- Authenticate using IRSA.
- Operate without storing AWS Access Keys.
- Follow AWS security best practices.

---

# Skills Practiced

- Amazon EKS
- Amazon DynamoDB
- IAM Roles for Service Accounts (IRSA)
- Kubernetes Deployments
- Kubernetes Services
- Docker
- Amazon ECR
- Python
- Boto3
- Cloud Security
- Principle of Least Privilege

---

# Key Learning Outcomes

- Deploy applications on Amazon EKS.
- Integrate Amazon DynamoDB with Kubernetes workloads.
- Secure AWS access using IRSA.
- Understand how Pods authenticate to AWS services without long-lived credentials.
- Build secure cloud-native applications following AWS best practices.