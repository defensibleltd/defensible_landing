#!/usr/bin/env python3
"""
Test Reports Script.

This script generates all available IP Fabric reports, both with and without site filters.
It provides a comprehensive way to test the report generation functionality using direct
parameter passing instead of environment variables.
"""

# Standard library imports
import os
import sys
from typing import List, Optional
import time
import dotenv

# Third-party imports
from loguru import logger

try:
    from ipfabric_reports.main import IPFabricReportGenerator
    from ipfabric_reports.report_registry import ReportRegistry
except ImportError:
    print("Required package 'ipfabric-reports' is not installed.")
    print("Please install it using: pip install ipfabric-reports")
    sys.exit(1)

# Configuration
# load environment variables from .env file
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
SITE_NAME = "L36"  # Static site name for testing
IPF_URL = os.getenv("IPF_URL")  # Still using env for sensitive data
IPF_TOKEN = os.getenv("IPF_TOKEN")
NVD_API_KEY = os.getenv("NVD_API_KEY")  # For CVE reports
SKIP_REPORTS = ["overview-compare"]  # Reports to skip


# Color definitions
class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"


def get_available_reports() -> List[str]:
    """Get list of all available report types."""
    return list(ReportRegistry.list_reports().keys())


def generate_report(report_type: str, site: Optional[str] = None) -> None:
    """
    Generate a single report.

    Args:
        report_type: Type of report to generate
        site: Optional site filter
    """
    try:
        logger.info(
            f"Generating {report_type} report for site {site if site else 'all'}"
        )
        generator = IPFabricReportGenerator(
            ipf_url=IPF_URL,
            token=IPF_TOKEN,
            report_type=report_type,
            site_filter=site,
            nvd_api_key=NVD_API_KEY,
        )
        generator.generate_report()
        logger.success(
            f"Successfully generated {report_type} report"
            + (f" for site {site}" if site else "")
        )

    except Exception as e:
        logger.error(f"Error generating {report_type} report: {str(e)}")
        return


def main() -> None:
    """
    Main execution function.
    Generates all available reports, first without site filter, then with site filter.
    """
    # Validate required environment variables
    if not all([IPF_URL, IPF_TOKEN]):
        logger.error("IPF_URL and IPF_TOKEN environment variables must be set")
        sys.exit(1)

    # Get all available reports
    reports = get_available_reports()
    logger.info(f"Found {len(reports)} available reports: {', '.join(reports)}")

    # Remove reports to skip
    reports = [r for r in reports if r not in SKIP_REPORTS]

    # Track execution time
    start_time = time.time()

    # First run all reports without site filter
    logger.info(f"{Colors.BLUE}Generating reports without site filter{Colors.RESET}")
    for report_type in reports:
        if report_type == "cve":
            # Skip CVE report without site filter
            logger.success("Skipping CVE report without site filter")
        else:
            generate_report(report_type)
            logger.info("Sleeping for 3 seconds to slow down data collection")
            time.sleep(3)

    # Then run all reports with site filter
    logger.info(
        f"{Colors.BLUE}Generating reports with site filter: {Colors.GREEN}{SITE_NAME}{Colors.RESET}"
    )
    if not SITE_NAME:
        logger.error(
            "SITE_NAME environment variable must be set to run reports with site filter"
        )
        sys.exit(1)
    for report_type in reports:
        if report_type == "discovery":
            # Skip discovery report with site filter
            logger.success(f"Skipping discovery report with site filter: {SITE_NAME}")
        else:
            generate_report(report_type, SITE_NAME)
            logger.info("Sleeping for 3 seconds to slow down data collection")
            time.sleep(3)

    # Print execution summary
    execution_time = time.time() - start_time
    total_reports = len(reports) * 2  # Each report is run twice
    logger.info(f"{Colors.BLUE}Execution Summary:{Colors.RESET}")
    logger.info(f"Total reports generated: {total_reports}")
    logger.info(f"Total execution time: {execution_time:.2f} seconds")
    logger.info(
        f"Average time per report: {execution_time / total_reports:.2f} seconds"
    )


if __name__ == "__main__":
    # Configure logger
    logger.remove()
    logger.add(
        sys.stderr,
        # format="<level>{level: <8}</level> | <white>{message}</white>",
        colorize=True,
    )

    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nTest execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
