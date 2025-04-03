# ipfabric_reports/cli.py
# Description: This module contains the command-line interface for the IP Fabric report generator.

# Standard library imports
import argparse
import os
import sys

# Third-party imports
from loguru import logger
import invoke

# Local imports
from .main import IPFabricReportGenerator
from .report_registry import ReportRegistry


def main():
    parser = argparse.ArgumentParser(
        description="Generate reports from IP Fabric data."
    )
    parser.add_argument("--env", help="Path to .env file", default=None)
    parser.add_argument("--type", help="Type of report to generate", default=None)
    parser.add_argument("--style", help="CSS style to use for the report", default=None)
    parser.add_argument("--site", help="Filter report by site name", default=None)
    parser.add_argument(
        "--list", action="store_true", help="List available report types"
    )
    parser.add_argument(
        "-i",
        "--install-extension",
        action="store_true",
        help="Install the report generator as an IP Fabric extension",
    )
    parser.add_argument(
        "--streamlit",
        action="store_true",
        help="Launch the streamlit web interface locally",
    )
    args = parser.parse_args()

    if args.list:
        available_reports = ReportRegistry.list_reports()
        print("Available reports:")
        max_type_length = max(
            len(report_type) for report_type in available_reports.keys()
        )
        for report_type, report_description in available_reports.items():
            print(f"{report_type.rjust(max_type_length + 2)}: {report_description}")
        return

    if args.streamlit:
        print("Starting streamlit web interface...")
        command_args = [
            "streamlit",
            "run",
            "ipfabric_reports/frontend/frontend.py",
            "--theme.primaryColor=#8C989B",
            "--theme.backgroundColor=#222D32",
            "--theme.secondaryBackgroundColor=#264183",
            "--theme.textColor=#F6F6F6",
            "--theme.font=monospace",
        ]
        invoke.run(str(" ".join(command_args)))
        return

    if args.install_extension:
        install_extension()
        return

    try:
        if args.type:
            os.environ["REPORT_TYPE"] = args.type
        generator = IPFabricReportGenerator(env_file=args.env)
        if args.site:
            generator.site_filter = args.site
        generator.generate_report()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


def install_extension():
    """Handle the extension installation logic."""
    print("Installing the report generator as an IP Fabric extension...")
    try:
        from ipfabric import IPFClient

        ipf = IPFClient()
        current_extensions = ipf.extensions.extensions
        if "ipfabric_reports" in [_.name for _ in current_extensions]:
            print("Extension already installed")
        else:
            print("Installing extension")
            ipf.extensions.register_from_git_url(
                git_url="https://gitlab.com/ip-fabric/integrations/scripts/ipfabric-reports",
                name="ipfabric_reports",
                slug="ipfabric-reports",
                description="IP Fabric reports extension for IP Fabric",
            )
            print("Extension installed")
        ipf_url = ipf.base_url
        ipf_url = str(ipf_url).replace("api/v7.0/", "")
        print(
            f"Extension is available in IP Fabric @ {ipf_url}extensions-apps/ipfabric-reports"
        )
        sys.exit(0)
    except AttributeError:
        # TODO: remove this once the extension endpoint is generally available and pin the IP Fabric sdk to version <=7.0.0
        print(
            "Extensions API not available. Please upgrade to IPFabric version 7.0.0b8 or higher."
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error installing extension: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
