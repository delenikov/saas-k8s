# CPU Workload Service

FastAPI microservice for a deterministic matrix multiplication workload used in Kubernetes HPA scalability experiments.

## Endpoints

- `GET /health` returns service health.
- `GET /metrics-info` returns hostname, process id, CPU count, and resident memory usage.
- `POST /compute?size=64&iterations=5` runs the CPU workload.
- The compute response includes `size`, `iterations`, `execution_time_seconds`, `checksum`, `timestamp`, `pod_hostname`, and `cpu_count`.

Validation rejects `size > 5000` and `iterations > 100` with FastAPI validation errors.

## Workload Algorithm

The service uses one algorithm: generate two deterministic `size x size` matrices, then repeatedly multiply them with an explicit triple-loop `O(n^3)` Python implementation. A checksum is accumulated from every multiplication result so the work cannot be optimized away.

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
curl http://localhost:8080/health
curl http://localhost:8080/metrics-info
curl -X POST "http://localhost:8080/compute?size=64&iterations=5"
curl -X POST "http://localhost:8080/compute?size=128&iterations=20"
```

## Kubernetes HPA Notes

- Run one uvicorn process per container and scale replicas with HPA.
- Set container CPU requests because CPU-based HPA calculates utilization from requested CPU.
- Increase request concurrency using k6 to produce predictable pod CPU pressure.
- Add Prometheus instrumentation later on a dedicated `/metrics` endpoint; `/metrics-info` is intentionally human-readable runtime info.
