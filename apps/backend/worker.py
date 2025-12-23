#!/usr/bin/env python3
"""// ZeaZDev [Backend Celery Worker Entry Point] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""

from src.worker.celery_app import celery_app

# Import tasks to register them with celery

if __name__ == "__main__":
    # Start celery worker
    celery_app.worker_main(
        ["worker", "--loglevel=info", "--concurrency=2", "--pool=solo"]
    )
