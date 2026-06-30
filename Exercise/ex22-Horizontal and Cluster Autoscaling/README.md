# Exercise 26 – Automatic Scaling on Amazon EKS

## Objective

Implement automatic scaling for applications running on Amazon EKS.

The exercise demonstrates how Kubernetes automatically scales Pods using the Horizontal Pod Autoscaler (HPA) and how the Cluster Autoscaler provisions additional worker nodes when existing nodes cannot schedule new Pods.

---

# Requirements

Implement:

- Horizontal Pod Autoscaler (HPA)
- Cluster Autoscaler

Perform load testing using:

- hey
- Apache Bench (ab)
- k6

---

# Expected Outcome

Horizontal Pod Autoscaler

```
Pods

2  →  20
```

Cluster Autoscaler

```
Worker Nodes

3  →  6
```

---

# Architecture

```
                   Client
                      │
                      ▼
               Load Testing Tool
      (hey / Apache Bench / k6)
                      │
                      ▼
                Kubernetes Service
                      │
                      ▼
                 Application Pods
                      │
          ------------------------
          │                      │
          ▼                      ▼
 Horizontal Pod Autoscaler   Metrics Server
          │
          ▼
 Increase / Decrease Pods
          │
          ▼
   Cluster Autoscaler
          │
          ▼
 Increase / Decrease Worker Nodes
```

---

# Project Structure

```
Exercise-26
│
├── README.md
│
├── kubernetes
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   └── metrics-server.yaml
│
├── autoscaler
│   ├── cluster-autoscaler.yaml
│   ├── cluster-autoscaler-policy.json
│   └── cluster-autoscaler-role.yaml
│
├── load-test
│   ├── hey.sh
│   ├── ab.sh
│   └── k6-script.js
│
└── screenshots
```

---

# Components

## Deployment

Deploys the sample application into the Kubernetes cluster.

---

## Service

Exposes the application within the Kubernetes cluster.

---

## Metrics Server

Collects CPU and memory metrics from Kubernetes Nodes and Pods.

These metrics are required by the Horizontal Pod Autoscaler.

---

## Horizontal Pod Autoscaler (HPA)

Automatically adjusts the number of application Pods based on CPU utilization.

Example:

```
Minimum Pods : 2

Maximum Pods : 20

Target CPU Utilization : 70%
```

---

## Cluster Autoscaler

Automatically increases or decreases the number of worker nodes.

Example:

```
Minimum Nodes : 3

Maximum Nodes : 6
```

---

# Load Testing

## hey

Example:

```bash
hey -n 100000 -c 200 http://<LoadBalancer-IP>
```

---

## Apache Bench

Example:

```bash
ab -n 100000 -c 200 http://<LoadBalancer-IP>/
```

---

## k6

Example:

```bash
k6 run k6-script.js
```

---

# Scaling Workflow

```
User Traffic
      │
      ▼
Application CPU Usage Increases
      │
      ▼
Metrics Server Collects Metrics
      │
      ▼
Horizontal Pod Autoscaler
      │
      ▼
Creates Additional Pods
      │
      ▼
Worker Nodes Become Full
      │
      ▼
Cluster Autoscaler
      │
      ▼
Launches Additional EC2 Worker Nodes
```

---

# Verification

Verify HPA

```bash
kubectl get hpa
```

Verify Pods

```bash
kubectl get pods
```

Verify Nodes

```bash
kubectl get nodes
```

Monitor Scaling

```bash
watch kubectl get hpa,pods,nodes
```

---

# Expected Results

Before Load Test

```
Pods : 2

Nodes : 3
```

During Load Test

```
Pods : 20

Nodes : 6
```

After Load Test

```
Pods decrease automatically

Unused nodes are removed automatically
```

---

# Learning Outcomes

- Understand Horizontal Pod Autoscaler (HPA)
- Configure Kubernetes autoscaling
- Configure Cluster Autoscaler
- Deploy Metrics Server
- Generate load using hey, Apache Bench, and k6
- Monitor Kubernetes scaling events
- Understand automatic node provisioning in Amazon EKS

---

# Skills Practiced

- Amazon EKS
- Kubernetes
- Horizontal Pod Autoscaler
- Cluster Autoscaler
- Metrics Server
- Docker
- Load Testing
- hey
- Apache Bench
- k6
- Kubernetes Monitoring