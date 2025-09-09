# Это нужно, чтобы celery всегда запускался, когда Django стартует
from .celery import app as celery_app

__all__ = ("celery_app",)
