# Kubernetes Deployment Guide (AWS EKS and Azure AKS)

This folder contains Kubernetes manifests for the CPU workload service:

- `deployment.yaml`: app Deployment
- `service.yaml`: ClusterIP/Service exposure
- `hpa.yaml`: Horizontal Pod Autoscaler

## What Is Used

- Container image: `saas-matrix-project:latest`
- Kubernetes manifests from this folder
- `kubectl` to apply and manage resources
- AWS path:
  - Amazon EKS (cluster)
  - Amazon ECR (container registry)
  - `eksctl` + `aws` CLI
- Azure path:
  - Azure AKS (cluster)
  - Azure ACR (container registry)
  - `az` CLI

## Prerequisites

- Docker installed and running
- `kubectl` installed
- AWS CLI + `eksctl` configured (for AWS flow)
- Azure CLI configured (for Azure flow)

---

## AWS Deployment (EKS) Step by Step

### 1) Create ECR repository

```powershell
$REPO_NAME = "saas-matrix-project"
$AWS_REGION = "eu-central-1"
aws ecr create-repository --repository-name $REPO_NAME --region $AWS_REGION
```

### 2) Create EKS cluster

```powershell
eksctl create cluster --name saas-project --region eu-central-1 --nodes 3 --node-type m7i-flex.large --managed
```

### 3) Build, tag, and push Docker image to ECR

```powershell
docker build -t saas-matrix-project:latest ..
docker tag saas-matrix-project:latest 457090734537.dkr.ecr.eu-central-1.amazonaws.com/saas-matrix-project:latest
docker push 457090734537.dkr.ecr.eu-central-1.amazonaws.com/saas-matrix-project:latest
```

### 4) Switch to EKS context

```powershell
kubectl config get-contexts
kubectl config rename-context saas-user@saas-project.eu-central-1.eksctl.io eks-prod
kubectl config use-context eks-prod
```

### 5) Deploy Kubernetes manifests

```powershell
kubectl apply -f .
```

### 6) Validate deployment and autoscaling

```powershell
kubectl get nodes
kubectl get pods -w
kubectl get hpa -w
while ($true) { kubectl top pods; Start-Sleep 2; Clear-Host }
```

### 7) Cleanup (optional)

```powershell
eksctl delete cluster --name saas-project --region eu-central-1
```

---

## Azure Deployment (AKS) Step by Step

### 1) Create resource group and ACR

```powershell
az group create --name saas-project-rg --location polandcentral
az acr create --resource-group saas-project-rg --name saasprojectregistry --sku Basic
```

### 2) Create AKS cluster

```powershell
az aks create --resource-group saas-project-rg --name saas-project --node-count 3 --node-vm-size Standard_B2s_v2 --location polandcentral --tier free --generate-ssh-keys
```

### 3) Login to Azure and ACR

```powershell
az login
az acr login --name saasprojectregistry
```

### 4) Build, tag, and push Docker image to ACR

```powershell
docker build -t saas-matrix-project:latest ..
docker tag saas-matrix-project:latest saasprojectregistry.azurecr.io/saas-matrix-project:latest
docker push saasprojectregistry.azurecr.io/saas-matrix-project:latest
```

### 5) Attach ACR to AKS

```powershell
az aks update --resource-group saas-project-rg --name saas-project --attach-acr saasprojectregistry
az aks check-acr --resource-group saas-project-rg --name saas-project --acr saasprojectregistry.azurecr.io
```

### 6) Switch to AKS context

```powershell
kubectl config get-contexts
kubectl config rename-context saas-project aks-prod
kubectl config use-context aks-prod
```

### 7) Deploy Kubernetes manifests

```powershell
kubectl apply -f .
```

### 8) Validate deployment and autoscaling

```powershell
kubectl get nodes
kubectl get pods -w
kubectl get hpa -w
while ($true) { kubectl top pods; Start-Sleep 2; Clear-Host }
```

### 9) Cleanup (optional)

```powershell
az group delete --name saas-project-rg --yes --no-wait
az group list -o table
```

---

## Notes

- Make sure `deployment.yaml` image points to the correct registry (ECR for AWS, ACR for Azure).
- From this folder, `kubectl apply -f .` applies Deployment, Service, and HPA together.
