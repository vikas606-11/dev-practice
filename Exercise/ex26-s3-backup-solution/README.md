# Exercise 01 - S3 Backup Solution

## Objective

Implement a backup strategy using Amazon S3 to store application files and configuration files. Demonstrate the restore process after simulating data loss.

---

## Services Used

* Amazon EC2
* Amazon S3
* AWS CLI
* IAM Role

---

## Architecture

```text
EC2 Instance
    │
    ├── Application Files
    ├── Configuration Files
    │
    ▼
Amazon S3 Bucket
    │
    ▼
Backup Storage
    │
    ▼
Restore Process
```

---

## Step 1: Create Application and Configuration Files

Create directories:

```bash
mkdir -p ~/backup-demo/application
mkdir -p ~/backup-demo/config
```

Create application files:

```bash
echo "Application Version 1.0" > ~/backup-demo/application/app.txt
echo "User Login Module" > ~/backup-demo/application/module.txt
echo "Application Log Data" > ~/backup-demo/application/log.txt
```

Create configuration files:

```bash
echo "DB_HOST=localhost" > ~/backup-demo/config/database.conf
echo "PORT=8080" > ~/backup-demo/config/app.conf
echo "ENV=production" > ~/backup-demo/config/env.conf
```

Verify:

```bash
tree ~/backup-demo
```

---

## Step 2: Verify AWS Access

Verify that the EC2 instance can access AWS services.

```bash
aws sts get-caller-identity
```

Expected Result:

```json
{
  "Account": "260969591589"
}
```

---

## Step 3: Create S3 Bucket

Create an S3 bucket to store backups.

```bash
aws s3 mb s3://backup-2026-001
```

Verify bucket creation:

```bash
aws s3 ls
```

---

## Step 4: Backup Application Files

Upload application files to S3.

```bash
aws s3 cp ~/backup-demo/application s3://backup-2026-001/application/ --recursive
```

---

## Step 5: Backup Configuration Files

Upload configuration files to S3.

```bash
aws s3 cp ~/backup-demo/config s3://backup-2026-001/config/ --recursive
```

---

## Step 6: Verify Backup

Verify that files exist in the S3 bucket.

```bash
aws s3 ls s3://backup-2026-001/application/ --recursive

aws s3 ls s3://backup-2026-001/config/ --recursive
```

---

## Step 7: Simulate Data Loss

Delete local files from the EC2 instance.

```bash
rm -rf ~/backup-demo/application
rm -rf ~/backup-demo/config
```

Verify deletion:

```bash
tree ~/backup-demo
```

Expected Output:

```text
0 directories, 0 files
```

---

## Step 8: Restore Application Files

Restore application files from S3.

```bash
aws s3 cp s3://backup-2026-001/application/ ~/backup-demo/application --recursive
```

---

## Step 9: Restore Configuration Files

Restore configuration files from S3.

```bash
aws s3 cp s3://backup-2026-001/config/ ~/backup-demo/config --recursive
```

---

## Step 10: Verify Restoration

Verify restored files:

```bash
tree ~/backup-demo
```

Expected Output:

```text
backup-demo
├── application
│   ├── app.txt
│   ├── log.txt
│   └── module.txt
└── config
    ├── app.conf
    ├── database.conf
    └── env.conf
```

Verify file contents:

```bash
cat ~/backup-demo/application/app.txt
cat ~/backup-demo/config/database.conf
```

---

## Results

* Successfully created application and configuration files.
* Created an Amazon S3 bucket for backup storage.
* Uploaded files to S3 using AWS CLI.
* Verified successful backup.
* Simulated data loss by deleting local files.
* Restored files from S3.
* Verified successful recovery of all files.

---

## Conclusion

Amazon S3 was used as a backup storage solution for application and configuration files. After simulating data loss, all files were successfully restored from S3, demonstrating a complete backup and recovery workflow.
