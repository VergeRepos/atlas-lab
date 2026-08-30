"""Tests for benchmark service."""
import pytest
from app.services.benchmark_service import BenchmarkService

def test_run_benchmark():
    svc = BenchmarkService()
    result = svc.run_benchmark(
        name="test",
        description="Test benchmark",
        category="test",
        benchmark_func=lambda: sum(range(100)),
        iterations=3
    )
    assert result.metrics.mean >= 0
    assert result.metrics.sample_count == 3
    assert result.metrics.median >= 0

def test_export_results():
    svc = BenchmarkService()
    svc.run_benchmark("t1", "desc", "cat", lambda: None, iterations=2)
    exp = svc.export_results()
    assert exp["count"] >= 1
    assert len(exp["benchmarks"]) >= 1

def test_benchmark_with_warmup():
    svc = BenchmarkService()
    result = svc.run_benchmark(
        name="warmup_test",
        description="With warmup",
        category="test",
        benchmark_func=lambda: None,
        iterations=2,
        warmup=1
    )
    assert result.metrics.sample_count == 2
