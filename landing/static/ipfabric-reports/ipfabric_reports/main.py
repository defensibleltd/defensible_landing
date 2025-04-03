#!/usr/bin/env python3
"""
IP Fabric Report Generator - Main Module.

This module serves as the core component of the IP Fabric report generator.
It provides the main functionality for generating various types of network
reports using data from IP Fabric.

Main Components:
    - IPFabricReportGenerator: Core class that orchestrates report generation
    - Environment configuration handling
    - IP Fabric client initialization
    - Report type selection and generation

Usage:
    The module can be used directly or imported as part of the larger package:
    >>> generator = IPFabricReportGenerator()
    >>> generator.generate_report()

Environment Variables:
    - IPF_URL: IP Fabric instance URL
    - IPF_TOKEN: API token for authentication
    - IPF_SNAPSHOT_ID: Specific snapshot ID (optional)
    - REPORT_TYPE: Type of report to generate
    - REPORT_SITE: Site filter for the report (optional)
    - INVENTORY_FILTER: Device inventory filter for the report (optional)
    - REPORT_STYLE: CSS style file to use (optional)
"""

from __future__ import annotations

# Standard library imports
import os
from pathlib import Path
from typing import Optional, Union

# Third-party imports
from dotenv import load_dotenv, find_dotenv
from ipfabric import IPFClient
from loguru import logger

# Local imports
from .report_registry import ReportRegistry
from .report_renderer import ReportRenderer


class IPFabricReportGenerator:
    """
    Generator for IP Fabric reports with flexible initialization options.

    Supports both direct parameter passing and environment variable configuration.
    Direct parameters take precedence over environment variables.

    Args:
        ipf_client: Pre-configured IPFClient instance
        ipf_url: IP Fabric instance URL
        token: API token for authentication
        snapshot_id: Specific snapshot ID (defaults to "$last")
        verify_ssl: Whether to verify SSL certificates
        timeout: API request timeout in seconds
        env_file: Path to environment file
        report_type: Type of report to generate
        site_filter: Site filter for the report
        inventory_filter: Device inventory filter
        report_style: CSS style file to use
        nvd_api_key: API key for NVD data
    """

    def __init__(
            self,
            ipf_client: Optional[IPFClient] = None,
            ipf_url: Optional[str] = None,
            token: Optional[str] = None,
            snapshot_id: str = None,
            snapshot_id_prev: str = None,
            verify_ssl: bool = False,
            timeout: int = 30,
            env_file: Optional[Union[str, Path]] = None,
            export_dir: str = None,
            report_type: Optional[str] = None,
            site_filter: Optional[str] = None,
            inventory_filter: Optional[str] = None,
            report_style: str = "default_style.css",
            nvd_api_key: Optional[str] = None
    ):
        # Load environment variables if specified
        self._load_env(env_file)

        # Set up IP Fabric client - either use provided client or create new one
        if ipf_client is not None:
            try:
                ipf_client.os_version
                self.ipf = ipf_client
            except Exception as e:
                raise ValueError(f"Error initializing IP Fabric client: {str(e)}")
        else:
            # Try parameters first, then environment variables
            final_url = ipf_url or os.getenv("IPF_URL")
            final_token = token or os.getenv("IPF_TOKEN")
            final_snapshot = snapshot_id or os.getenv("IPF_SNAPSHOT_ID", "$last")
            if not all([final_url, final_token]):
                raise ValueError(
                    "When not providing an IPFClient instance, "
                    "both URL and token must be provided either directly "
                    "or through environment variables (IPF_URL, IPF_TOKEN)"
                )

            self.ipf = IPFClient(
                base_url=final_url,
                auth=final_token,
                snapshot_id=final_snapshot,
                verify=verify_ssl,
                timeout=timeout,
            )

        # Set report configuration
        self.report_type = report_type or os.getenv("REPORT_TYPE")
        self.site_filter = site_filter or os.getenv("REPORT_SITE")
        self.inventory_filter = inventory_filter or os.getenv("INVENTORY_FILTER")
        self.report_style = report_style or os.getenv(
            "REPORT_STYLE", "default_style.css"
        )
        self.nvd_api_key = nvd_api_key or os.getenv("NVD_API_KEY")
        self.export_dir = export_dir or os.getenv("EXPORT_DIR", "export")
        self.snapshot_id_prev = snapshot_id_prev or os.getenv("IPF_SNAPSHOT_ID_PREV", "$prev")
        self.logo_path = os.getenv("LOGO_PATH") or None

        # Validate report type
        self._validate_report_type()

        # Validate site filter if provided
        if self.site_filter:
            self._validate_site_filter()

        # Initialize renderer
        self._initialize_renderer()

    @staticmethod
    def _load_env(env_file: Optional[Union[str, Path]]) -> None:
        """Load environment variables from file."""
        if env_file:
            env_path = Path(env_file)
            if not env_path.exists():
                raise FileNotFoundError(f"Environment file not found: {env_path}")
            load_dotenv(env_path, override=True)
            logger.info(f"Loaded environment from: {env_path}")
        else:
            load_dotenv(find_dotenv(usecwd=True), override=True)

    def _validate_report_type(self) -> None:
        """Validate the report type."""
        if not self.report_type:
            available_reports = ReportRegistry.list_reports()
            raise ValueError(
                "Report type must be specified. "
                f"Available types: {', '.join(available_reports.keys())}"
            )

    def _validate_site_filter(self) -> None:
        """Validate the site filter if provided."""
        site_list = self.ipf.fetch_all("tables/inventory/sites")
        site_names = [site["siteName"] for site in site_list]

        if self.site_filter not in site_names:
            raise ValueError(f"Site not found: {self.site_filter}")

        site_devices = self.ipf.inventory.devices.all(
            filters={"siteName": ["eq", self.site_filter]}
        )
        if not site_devices:
            raise ValueError(f"No devices found in site: {self.site_filter}")

    def _initialize_renderer(self) -> None:
        """Initialize the report renderer."""
        package_dir = Path(__file__).resolve().parent
        self.css_path = package_dir / "styles" / self.report_style

        self.renderer = ReportRenderer(
            template_dir=package_dir / "templates",
            output_dir=self.export_dir,
            generate_html=False,
            logo_path=self.logo_path or "styles/img/IP_Fabric_VerticalLogo_Color.svg",
        )

    def generate_report(self) -> None:
        """Generate the report based on configured settings."""
        report_class = ReportRegistry.get_report(self.report_type)

        # Handle CVE report special case
        if self.report_type == "cve" and not self.nvd_api_key:
            raise ValueError("NVD_API_KEY environment variable is required for CVE reports")
        
        # Create report instance
        report = report_class(
            self.ipf,
            snapshot_id=self.ipf.snapshot_id,
            snapshot_id_prev=self.snapshot_id_prev,
            site_filter=self.site_filter,
            inventory_filter=self.inventory_filter,
            nvd_api_key=self.nvd_api_key,
            export_dir=self.export_dir,
        )

        # Collect data and render reports
        try:
            logger.info(
                f"Collecting data for {report_class.get_report_details().get('name')} report..."
            )
            report_data = report.collect_data()
            template_name = f"{self.report_type}_template.html"

            # Handle special case for trunk mismatch reports
            if self.report_type == "trunk-mismatch":
                self.renderer.render_xlsx_report(report_data=report_data)
            self.renderer.render_pdf_report(template_name, report_data, self.css_path)

        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise


def main():
    generator = IPFabricReportGenerator()
    generator.generate_report()


if __name__ == "__main__":
    main()
