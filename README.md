# **SRE Project – Kubernetes Microservices Platform**

This project demonstrates the design, deployment, monitoring, and failure-handling of a microservices architecture on Kubernetes.  
The system consists of **three web services** (API, Auth, Images) written in **Node.js, Go, and Python**, deployed with full SRE best practices: reliability, observability, auto-scaling, security, and failure simulation.

----------

## **1. System Architecture**

### **Architecture Diagram**


[Open Diagram on Google Drive](https://drive.google.com/file/d/1CW-SJqZd5VdvCVCTrUlVmwjezJGxqkDb/view?usp=sharing)
### **Architecture Summary**

-   Three microservices deployed inside a dedicated namespace **app**.
    
-   Each service has its own Deployment and Service (ClusterIP).
    
-   External access is provided via **Ingress + TLS**.
    
-   Shared resources:
    
    -   **PostgreSQL database** (optional simulation)
        
    -   **Object storage (S3-like)** for images.
        
-   Isolation implemented with:
    
    -   **Namespaces**
        
    -   **Network Policies**
        
-   Sensitive data stored using **Kubernetes Secrets**.
    
-   Full monitoring stack in namespace **monitoring**:
    
    -   Prometheus
        
    -   Grafana
        
    -   Alertmanager (Slack notifications enabled)
        

----------

## **2. Building & Deploying Services**

### **2.1 Dockerfiles**

Each service contains its own Dockerfile:

-   API → Node.js
    
-   Auth → Go
    
-   Images → Python (FastAPI)
    

Example tasks performed:

-   Installed dependencies
    
-   Exposed service port
    
-   Set entrypoint command
    

### **2.2 Building Docker Images**

`docker build -t ghcr.io/<username>/api-service:latest api/
docker build -t ghcr.io/<username>/auth-service:latest auth/
docker build -t ghcr.io/<username>/images-service:latest images/` 

### **2.3 Pushing Images to GHCR**

`echo <TOKEN> | docker login ghcr.io -u <username> --password-stdin docker push ghcr.io/<username>/api-service:latest
docker push ghcr.io/<username>/auth-service:latest
docker push ghcr.io/<username>/images-service:latest` 

### **2.4 Deploying to Kubernetes**

`kubectl apply -f k8s/namespaces.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/ingress.yaml` 

----------

## **3. Security & Networking**

### **3.1 Network Policies**

-   Block cross-service communication except required paths.
    
-   Allow ingress only through Ingress Controller.
    
-   Deny all traffic by default inside namespace.
    

### **3.2 Secrets Management**

Stored in:

`k8s/secrets.yaml` 

Contains:

-   JWT secret
    
-   Database URL
    
-   API keys (sanitized — no real secrets committed)
    

### **3.3 TLS Configuration**

-   Self-signed certificate stored in secret `app-tls`
    
-   Applied automatically via Ingress
    

----------

## **4. Observability & Alerting**

### **4.1 Monitoring Stack**

Installed using Kubernetes manifests:

-   Prometheus
    
-   Grafana
    
-   Alertmanager
    

### **4.2 Custom Metrics**

-   Pod failures
    
-   Probe failures
    
-   Resource usage
    

### **4.3 Slack Alerts**

Alertmanager was configured with:

`slack_api_url:  "<your webhook URL>"  channel:  "#all-sre-project"` 

### **4.4 Dashboards**

Grafana dashboards include:

-   API latency, traffic, and error rates
    
-   Pod restarts & HPA scaling events
    
-   System-wide health panel
    

----------

## **5. Reliability & Auto-Scaling**

### **5.1 Horizontal Pod Autoscaling (HPA)**

Enabled for all services:

`kubectl apply -f k8s/hpa/` 

Triggers:

-   CPU > 50%
    
-   Memory usage (optional)
    
-   Request rate (optional)
    

### **5.2 Liveness & Readiness Probes**

Configured for each service to prevent serving bad pods.

### **5.3 PodDisruptionBudget**

Ensures at least 1 replica stays running during updates.

----------

## **6. Failure Simulation & Recovery Testing**

The following failure scenarios were performed:

### **6.1 Secret Deletion**

`kubectl delete secret app-secrets -n app` 

**Expected behavior:**

-   Pods restart and fail due to missing env vars
    
-   Prometheus records probe failures
    
-   Slack alert triggers
    

### **6.2 Pod Deletion**

`kubectl delete pod <pod-name> -n app` 

**Expected behavior:**

-   Kubernetes instantly schedules a replacement pod
    
-   Zero downtime if replicas >= 2
    

### **6.3 Probe Failure Simulation**

Example: breaking a readiness endpoint  
**Expected behavior:**

-   Pod marked Unready
    
-   Removed from Service
    
-   Alert created
    

Each scenario includes:

-   Logs
    
-   Events
    
-   Prometheus queries
    
-   Alerts (Slack)
    

----------

## **7. How to Reproduce This Environment**

### **7.1 Requirements**

-   Docker Desktop (with Kubernetes enabled)
    
-   kubectl
    
-   Git
    
-   GHCR PAT token
    
-   VSCode
    

### **7.2 Setup Steps**

`git clone https://github.com/<username>/SRE-Project.git cd SRE-Project

kubectl apply -f k8s/namespaces.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa/
kubectl apply -f k8s/monitoring/` 

### **7.3 Access Tools**

Grafana:

`localhost:3000` 

Prometheus:

`localhost:9090` 

Application:

`https://localhost/` 

----------

## **8. Lessons Learned**

-   Kubernetes handles failovers automatically with minimal manual intervention.
    
-   Proper probes and HPA rules prevent service outages.
    
-   Slack alerts provide real-time visibility into system failures.
    
-   Secrets must _never_ be committed (GitHub will block them).
    
-   Network Policies significantly increase cluster security.
    
-   Monitoring stack is essential to validating SRE best practices.
    

----------

## **9. Future Improvements**

-   Add CI/CD pipeline for automated deployments
    
-   Implement service mesh (Istio/Linkerd)
    
-   Add distributed tracing (Jaeger/Tempo)
    
-   Add chaos engineering automation (Litmus or ChaosMesh)
