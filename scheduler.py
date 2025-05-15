from flask_apscheduler import APScheduler
import logging

# Global reference to the scheduler
_scheduler = None

def init_scheduler(scheduler):
    """Initialize the global scheduler reference"""
    global _scheduler
    _scheduler = scheduler
    return _scheduler

def add_job(job_id, func, run_date, args=None, kwargs=None):
    """Add a job to the scheduler"""
    if _scheduler is None:
        logging.error("Scheduler not initialized")
        raise ValueError("Scheduler not initialized")
    
    return _scheduler.add_job(
        id=job_id,
        func=func,
        trigger='date',
        run_date=run_date,
        args=args or [],
        kwargs=kwargs or {}
    )

def remove_job(job_id):
    """Remove a job from the scheduler"""
    if _scheduler is None:
        logging.error("Scheduler not initialized")
        raise ValueError("Scheduler not initialized")
    
    _scheduler.remove_job(job_id)

def get_jobs():
    """Get all scheduled jobs"""
    if _scheduler is None:
        logging.error("Scheduler not initialized")
        raise ValueError("Scheduler not initialized")
    
    return _scheduler.get_jobs()
