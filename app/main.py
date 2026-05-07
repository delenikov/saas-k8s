from __future__ import annotations

import logging
from datetime import UTC, datetime

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
    description="Request-based NumPy workloads for Kubernetes HPA CPU scaling experiments.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics-info")
def metrics_info() -> dict[str, int | str]:
    metrics = collect_runtime_metrics()
    return {
        "hostname": metrics.hostname,
        "process_id": metrics.process_id,
        "cpu_count": metrics.cpu_count,
        "memory_usage_bytes": metrics.memory_usage_bytes,
    }


@app.post("/compute")
def compute(
    size: int = Query(default=500, ge=1, le=5000),
    iterations: int = Query(default=5, ge=1, le=100),
    complexity: int = Query(default=1, ge=1, le=10),
) -> dict[str, float | int | str]:
    metrics = collect_runtime_metrics()
    request = ComputeRequest(size=size, iterations=iterations, complexity=complexity)
    logger.info(
        "compute request size=%s iterations=%s complexity=%s hostname=%s",
        size,
        iterations,
        complexity,
        metrics.hostname,
    )

    try:
        result = run_cpu_workload(request)
    except MemoryError as exc:
        logger.exception("compute failed due to insufficient memory hostname=%s", metrics.hostname)
        raise HTTPException(status_code=507, detail="Not enough memory for requested workload") from exc
    except Exception as exc:
        logger.exception("compute failed hostname=%s", metrics.hostname)
        raise HTTPException(status_code=500, detail="Computation failed") from exc

    logger.info(
        "compute completed size=%s iterations=%s complexity=%s duration=%.6f hostname=%s",
        size,
        iterations,
        complexity,
        result.execution_time_seconds,
        metrics.hostname,
    )
    return {
        "size": size,
        "iterations": iterations,
        "complexity": complexity,
        "execution_time_seconds": result.execution_time_seconds,
        "timestamp": datetime.now(UTC).isoformat(),
        "pod_hostname": metrics.hostname,
        "cpu_count": metrics.cpu_count,
    }
