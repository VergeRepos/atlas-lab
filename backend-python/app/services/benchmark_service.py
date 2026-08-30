"""
Benchmark Service
Measures performance of key operations
"""

import time
import statistics
from typing import List, Dict, Any
from datetime import datetime, timezone
import json

from ..models.database import BenchmarkResult, BenchmarkMetrics


class BenchmarkService:
    """Service for benchmarking system performance."""

    def __init__(self):
        self.benchmarks: List[BenchmarkResult] = []

    def run_benchmark(
        self,
        name: str,
        description: str,
        category: str,
        benchmark_func,
        iterations: int = 10,
        warmup: int = 2,
        duration_limit: float = 60.0  # Max seconds per measurement
    ) -> BenchmarkResult:
        """Run a benchmark and collect metrics."""
        # Warmup
        for _ in range(warmup):
            benchmark_func()

        measurements = []
        start_total = time.time()

        for _ in range(iterations):
            start = time.time()
            benchmark_func()
            end = time.time()
            measurements.append(end - start)

            # Check if we've exceeded duration limit
            if (time.time() - start_total) > duration_limit:
                break

        # Calculate metrics
        mean_time = statistics.mean(measurements)
        median_time = statistics.median(measurements)
        sorted_measurements = sorted(measurements)

        # P95 and P99
        p95_idx = max(0, int(len(sorted_measurements) * 0.95))
        p99_idx = max(0, int(len(sorted_measurements) * 0.99))
        p95 = sorted_measurements[p95_idx]
        p99 = sorted_measurements[p99_idx]

        std_dev = statistics.stdev(measurements) if len(measurements) > 1 else 0.0

        # Calculate throughput (items per second)
        throughput = 1.0 / mean_time if mean_time > 0 else 0.0

        metrics = BenchmarkMetrics(
            mean=mean_time,
            median=median_time,
            p95=p95,
            p99=p99,
            min=min(measurements),
            max=max(measurements),
            std_dev=std_dev,
            throughput=throughput,
            sample_count=len(measurements),
        )

        result = BenchmarkResult(
            id=str(__import__('uuid').uuid4()),
            name=name,
            description=description,
            category=category,
            metrics=metrics,
            environment=self._get_environment_info(),
            created_at=datetime.now(timezone.utc),
            duration_ms=sum(measurements) * 1000,
        )

        self.benchmarks.append(result)
        return result

    def _get_environment_info(self) -> Dict[str, Any]:
        """Get environment information."""
        import platform
        import sys
        return {
            'os': platform.system(),
            'os_version': platform.release(),
            'python_version': sys.version.split()[0],
            'cpu_count': __import__('os').cpu_count(),
            'machine': platform.machine(),
        }

    def export_results(self, format: str = 'json') -> Dict[str, Any]:
        """Export benchmark results."""
        results = []
        for bench in self.benchmarks:
            results.append({
                'id': bench.id,
                'name': bench.name,
                'description': bench.description,
                'category': bench.category,
                'metrics': {
                    'mean': bench.metrics.mean,
                    'median': bench.metrics.median,
                    'p95': bench.metrics.p95,
                    'p99': bench.metrics.p99,
                    'min': bench.metrics.min,
                    'max': bench.metrics.max,
                    'throughput': bench.metrics.throughput,
                    'sample_count': bench.metrics.sample_count,
                },
                'duration_ms': bench.duration_ms,
                'created_at': bench.created_at.isoformat(),
            })

        return {'benchmarks': results, 'count': len(results)}

    def compare_results(
        self, benchmark_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare benchmark results by ID."""
        comparison = {}
        for bench_id in benchmark_ids:
            bench = next(
                (b for b in self.benchmarks if b.id == bench_id), None
            )
            if bench:
                comparison[bench_id] = {
                    'name': bench.name,
                    'mean_ms': bench.metrics.mean * 1000,
                    'median_ms': bench.metrics.median * 1000,
                    'throughput': bench.metrics.throughput,
                }
        return comparison