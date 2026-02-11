"""
FastAPI application simulating GIS/Image processing workload.

This simulates:
- Raster processing
- Tile generation
- Feature extraction
- ML inference

Each request blocks for 10 seconds to demonstrate bottleneck scenarios.
"""

from fastapi import FastAPI
import time
import os
from datetime import datetime

app = FastAPI(
    title="GIS Processing Simulation API",
    description="Demonstrates single-node bottlenecks and horizontal scaling benefits",
    version="1.0.0"
)


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "service": "GIS Processing Simulation",
        "worker_pid": os.getpid(),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/process")
def process():
    """
    Simulates a heavy GIS/Image computation task.
    
    In real scenarios, this could be:
    - Raster tile rendering
    - Feature extraction from satellite imagery
    - ML inference on geospatial data
    - Coordinate transformation on large datasets
    
    The 10-second sleep simulates CPU-intensive processing.
    """
    pid = os.getpid()
    start_time = datetime.now()
    
    # Simulated GIS/Image computation - 1 seconds of blocking work
    time.sleep(1)
    
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    return {
        "status": "done",
        "worker_pid": pid,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "processing_time_seconds": processing_time
    }


@app.get("/health")
def health():
    """Lightweight health check for load balancer."""
    return {"status": "healthy", "pid": os.getpid()}
