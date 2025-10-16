"""
Utility Functions Module (utils.py)

This module contains reusable helper functions that support general backend operations 
throughout EchoLogz. These functions perform small, common, and framework-independent 
tasks that keep other modules (like `compatibility`, `crud`, or `main`) clean and focused.

Core Responsibilities:
- Provide lightweight, reusable utilities (e.g., normalization, timestamp formatting, 
  file path resolution, or vector math helpers)
- Serve as a centralized toolbox for minor data manipulation tasks
- Support core logic in the `services` and `database` layers without creating dependencies

Purpose:
Acts as the Swiss Army knife of the EchoLogz backend — simplifying repetitive logic, 
maintaining clean code structure, and ensuring consistency across modules.

Typical Usage Example:
    from services.utils import normalize_vector, timestamp_now

    normalized = normalize_vector([0.2, 0.4, 0.8])
    print(f"Normalized Vector: {normalized}")
    print(f"Timestamp: {timestamp_now()}")
"""

# Standard Library
import os                      # File paths, environment variables
import json                    # JSON formatting and serialization
import math                    # Basic math operations (ex: rounding, normalization)
import logging                 # Consistent logging for debugging
from datetime import datetime  # Timestamps, log markers

# Third-Party Libraries (commonly used with EchoLogz stack)
import numpy as np             # Vector operations (used by compatibility calculations)
from sklearn.preprocessing import normalize  # Optional: for feature normalization


def normalize_vector(vector):
    """Normalize a numeric list or NumPy array to unit length."""
    vector = np.array(vector)
    norm = np.linalg.norm(vector)
    return vector / norm if norm != 0 else vector


def timestamp_now():
    """Return current UTC timestamp as an ISO-formatted string."""
    return datetime.utcnow().isoformat()


def json_pretty(data):
    """Convert Python objects into a pretty-formatted JSON string."""
    return json.dumps(data, indent=4, ensure_ascii=False)


def log_message(message, level="info"):
    """Log messages consistently across the app."""
    getattr(logging, level.lower())(f"[EchoLogz] {message}")