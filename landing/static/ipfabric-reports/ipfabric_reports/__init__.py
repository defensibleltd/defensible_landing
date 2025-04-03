"""
IP Fabric Reports Generator.

A Python package for generating comprehensive network reports using IP Fabric data.
Provides automated report generation with multiple report types and customizable templates.

Available Report Types:
    - Management Protocol Report
    - Port Capacity Report
    - Overview Report
    - Overview Compare Report
    - Discovery Report
    - CVE Report
    - Trunk Mismatch Report

For detailed usage instructions, see the documentation.
"""

# Version information
__version__ = "1.0.5"
__author__ = "IP Fabric"
__license__ = "MIT"

# Public API
from .main import IPFabricReportGenerator  # noqa: F401
from . import cli  # noqa: F401

# Define public interface
__all__ = [
    "IPFabricReportGenerator",
    "cli",
]
