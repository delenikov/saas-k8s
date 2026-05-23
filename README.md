# CPU Workload Service

FastAPI microservice for a deterministic matrix multiplication workload used in Kubernetes HPA scalability experiments.

## Endpoints

- `POST /compute?size=64` runs the CPU workload.
- The compute response includes `size`, `execution_time_seconds`, `checksum`, `timestamp`, `pod_hostname`, and `cpu_count`.

Validation rejects `size > 5000` with FastAPI validation errors.

## Workload Algorithm

The service uses one algorithm: generate two deterministic `size x size` matrices, then repeatedly multiply them with an explicit triple-loop `O(n^3)` Python implementation. 

## Local Run

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Docker

```bash
docker build -t saas-matrix-project:latest .
docker run --rm -p 8080:8080 saas-matrix-project:latest
```

## Example Requests

```bash
curl -X POST "http://localhost:8080/compute?size=64"
curl -X POST "http://localhost:8080/compute?size=128"
```


## Load testing
```bash
./scripts/run_tests.sh http://a81c30a73ecb14b55b4216b98eb754fe-1000624712.eu-central-1.elb.amazonaws.com eks
./scripts/run_tests.sh http://134.112.128.79 aks
python scripts/parse_results.py
```
