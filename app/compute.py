from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ComputeRequest:
    size: int
    iterations: int
    complexity: int


@dataclass(frozen=True, slots=True)
class ComputeResult:
    execution_time_seconds: float
    checksum: float


def run_cpu_workload(request: ComputeRequest) -> ComputeResult:
    start_time = time.perf_counter()

    rng = np.random.default_rng()
    matrix_a = rng.random((request.size, request.size), dtype=np.float64)
    matrix_b = rng.random((request.size, request.size), dtype=np.float64)

    try:
        checksum = _matrix_power_workload(
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            iterations=request.iterations,
            complexity=request.complexity,
        )
    except FloatingPointError:
        logger.exception("Floating point error while running CPU workload")
        raise
    except np.linalg.LinAlgError:
        logger.exception("Linear algebra error while running CPU workload")
        raise

    return ComputeResult(
        execution_time_seconds=time.perf_counter() - start_time,
        checksum=float(checksum),
    )


def _matrix_power_workload(
    matrix_a: NDArray[np.float64],
    matrix_b: NDArray[np.float64],
    iterations: int,
    complexity: int,
) -> float:
    result = matrix_a
    checksum = 0.0

    for _ in range(iterations):
        result = result @ matrix_b

        for _ in range(complexity):
            result = np.sin(result) + np.cos(result)

        normalized = _normalized_square(result)
        checksum += float(np.linalg.det(normalized))

        if complexity >= 3:
            eigenvalues = np.linalg.eigvals(normalized)
            checksum += float(np.abs(eigenvalues).mean())

        if complexity >= 6:
            inverse = np.linalg.inv(normalized)
            checksum += float(inverse.mean())

        result = np.divide(result, np.linalg.norm(result) + 1.0)

    return checksum


def _normalized_square(matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    scale = np.linalg.norm(matrix) + 1.0
    return np.divide(matrix, scale) + np.eye(matrix.shape[0], dtype=np.float64)
