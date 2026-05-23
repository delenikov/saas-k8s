from __future__ import annotations

import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)

Matrix = list[list[float]]


@dataclass(frozen=True, slots=True)
class ComputeRequest:
    size: int


@dataclass(frozen=True, slots=True)
class ComputeResult:
    execution_time_seconds: float
    checksum: float


def run_cpu_workload(request: ComputeRequest) -> ComputeResult:
    start_time = time.perf_counter()

    matrix_a = _build_matrix(request.size, seed=1)
    matrix_b = _build_matrix(request.size, seed=7)

    try:
        checksum = _matrix_multiplication_workload(
            matrix_a=matrix_a,
            matrix_b=matrix_b,
        )
    except MemoryError:
        logger.exception("Memory error while running CPU workload")
        raise

    return ComputeResult(
        execution_time_seconds=time.perf_counter() - start_time,
        checksum=float(checksum),
    )


def _build_matrix(size: int, seed: int) -> Matrix:
    matrix: Matrix = []

    for row_index in range(size):
        row: list[float] = []

        for column_index in range(size):
            value = ((row_index + seed) * (column_index + seed + 1)) % 97
            row.append((value + 1) / 97.0)

        matrix.append(row)

    return matrix


def _matrix_multiplication_workload(
    matrix_a: Matrix,
    matrix_b: Matrix,
) -> float:
    result = matrix_a
    checksum = 0.0
    size = len(matrix_a)
    next_result: Matrix = [[0.0] * size for _ in range(size)]

    for row_index in range(size):
        result_row = result[row_index]
        next_row = next_result[row_index]

        for column_index in range(size):
            total = 0.0

            for inner_index in range(size):
                total += result_row[inner_index] * matrix_b[inner_index][column_index]

            next_row[column_index] = total
            checksum += total

    return checksum
