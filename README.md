# CPU Workload Service

FastAPI microservice for one request-based CPU-intensive NumPy calculation used in Kubernetes HPA scalability experiments.

## Endpoints

- `GET /health` returns service health.
- `GET /metrics-info` returns hostname, process id, CPU count, and resident memory usage.
- `POST /compute?size=500&iterations=5&complexity=1` runs the CPU workload.

Validation rejects `size > 5000`, `iterations > 100`, and `complexity > 10` with FastAPI validation errors.

## Workload Algorithm

The service uses one algorithm: generate two random `size x size` matrices, repeatedly multiply them, and add complexity-controlled NumPy operations. Higher `complexity` values add more trigonometric passes and heavier linear algebra work.

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
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Docker

```bash
docker build -t cpu-workload-service:latest .
docker run --rm -p 8080:8080 cpu-workload-service:latest
```

## Example Requests

```bash
curl http://localhost:8080/health
curl http://localhost:8080/metrics-info
curl -X POST "http://localhost:8080/compute?size=500&iterations=5&complexity=1"
curl -X POST "http://localhost:8080/compute?size=1200&iterations=20&complexity=3"
```

## Kubernetes HPA Notes

- Run one uvicorn process per container and scale replicas with HPA.
- Set container CPU requests because CPU-based HPA calculates utilization from requested CPU.
- Start with `OPENBLAS_NUM_THREADS=1` and increase request concurrency using k6 to produce predictable pod CPU pressure.
- Add Prometheus instrumentation later on a dedicated `/metrics` endpoint; `/metrics-info` is intentionally human-readable runtime info.
