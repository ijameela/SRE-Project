graph TD

%% =================== CLIENT & INGRESS ===================
subgraph Client[User Browser]
end

subgraph IngressLayer[NGINX Ingress Controller]
    Client -->|HTTPS| Ingress
end


%% =================== APPLICATION NAMESPACE ===================
subgraph AppNS[Namespace: app]

    %% -------- Deployments ----------
    API[API Service (FastAPI/Python)]
    AUTH[Auth Service (Node.js)]
    IMAGES[Images Service (Go)]

    %% -------- Services ----------
    API_SVC[Service: api-service (ClusterIP)]
    AUTH_SVC[Service: auth-service (ClusterIP)]
    IMG_SVC[Service: images-service (ClusterIP)]

    %% ----- HPA -----
    API_HPA[HPA for API Service]
    AUTH_HPA[HPA for Auth Service]
    IMG_HPA[HPA for Images Service]

    %% ----- Probes -----
    API_PROBE[(Liveness/Readiness Probes)]
    AUTH_PROBE[(Probes)]
    IMG_PROBE[(Probes)]

    %% ----- Pod Disruption Budget -----
    API_PDB[(PDB API)]
    AUTH_PDB[(PDB Auth)]
    IMG_PDB[(PDB Images)]

end


%% =================== NETWORK POLICIES ===================
subgraph NetPol[Network Policies]
    NP1[Only API can call AUTH]
    NP2[Only API can call IMAGES]
    NP3[Deny all cross-namespace traffic]
end


%% =================== DATABASE ===================
subgraph DBNS[Namespace: database]
    DB[(PostgreSQL Database)]
    DB_SECRET[(DB Credentials Secret)]
end


%% =================== STORAGE ===================
subgraph StorageNS[Namespace: storage]
    S3[(Object Storage – S3 or MinIO)]
    S3_SECRET[(S3 Access Keys)]
end


%% =================== MONITORING ===================
subgraph MonitoringNS[Namespace: monitoring]
    PROM[Prometheus]
    GRAF[Grafana Dashboard]
    ALERT[Alertmanager]
    EXPORTERS[Custom Metrics Exporters]
end


%% =================== INGRESS ROUTES ===================
Ingress -->|api.localhost| API_SVC
Ingress -->|auth.localhost| AUTH_SVC
Ingress -->|images.localhost| IMG_SVC


%% =================== SERVICE CONNECTIONS ===================
%% API CALLS
API -->|calls| AUTH_SVC
API -->|calls| IMG_SVC

%% Images Service -> Storage
IMAGES -->|read/write| S3

%% API -> Database
API -->|queries| DB


%% =================== SECRETS ===================
API --> DB_SECRET
AUTH --> S3_SECRET
IMAGES --> S3_SECRET

%% =================== MONITORING ===================
API --> EXPORTERS
AUTH --> EXPORTERS
IMAGES --> EXPORTERS
EXPORTERS --> PROM
PROM --> ALERT
PROM --> GRAF

%% =================== HPA LINKS ===================
API --> API_HPA
AUTH --> AUTH_HPA
IMAGES --> IMG_HPA

%% =================== PROBES ===================
API --> API_PROBE
AUTH --> AUTH_PROBE
IMAGES --> IMG_PROBE

%% =================== PDBs ===================
API --> API_PDB
AUTH --> AUTH_PDB
IMAGES --> IMG_PDB
