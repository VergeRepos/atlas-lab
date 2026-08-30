"""Benchmark router."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from ..services.benchmark_service import BenchmarkService

router = APIRouter()
benchmark_service = BenchmarkService()
logger = logging.getLogger(__name__)

@router.get("/")
async def list_benchmarks():
    return benchmark_service.export_results()

@router.post("/run/{category}")
async def run_benchmark(name: str, description: str, category: str):
    try:
        def dummy():
            import time
            time.sleep(0.001)
        result = benchmark_service.run_benchmark(name, description, category, dummy, iterations=5)
        return result
    except Exception as e:
        logger.error(f"Benchmark error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
async def export_benchmarks():
    return benchmark_service.export_results()
