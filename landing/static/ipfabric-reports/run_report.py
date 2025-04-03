#!/usr/bin/env python3
"""
Run Report Script.

This module contains the entry point for running the IP Fabric report generator.
It provides a simple interface to generate reports using the IPFabricReportGenerator.
"""

# Standard library imports
import sys

# Third-party imports
try:
    from ipfabric_reports.main import IPFabricReportGenerator
except Exception as e:
    print(f"Error importing ipfabric-reports: {str(e)}")
    sys.exit(1)


def main() -> None:
    """
    Main execution function.

    Creates an instance of IPFabricReportGenerator and generates the report.
    """
    try:
        generator = IPFabricReportGenerator()
        generator.generate_report()
    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
