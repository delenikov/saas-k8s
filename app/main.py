from __future__ import annotations

import logging
from datetime import UTC, datetime

import time
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query

from app.compute import ComputeRequest, run_cpu_workload
from app.metrics import collect_runtime_metrics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CPU Workload Service",
    description="Deterministic matrix multiplication workloads for Kubernetes HPA CPU scaling experiments.",
    version="1.0.0",
)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/compute")
def compute(
    size: int = Query(default=100, ge=1, le=5000),
    iterations: int = Query(default=1, ge=1, le=100),
) -> dict[str, float | int | str]:
    request_start_time = time.perf_counter()
    request_id = str(uuid4())

    metrics = collect_runtime_metrics()

    request = ComputeRequest(size=size,iterations=iterations,)

    logger.info("request_id=%s compute request size=%s iterations=%s hostname=%s", request_id, size, iterations, metrics.hostname)

    try:
        result = run_cpu_workload(request)

    except MemoryError as exc:
        logger.exception("request_id=%s compute failed due to insufficient memory hostname=%s", request_id, metrics.hostname)
        raise HTTPException(status_code=507, detail="Not enough memory for requested workload") from exc

    except Exception as exc:
        logger.exception("request_id=%s compute failed hostname=%s", request_id, metrics. hostname)
        raise HTTPException(status_code=500,detail="Computation failed") from exc

    total_request_duration = time.perf_counter() - request_start_time

    logger.info(("request_id=%s compute completed " "size=%s iterations=%s " "compute_duration=%.6f " "total_duration=%.6f " "hostname=%s"), request_id, size, iterations, result.execution_time_seconds, total_request_duration, metrics.hostname)

    return {
        "request_id": request_id,
        "size": size,
        "iterations": iterations,
        "checksum": result.checksum,
        "compute_time_seconds": result.execution_time_seconds,
        "total_request_time_seconds": total_request_duration,
        "timestamp": datetime.now(UTC).isoformat(),
        "metrics_hostname": metrics.hostname,
        "metrics_process_id": metrics.process_id,
        "metrics_cpu_count": metrics.cpu_count,
        "metrics_memory_usage_bytes": metrics.memory_usage_bytes,
    }