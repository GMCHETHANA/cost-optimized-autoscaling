# Cost-Optimized Auto-Scaling Infrastructure

This project demonstrates a "cost-optimized auto-scaling infrastructure" locally using "Docker + Kubernetes (Kind)", simulating a real AWS architecture.

It showcases:

- Automatic scaling of applications based on "CPU and memory usage"
- Time-of-day scaling (simulate scale-down at night)
- Request-pattern simulation for load-based scaling
- Cost-threshold scaling using scheduled CronJobs
- Local simulation of AWS services:
  - Application Load Balancer → Kubernetes Ingress
  - Auto Scaling Group → Horizontal Pod Autoscaler (HPA)
  - EC2 instances → Pods
  - CloudWatch metrics → Metrics Server
  - Lambda functions → Kubernetes CronJobs


## Project Structure

cost-optimized-autoscaling/
├── app/
│ ├── app.py # Flask application
│ └── Dockerfile # Docker image for the app
├── k8s/
│ ├── deployment.yaml # Deployment manifest
│ ├── service.yaml # Service manifest
│ ├── ingress.yaml # Ingress (ALB simulation)
│ ├── hpa.yaml # Horizontal Pod Autoscaler (CPU + Memory)
│ ├── scale-down-cronjob.yaml # Time-of-day scaling (simulate Lambda)
│ └── cost-threshold-cronjob.yaml # Cost threshold scaling simulation
├── load-test.sh # Load test script for request-pattern scaling
├── components.yaml # Metrics server manifest
└── README.md # Project documentation

##  Prerequisites

- Docker
- Kind (Kubernetes in Docker)
- kubectl
- WSL or Linux/Mac terminal


##  Setup & Deployment

### 1. Clone the repository

git clone git@github.com:GMCHETHANA/cost-optimized-autoscaling.git
cd cost-optimized-autoscaling

## 2. Build Docker image
docker build -t autoscale-app:1.0 ./app
kind load docker-image autoscale-app:1.0 --name cost-optimized

## 3. Apply Kubernetes manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/scale-down-cronjob.yaml
kubectl apply -f k8s/cost-threshold-cronjob.yaml

## 4. Install Metrics Server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

## 5. Verify Deployment
kubectl get pods
kubectl get svc
kubectl get hpa -w
kubectl get cronjob

## Test Load / Auto-Scaling

# CPU Load Simulation
kubectl exec -it <pod-name> -- /bin/sh
apt update && apt install -y stress
stress --cpu 1 --timeout 60

# Request-Pattern Simulation
chmod +x load-test.sh
./load-test.sh
kubectl get hpa -w
kubectl get pods -w

## Access Application

# Port-forward Ingress
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80

# Visit
http://localhost:8080/

## Features Implemented
Feature	-> Implementation
CPU-based auto-scaling ->	HPA metrics
Memory-based auto-scaling ->	HPA metrics
Request-pattern scaling	-> load-test.sh script
Time-of-day scale-down	-> CronJob scale-down-cronjob.yaml
Cost-threshold scale-down-> 	CronJob cost-threshold-cronjob.yaml
ALB Simulation ->	Kubernetes Ingress
EC2 Simulation -> Pods
CloudWatch Simulation ->	Metrics Server
Lambda Simulation	-> CronJobs

