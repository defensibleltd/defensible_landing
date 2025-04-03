#!/usr/bin/env python3
"""
IP Fabric Report Generator - Report Registry Module.

This module implements a registry pattern for managing and accessing different
report types in the IP Fabric report generator. It provides a central location
for registering report types and their corresponding configurations.

Key Features:
    - Dynamic report type registration
    - Report type validation
    - Configuration mapping
    - Report class lookup functionality
    - Report type enumeration

Available Reports:
    - Management Protocol Report: Network management protocols analysis
    - Port Capacity Report: Network port utilization analysis
    - Overview Report: Network infrastructure overview
    - Overview Compare Report: Snapshot comparison analysis
    - Discovery Report: Network discovery status
    - CVE Report: Security vulnerability analysis
    - Trunk Mismatch Report: VLAN trunking analysis

Usage:
    The registry provides methods to:
    - Register new report types
    - Retrieve report classes
    - List available reports
    - Validate report configurations

Note:
    All report types must be registered here to be available in the application.
    Each report type must have a corresponding configuration class.
"""

# Standard library imports
from typing import Dict, Type

# Local imports
from .config import (
    CVEReportConfig,
    DiscoveryReportConfig,
    ManagementProtocolConfig,
    OverviewCompareReportConfig,
    OverviewReportConfig,
    PortCapacityReportConfig,
    TrunkMismatchConfig,
)
from .report_types import (
    BaseReport,
    CVEReport,
    DiscoveryReport,
    ManagementProtocolReport,
    OverviewCompareReport,
    OverviewReport,
    PortCapacityReport,
    TrunkMismatchReport,
)


class ReportRegistry:
    _reports: Dict[str, Type[BaseReport]] = {}

    @classmethod
    def register(cls, report_type: str, report_class: Type[BaseReport]):
        cls._reports[report_type] = report_class

    @classmethod
    def get_report(cls, report_type: str) -> Type[BaseReport]:
        if report_type not in cls._reports:
            raise ValueError(f"Unknown report type: {report_type}")
        return cls._reports[report_type]

    @classmethod
    def list_reports(cls):
        reports = {}
        for report_type, report_class in cls._reports.items():
            try:
                description = report_class.get_report_details().get(
                    "description", "Description unavailable"
                )
                reports[report_type] = description
            except Exception as e:
                print(f"Error getting description for report type '{report_type}': {e}")
                reports[report_type] = "Description unavailable"
        return reports


# Register all report types
ReportRegistry.register(CVEReportConfig.REPORT_TYPE, CVEReport)
ReportRegistry.register(DiscoveryReportConfig.REPORT_TYPE, DiscoveryReport)
ReportRegistry.register(ManagementProtocolConfig.REPORT_TYPE, ManagementProtocolReport)
ReportRegistry.register(OverviewReportConfig.REPORT_TYPE, OverviewReport)
ReportRegistry.register(OverviewCompareReportConfig.REPORT_TYPE, OverviewCompareReport)
ReportRegistry.register(PortCapacityReportConfig.REPORT_TYPE, PortCapacityReport)
ReportRegistry.register(TrunkMismatchConfig.REPORT_TYPE, TrunkMismatchReport)
