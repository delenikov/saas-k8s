from __future__ import annotations

import os
import socket
from dataclasses import dataclass

import psutil


@dataclass(frozen=True, slots=True)
class RuntimeMetrics:
    hostname: str
    process_id: int
    cpu_count: int
    memory_usage_bytes: int


def collect_runtime_metrics() -> RuntimeMetrics:
    return RuntimeMetrics(
        hostname=socket.gethostname(),
        process_id=os.getpid(),
        cpu_count=os.cpu_count() or 1,
        memory_usage_bytes=_memory_usage_bytes(),
    )


def _memory_usage_bytes() -> int:
    process = psutil.Process(os.getpid())
    return int(process.memory_info().rss)
