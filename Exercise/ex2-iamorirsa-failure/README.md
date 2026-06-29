# Exercise 2 – IAM / IRSA Failure Troubleshooting

## Objective

Troubleshoot an application running on Amazon EKS that is unable to access Amazon DynamoDB using IAM Roles for Service Accounts (IRSA).

---

# Incident

The application suddenly cannot read data from DynamoDB.

### Application Logs

```text
2026-05-10T08:12:13Z ERROR

botocore.exceptions.ClientError:

An error occurred (AccessDeniedException)

when calling the GetItem operation:

User:
arn:aws:sts::123456789012:assumed-role/eks-nodegroup-role

is not authorized to perform:

dynamodb:GetItem

on resource:

arn:aws:dynamodb:ap-south-1:123456789012:table/customer-data
```

---

# Current Architecture

```
Python Application
        │
        ▼
      Pod
        │
        ▼
Service Account
        │
        ▼
IAM Role (IRSA)
        │
        ▼
IAM Policy
        │
        ▼
Amazon DynamoDB
```

---

# Problem Analysis

The application is expected to use the IAM Role associated with the Kubernetes Service Account through IRSA.

Instead, it is using the Worker Node IAM Role.

Current Identity:

```
eks-nodegroup-role
```

Expected Identity:

```
dynamodb-irsa-role
```

This indicates that IRSA authentication is not working.

---

# Possible Causes

## 1. Wrong Service Account

The Deployment is using the default Service Account instead of the IRSA-enabled Service Account.

Incorrect:

```yaml
serviceAccountName: default
```

Correct:

```yaml
serviceAccountName: dynamodb-sa
```

---

## 2. Missing IAM Role Annotation

The Service Account is missing the IAM Role annotation.

```yaml
annotations:
  eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/dynamodb-irsa-role
```

Without this annotation, the Pod cannot assume the IAM Role.

---

## 3. OIDC Provider Not Configured

The EKS cluster is not associated with an IAM OIDC Provider.

Without an OIDC Provider, IRSA authentication cannot occur.

---

## 4. Incorrect IAM Trust Policy

The IAM Role Trust Policy does not trust the correct Kubernetes Service Account.

Expected subject:

```
system:serviceaccount:default:dynamodb-sa
```

---

## 5. Incorrect IAM Policy

The IAM Policy does not allow:

- dynamodb:GetItem
- dynamodb:PutItem
- dynamodb:UpdateItem

---

## 6. Pod Using Cached Credentials

The Pod was started before IRSA configuration was updated.

Restarting the Pod allows it to obtain fresh temporary credentials.

---

# Troubleshooting Steps

---

## Step 1 – Verify the Pod Identity

Run:

```bash
kubectl exec -it <pod-name> -- aws sts get-caller-identity
```

If the output shows:

```text
arn:aws:sts::<ACCOUNT_ID>:assumed-role/eks-nodegroup-role
```

the Pod is using the Worker Node IAM Role.

---

## Step 2 – Verify the Deployment

Check the Deployment:

```bash
kubectl describe deployment <deployment-name>
```

Verify:

```yaml
serviceAccountName: dynamodb-sa
```

If it is set to `default`, update the Deployment.

Apply the changes:

```bash
kubectl apply -f deployment.yaml
```

---

## Step 3 – Verify the Service Account

Describe the Service Account:

```bash
kubectl describe serviceaccount dynamodb-sa
```

Verify the annotation:

```yaml
annotations:
  eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/dynamodb-irsa-role
```

If missing, update the Service Account.

Apply the configuration:

```bash
kubectl apply -f serviceaccount.yaml
```

---

## Step 4 – Verify the OIDC Provider

Check the EKS cluster:

```bash
aws eks describe-cluster \
--name <cluster-name> \
--region <region>
```

Look for:

```
identity
 └── oidc
```

If the OIDC Provider is missing, associate it:

```bash
eksctl utils associate-iam-oidc-provider \
--cluster <cluster-name> \
--region <region> \
--approve
```

---

## Step 5 – Verify the IAM Trust Policy

Retrieve the IAM Role:

```bash
aws iam get-role \
--role-name dynamodb-irsa-role
```

Verify the Trust Policy contains:

```text
system:serviceaccount:default:dynamodb-sa
```

If incorrect, update the Trust Policy.

---

## Step 6 – Verify the IAM Policy

List the attached policies:

```bash
aws iam list-attached-role-policies \
--role-name dynamodb-irsa-role
```

Verify the IAM Policy contains:

```json
"Action": [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem"
]
```

If the required permissions are missing, attach the correct IAM Policy.

---

## Step 7 – Restart the Application

Restart the Deployment:

```bash
kubectl rollout restart deployment <deployment-name>
```

This ensures the Pod receives fresh temporary credentials.

---

# Verification

### Verify the Pod Identity

```bash
kubectl exec -it <pod-name> -- aws sts get-caller-identity
```

Expected:

```text
arn:aws:sts::<ACCOUNT_ID>:assumed-role/dynamodb-irsa-role
```

---

### Verify DynamoDB Access

The application should now successfully perform:

- GetItem
- PutItem
- UpdateItem

without using AWS Access Keys.

---

# Root Cause

The Pod failed to assume the IAM Role through IRSA.

Because IRSA authentication failed, the AWS SDK automatically used the Worker Node IAM Role.

The Worker Node IAM Role does not have permission to access the DynamoDB table, resulting in an **AccessDeniedException**.

---

# Resolution

- Configure the correct Kubernetes Service Account.
- Annotate the Service Account with the IRSA IAM Role.
- Verify the IAM OIDC Provider.
- Verify the IAM Trust Policy.
- Verify the IAM Policy permissions.
- Restart the application Pods.

---

# Skills Practiced

- Amazon EKS
- Kubernetes
- IAM Roles
- IAM Policies
- IAM Roles for Service Accounts (IRSA)
- OIDC Provider
- Amazon DynamoDB
- AWS CLI
- Kubernetes Troubleshooting
- Cloud Security
- Principle of Least Privilege

---

# Key Learning Outcomes

- Understand how IRSA provides AWS credentials to Pods.
- Identify when a Pod is using the Worker Node IAM Role.
- Troubleshoot IRSA authentication failures.
- Verify Service Accounts, IAM Roles, OIDC Providers, and Trust Policies.
- Securely access AWS services without storing AWS Access Keys.