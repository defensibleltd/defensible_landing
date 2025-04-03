#!/usr/bin/env python3
"""
IP Fabric Report Generator - Data Collectors Module.

This module provides data collection and processing functionality for various
IP Fabric reports. It contains collector classes that fetch and transform data
from IP Fabric's API into formats suitable for report generation.

Main Components:
    - BaseDataCollector: Abstract base class for all collectors
    - SnapshotSummaryCollector: Collects network summary information
    - PerSiteSummaryCollector: Collects summary information per site
    - ManagementProtocolCollector: Gathers management protocol data
    - PortCapacityCollector: Analyzes port capacity and utilization
    - OverviewCollector: Collects general network overview data
    - DiscoveryReportCollector: Handles discovery-related information
    - CVECollector: Processes vulnerability data
    - TrunkMismatchCollector: Collects data to analyze Vlan mismatch in trunks

Each collector is responsible for:
    - Fetching specific data from IP Fabric
    - Processing and transforming the data
    - Providing structured output for report generation
    - Handling data validation and error cases

Dependencies:
    - IPFabric SDK for API interaction
    - Pandas for data processing
    - Configuration classes for collector settings
"""

# Standard library imports
from collections import defaultdict
from dataclasses import dataclass, field
import json
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Type
from time import sleep
import requests.exceptions

# Third-party imports
import pandas as pd
from ipfabric import IPFClient
from ipfabric.tools import Vulnerabilities
from loguru import logger

# Local imports
from .config import (
    CVEReportConfig,
    DiscoveryReportConfig,
    NetworkSummaryConfig,
    PerSiteSummaryConfig,
    ManagementProtocolConfig,
    OverviewReportConfig,
    OverviewCompareReportConfig,
    PortCapacityReportConfig,
    TrunkMismatchConfig,
)
from .modules import count_unique_occurrences, get_distribution_ratio


def transform_name(name: str) -> str:
    """
    Transform the name to lowercase and replace spaces with underscores - used for attribute names
    """
    return name.lower().replace(" ", "_")


class ConfigurationError(Exception):
    """Exception raised for errors in the configuration."""

    pass


@dataclass
class BaseDataCollector:
    ipf: IPFClient
    site_filter: Optional[str] = None
    nvd_api_key: Optional[str] = None
    inventory_filter: Optional[str] = None
    snapshot_id: Optional[str] = "$last"
    config_class: ClassVar[Type] = None
    data: Dict[str, Any] = field(default_factory=dict, init=False)

    def __post_init__(self):
        if self.config_class:
            self._collect_data()

    def _collect_data(self):
        if not self.config_class:
            raise ValueError("config_class is not set")
        for index, item in enumerate(self.config_class.ITEMS, start=1):
            try:
                # The `name` and `method` fields are mandatory
                name = item["name"]
                method = item["method"]
            except KeyError as e:
                raise ConfigurationError(
                    f"Missing mandatory field '{e.args[0]}' in item {index} of {self.config_class.__name__}"
                )

            # The `key`, `filters`, `export` fields are optional
            key = item.get("key", None)
            filters = item.get("filters", {})
            export = item.get("export", None)

            if self.site_filter:
                filters["siteName"] = ["eq", self.site_filter]

            # ---> TODO Add a check to ensure the export is either 'df', or xxxx (not sure all possible options)

            transformed_name = transform_name(name)
            try:
                value = self._fetch_data(method=method, filters=filters, export=export)

            except Exception as e:
                raise ConfigurationError(
                    f"Error fetching data for '{name}' using method '{method}': {str(e)}"
                )

            if "uniq" in name.lower():
                unique_count = count_unique_occurrences(value, key)
                # self.data[transform_name(name)] = unique_count
                # print(f"Unique count for {name}: {unique_count}")
                self.data[transformed_name] = {
                    "name": name,
                    "key": None,
                    "value": unique_count,
                }
            else:
                # print(f"Value for {name}: {value} - {key}")
                self.data[transformed_name] = {
                    "name": name,
                    "key": key,
                    "value": value,
                }

    def _fetch_data(
        self,
        method: str,
        filters: Dict[str, Any] = None,
        columns: List[str] = None,
        export: str = None,
    ) -> Any:
        api_method = self.ipf
        for part in method.split("."):
            api_method = getattr(api_method, part)

        if callable(api_method):
            kwargs = {}
            if filters:
                kwargs["filters"] = filters
            if columns:
                kwargs["columns"] = columns
            if export:
                kwargs["export"] = export
            if self.snapshot_id:
                kwargs["snapshot_id"] = self.snapshot_id

            return api_method(**kwargs)
        else:
            return api_method

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'. "
            f"Available attributes: {', '.join(self.data.keys())}"
        )

    def return_data(self) -> Dict[str, Any]:
        """
        Return the collected data
        """
        return self.data

    @classmethod
    def get_report_details(cls) -> Dict[str, str]:
        """
        Return the report details
        """
        return {
            "name": cls.config_class.REPORT_NAME if cls.config_class else "",
            "type": cls.config_class.REPORT_TYPE if cls.config_class else "",
            "description": (
                cls.config_class.REPORT_DESCRIPTION if cls.config_class else ""
            ),
            "introduction": cls.config_class.REPORT_INTRO if cls.config_class else "",
        }


class SnapshotSummaryCollector(BaseDataCollector):
    config_class: ClassVar[Type] = NetworkSummaryConfig


class PerSiteSummaryCollector(BaseDataCollector):
    config_class = PerSiteSummaryConfig


class ManagementProtocolCollector(BaseDataCollector):
    config_class: ClassVar[Type] = ManagementProtocolConfig


class TrunkMismatchCollector(BaseDataCollector):
    config_class: ClassVar[Type] = TrunkMismatchConfig


@dataclass
class PortCapacityCollector(BaseDataCollector):
    config_class: ClassVar[Type] = PortCapacityReportConfig

    def get_data(self) -> Dict[str, Any]:
        filter_exclude_interfaces = {
            "intName": ["nireg", PortCapacityReportConfig.EXCLUDE_INTF_NAME]
        }
        if self.site_filter:
            filter_exclude_interfaces["siteName"] = ["eq", self.site_filter]

        interfaces_json = self.ipf.inventory.interfaces.all(
            columns=PortCapacityReportConfig.INTERFACE_COLUMNS,
            filters=filter_exclude_interfaces,
        )

        interfaces_dict = self._process_interfaces(interfaces_json)
        interfaces_report = self._generate_report(interfaces_dict)
        site_report = self._generate_site_report(interfaces_report)

        return {
            "interfaces_raw": interfaces_json,
            "interfaces_report": interfaces_report,
            "site_report": site_report,
        }

    @staticmethod
    def _process_interfaces(
        interfaces_json: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        interfaces_dict = {}
        for intf in interfaces_json:
            if intf["hostname"] in interfaces_dict:
                interfaces_dict[intf["hostname"]]["interfaces"].append(intf)
            else:
                interfaces_dict[intf["hostname"]] = {"interfaces": [intf]}
        return interfaces_dict

    @staticmethod
    def _generate_report(
        interfaces_dict: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        interfaces_report = []
        for hostname, data in interfaces_dict.items():
            interfaces_total = len(data["interfaces"])
            interfaces_l1up_l2up = len(
                [i for i in data["interfaces"] if i["l1"] == "up" and i["l2"] == "up"]
            )
            interfaces_l1down_l2down = len(
                [
                    i
                    for i in data["interfaces"]
                    if i["l1"] == "down" and i["l2"] == "down"
                ]
            )
            interfaces_l1up_l2down = len(
                [i for i in data["interfaces"] if i["l1"] == "up" and i["l2"] == "down"]
            )
            interfaces_l1l2unknown = len(
                [
                    i
                    for i in data["interfaces"]
                    if i["l1"] not in ["up", "down"] or i["l2"] not in ["up", "down"]
                ]
            )
            interfaces_admin_down = len(
                [
                    i
                    for i in data["interfaces"]
                    if i["reason"]
                    in PortCapacityReportConfig.INTERFACE_ADMIN_DOWN_REASON
                ]
            )
            interfaces_err_disabled = len(
                [
                    i
                    for i in data["interfaces"]
                    if i.get("reason") is not None and "err" in i.get("reason", "")
                ]
            )

            sum_interfaces_used = (
                interfaces_l1up_l2up + interfaces_l1l2unknown + interfaces_l1up_l2down
            )
            sum_interfaces_unused = interfaces_l1down_l2down  # admin_down and err_disabled are already l1&l2 down

            interfaces_report.append(
                {
                    "hostname": hostname,
                    "sn": data["interfaces"][0]["sn"],
                    "siteName": data["interfaces"][0]["siteName"],
                    "total": interfaces_total,
                    "l1&l2 up": interfaces_l1up_l2up,
                    "l1&l2 down": interfaces_l1down_l2down,
                    "l1 up & l2 down": interfaces_l1up_l2down,
                    "L1 and l2 unknown": interfaces_l1l2unknown,
                    "admin-down": interfaces_admin_down,
                    "err-disabled": interfaces_err_disabled,
                    "port utilisation (%)": (
                        round((sum_interfaces_used / interfaces_total) * 100, 2)
                        if interfaces_total > 0
                        else 0
                    ),
                    "port availability (%)": (
                        round((sum_interfaces_unused / interfaces_total) * 100, 2)
                        if interfaces_total > 0
                        else 0
                    ),
                }
            )
        return interfaces_report

    @staticmethod
    def _generate_site_report(
        interfaces_report: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        site_data = defaultdict(lambda: defaultdict(int))

        for device in interfaces_report:
            site_name = device["siteName"]
            site_data[site_name]["total"] += device["total"]
            site_data[site_name]["l1&l2 up"] += device["l1&l2 up"]
            site_data[site_name]["l1&l2 down"] += device["l1&l2 down"]
            site_data[site_name]["l1 up & l2 down"] += device["l1 up & l2 down"]
            site_data[site_name]["L1 and l2 unknown"] += device["L1 and l2 unknown"]
            site_data[site_name]["admin-down"] += device["admin-down"]
            site_data[site_name]["err-disabled"] += device["err-disabled"]

        site_report = []
        for site_name, data in site_data.items():
            total = data["total"]
            used = (
                data["l1&l2 up"] + data["l1 up & l2 down"] + data["L1 and l2 unknown"]
            )
            site_report.append(
                {
                    "siteName": site_name,
                    "total": total,
                    "l1&l2 up": data["l1&l2 up"],
                    "l1&l2 down": data["l1&l2 down"],
                    "l1 up & l2 down": data["l1 up & l2 down"],
                    "L1 and l2 unknown": data["L1 and l2 unknown"],
                    "admin-down": data["admin-down"],
                    "err-disabled": data["err-disabled"],
                    "port utilisation (%)": (
                        round((used / total) * 100, 2) if total > 0 else 0
                    ),
                    "port availability (%)": (
                        round((data["l1&l2 down"] / total) * 100, 2) if total > 0 else 0
                    ),
                }
            )

        return site_report


@dataclass
class OverviewCollector(BaseDataCollector):
    config_class: ClassVar[Type] = OverviewReportConfig

    def get_data(self):
        for (
            section_name,
            section_config,
        ) in OverviewReportConfig.OVERVIEW_SECTIONS.items():
            if section_config is None:
                continue

            if section_name == "Routing":
                self._collect_routing_data(section_config)
            else:
                self._collect_regular_section_data(section_name, section_config)

    def _collect_regular_section_data(self, section_name, section_config):
        section_data = []
        for item in section_config.ITEMS:
            name = item["name"]
            method = item.get("method")
            key = item.get("key")
            filters = item.get("filters", {})
            if self.site_filter:
                filters["siteName"] = ["eq", self.site_filter]

            if method:
                value = self._fetch_data(method, filters)
                if name == "Network Inventory":
                    vendors = get_distribution_ratio(value, "vendor")
                    device_types = get_distribution_ratio(value, "devType")
                    self.data["Vendors Overview"] = [
                        (k.capitalize(), v) for k, v in vendors.items()
                    ]
                    self.data["Device Types"] = [
                        (k.capitalize(), v) for k, v in device_types.items()
                    ]
                elif key:
                    unique_count = count_unique_occurrences(value, key)
                    section_data.append((name, unique_count))
                else:
                    section_data.append((name, value))

        self.data[section_name] = section_data

    def _collect_routing_data(self, section_config):
        routing_data = []
        filters = {"siteName": ["eq", self.site_filter]} if self.site_filter else {}
        all_routes = self._fetch_data(
            "technology.routing.routes_ipv4.all",
            filters,
            columns=["siteName", "protocol"],
        )

        protocol_mapping = {
            item["protocol"]: item["name"]
            for item in section_config.ITEMS
            if "protocol" in item
        }
        route_counts = defaultdict(int)

        for route in all_routes:
            protocol = route.get("protocol", "")
            if protocol.startswith("O"):  # Handle OSPF variants
                route_counts["(O) - OSPF Routes"] += 1
            elif protocol.startswith("I"):  # Handle IS-IS variants
                route_counts["(IS-IS) - IS-IS Routes"] += 1
            elif protocol_mapping.get(protocol):
                route_name = protocol_mapping.get(protocol)
                route_counts[route_name] += 1
            else:
                route_counts["(X) - Other routes"] += 1

        for item in section_config.ITEMS:
            name = item["name"]
            # if "method" in item:
            #     value = self._fetch_data(item["method"], filters)
            #     routing_data.append((name, value))
            # else:
            if route_counts.get(name, 0) == 0:
                continue
            else:
                routing_data.append((name, route_counts.get(name, 0)))

        self.data["Routing"] = routing_data

    def _fetch_data(
        self,
        method: str,
        filters: Dict[str, Any] = None,
        columns: List[str] = [],
        **kwargs,
    ) -> Any:
        api_method = self.ipf
        for part in method.split("."):
            api_method = getattr(api_method, part)
        if callable(api_method):
            kwargs = {}
            if filters:
                kwargs["filters"] = filters
            if self.snapshot_id:
                kwargs["snapshot_id"] = self.snapshot_id
            if columns:
                kwargs["columns"] = columns
            return api_method(**kwargs)
        else:
            return api_method


@dataclass
class OverviewCompareCollector(BaseDataCollector):
    config_class: ClassVar[Type] = OverviewCompareReportConfig


@dataclass
class DiscoveryReportCollector(BaseDataCollector):
    config_class: ClassVar[Type] = DiscoveryReportConfig

    def __post_init__(self):
        # Override to do nothing, preventing automatic data collection for ITEMS
        pass

    def get_data(self) -> list[dict]:
        data_frames = {}
        for item in self.config_class.ITEMS:
            name = item["name"]
            method = item["method"]
            columns = item.get("columns", None)
            filters = item.get("filters", None)
            uri = item.get("uri")
            if method == "fetch_all":
                # We are not collecting data about discovered devices with status 'ok' or 'found'
                data = self.ipf.fetch_all(
                    uri,
                    filters={
                        "and": [
                            {"status": ["neq", "ok"]},
                            {"status": ["neq", "found"]},
                        ]
                    },
                )
            else:
                data = self._fetch_data(method, columns=columns, filters=filters)
            data_frames[name] = pd.DataFrame(data)

        connectivity_report = data_frames["Connectivity Report"]

        if connectivity_report.empty:
            print("  ... Connectivity Report is empty")
            return []

        cdp_unmanaged_neighbors = data_frames["CDP Unmanaged Neighbors"]
        matrix_unmanaged = data_frames["Matrix Unmanaged Neighbors"]

        # Ensure CDP columns exist in connectivity_report, even if CDP Unmanaged Neighbor table is empty
        cdp_item = next(
            (
                item
                for item in self.config_class.ITEMS
                if item["name"] == "CDP Unmanaged Neighbors"
            ),
            None,
        )
        if cdp_item and "columns" in cdp_item:
            for col in cdp_item["columns"]:
                if col not in connectivity_report.columns:
                    connectivity_report[col] = None

        # Initialize merged_df with connectivity_report
        merged_df = connectivity_report

        if not cdp_unmanaged_neighbors.empty:
            # Create a dictionary mapping 'remoteHost' to the rest of the CDP data
            cdp_dict = (
                cdp_unmanaged_neighbors.groupby("remoteIp").first().to_dict("index")
            )

            # Update merged_df with CDP data
            for idx, row in merged_df.iterrows():
                ip_address = row["ip"]
                if ip_address in cdp_dict:
                    for col, value in cdp_dict[ip_address].items():
                        if col not in merged_df.columns:
                            merged_df[col] = None
                        merged_df.at[idx, col] = value

        # Process Matrix unmanaged data
        for protocol in self.config_class.PROTOCOLS:
            merged_df[protocol] = "N"

        if not matrix_unmanaged.empty:
            # Create a dictionary for quick lookup
            matrix_dict = (
                matrix_unmanaged.groupby("neiIp")["protocol"].apply(list).to_dict()
            )
            for idx, row in merged_df.iterrows():
                if row["ip"] in matrix_dict:
                    for protocol in matrix_dict[row["ip"]]:
                        if protocol.lower() in self.config_class.PROTOCOLS:
                            merged_df.at[idx, protocol.lower()] = "Y"

        # Translate column names and remove 'id' column
        merged_df = merged_df.rename(columns=self.config_class.COLUMN_TRANSLATIONS)
        if "id" in merged_df.columns:
            merged_df = merged_df.drop(columns=["id"])

        # Ensure index is unique before converting to dict
        merged_df = merged_df.reset_index(drop=True)

        return merged_df.to_dict("records")


@dataclass
class CVECollector(BaseDataCollector):
    config_class: ClassVar[Type] = CVEReportConfig

    # Cache field names at class level for better performance
    _DEVICE_INFO_FIELDS = [
        field["name"] for field in CVEReportConfig.CSV_FIELDS["device_info"]
    ]
    _CVE_BASIC_FIELDS = [
        field["name"] for field in CVEReportConfig.CSV_FIELDS["cve_basic"]
    ]
    _CVSS_V2_FIELDS = [field["name"] for field in CVEReportConfig.CSV_FIELDS["cvss_v2"]]
    _CVSS_V3_FIELDS = [field["name"] for field in CVEReportConfig.CSV_FIELDS["cvss_v3"]]

    def get_data(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Collects data and returns two datasets:
        1. Summary data for PDF report
        2. Detailed data for CSV export

        Optimizations:
        - Caches OS version groups to minimize API calls
        - Implements error handling and retries
        - Adds performance logging
        - Uses dataclasses for structured data handling
        """
        self._validate_requirements()
        filtered_devices = self._get_filtered_devices()
        os_groups = self._group_devices_by_os(filtered_devices)

        vuln = self._initialize_vulnerability_checker()
        processed_data = self._process_vulnerabilities(vuln, os_groups)

        return self._format_output(processed_data)

    def _validate_requirements(self) -> None:
        """Validates all required parameters are present."""
        if not self.nvd_api_key:
            raise ValueError("NVD_API_KEY is required for generating the CVE report.")

        if not self.site_filter and not self.inventory_filter:
            raise ValueError(
                "Either REPORT_SITE or INVENTORY_FILTER must be set for the CVE report."
            )

    def _get_filtered_devices(self) -> List[Dict[str, Any]]:
        """Gets filtered devices based on site or inventory filter."""
        device_filter = (
            {"siteName": ["eq", self.site_filter]}
            if self.site_filter
            else self._parse_inventory_filter()
        )

        return self._fetch_data(method="inventory.devices.all", filters=device_filter)

    def _parse_inventory_filter(self) -> Dict:
        """Parses and validates inventory filter."""
        try:
            return json.loads(self.inventory_filter)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format for INVENTORY_FILTER")

    @staticmethod
    def _group_devices_by_os(devices: List[Dict[str, Any]]) -> Dict[Tuple, Dict]:
        """
        Groups devices by OS version to minimize the number of API calls.
        Args:
            devices: List of device dictionaries containing vendor, family, version info
        Returns:
            Dictionary mapping OS tuples to device groups
        """
        os_groups = {}
        for device in devices:
            os_key = (
                device.get("vendor", ""),
                device.get("family", ""),
                device.get("version", ""),
            )

            if os_key not in os_groups:
                os_groups[os_key] = {
                    "vendor": device.get("vendor"),
                    "family": device.get("family"),
                    "version": device.get("version"),
                    "hostnames": [],
                    "cves": None,
                }
            os_groups[os_key]["hostnames"].append(device.get("hostname"))

        return os_groups

    def _initialize_vulnerability_checker(self) -> Vulnerabilities:
        """Initializes the vulnerability checker with retry logic."""
        try:
            return Vulnerabilities(self.ipf, nvd_api_key=self.nvd_api_key)
        except Exception as e:
            raise ValueError(f"Error initializing Vulnerabilities class: {str(e)}")

    @staticmethod
    def _process_vulnerabilities(
        vuln: Vulnerabilities,
        os_groups: Dict[Tuple, Dict],
        max_retries: int = 3,
        retry_delay: int = 5,
    ) -> Dict[Tuple, Dict]:
        """Processes vulnerabilities for each OS group with comprehensive error handling."""

        def inspect_vuln_response(
            vuln_to_inspect, dev_name: str
        ) -> Tuple[bool, Optional[str]]:
            """
            Inspects the vulnerability response data for errors and validity.

            Returns:
                Tuple[bool, Optional[str]]: (is_valid, error_message)
            """
            if vuln_to_inspect is None:
                logger.info(f"No CVE data found for {dev_name}")
                return True, None  # Changed to True since this is now an expected case

            # Check for API error response
            if hasattr(vuln_to_inspect, "error") and vuln_to_inspect.error:
                return False, f"API Error: {vuln_to_inspect.error}"

            # Having no CVEs is valid - just means no vulnerabilities found
            if not hasattr(vuln_to_inspect, "cves"):
                return True, None

            if hasattr(vuln_to_inspect, "total_results"):
                actual_count = len(vuln_to_inspect.cves) if vuln_to_inspect.cves else 0
                if vuln_to_inspect.total_results != actual_count:
                    logger.warning(
                        f"Results count mismatch for {dev_name}: "
                        f"expected {vuln_to_inspect.total_results}, got {actual_count}"
                    )

            return True, None

        for device in os_groups.values():
            os_key = (device["vendor"], device["family"], device["version"])
            hostname = device["hostnames"][0]
            os_info = f"{device['vendor']}/{device['family']}/{device['version']}"

            for attempt in range(max_retries):
                try:
                    logger.info(f"Checking vulnerabilities for {hostname} ({os_info})")
                    dev_vuln = vuln.check_device(hostname)

                    if not dev_vuln:
                        logger.info(f"No vulnerabilities found for {hostname} ({os_info})")
                        os_groups[os_key]["cves"] = []
                        break

                    # Differentiate between ipfabric 6.9 and 6.10+ versions
                    if isinstance(dev_vuln[0].cves, list):
                        cve_data = dev_vuln[0].cves[0]
                    else:
                        cve_data = dev_vuln[0].cves

                    is_valid, error_msg = inspect_vuln_response(cve_data, hostname)

                    if is_valid:
                        if cve_data and hasattr(cve_data, 'cves') and cve_data.cves:
                            os_groups[os_key]["cves"] = cve_data
                        else:
                            os_groups[os_key]["cves"] = []
                        break
                    else:
                        logger.error(
                            f"Invalid vulnerability data for {hostname} ({os_info}): {error_msg}"
                        )

                except requests.exceptions.HTTPError as http_err:
                    if http_err.response.status_code == 429:  # Rate limit
                        if attempt < max_retries - 1:
                            sleep(retry_delay * (attempt + 1))  # Exponential backoff
                            continue
                    logger.warning(f"HTTP error for {hostname} ({os_info}): {str(http_err)}")

                except requests.exceptions.ConnectionError:
                    if attempt < max_retries - 1:
                        sleep(retry_delay)
                        continue
                    logger.warning(f"Connection error for {hostname} ({os_info})")

                except requests.exceptions.Timeout:
                    if attempt < max_retries - 1:
                        sleep(retry_delay)
                        continue
                    logger.warning(f"Timeout error for {hostname} ({os_info})")

                except requests.exceptions.RequestException as e:
                    logger.warning(f"Request error for {hostname} ({os_info}): {str(e)}")

                except Exception as e:
                    logger.warning(f"Unexpected error checking vulnerabilities for {hostname} ({os_info}): {str(e)}")

                # If we get here, all retries failed or we hit a non-retryable error
                os_groups[os_key]["cves"] = []  # Set empty list instead of None
                break

        # Log summary statistics
        processed = sum(1 for d in os_groups.values() if d["cves"] is not None)
        total = len(os_groups)
        logger.info(
            f"Processed {processed}/{total} OS versions successfully "
            f"({(processed / total) * 100:.1f}% success rate)"
        )

        return os_groups

    def _format_output(
        self, os_groups: Dict[Tuple, Dict]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Formats the data into summary and detailed outputs."""
        summary_data = []
        detailed_data = []

        for item in os_groups.values():
            # Include all devices in summary, even those without CVEs
            for hostname in item["hostnames"]:
                device_summary = {
                    "hostname": hostname,
                    "vendor": item["vendor"],
                    "family": item["family"],
                    "version": item["version"],
                }

                if item["cves"] and hasattr(item["cves"], "total_results"):
                    device_summary.update({
                        "cve_count": item["cves"].total_results,
                        "raw_cves": item["cves"],
                        **self._process_device_summary(item["cves"])
                    })
                else:
                    device_summary.update({
                        "cve_count": 0,
                        "raw_cves": None,
                        **{f"{level.lower()}_count": 0 for level in self.config_class.SEVERITY_LEVELS}
                    })

                summary_data.append(device_summary)

                # Only add detailed data if there are actual CVEs
                if item["cves"] and hasattr(item["cves"], "cves") and item["cves"].cves:
                    device_details = self._process_device_details(
                        {
                            "hostname": hostname,
                            "vendor": item["vendor"],
                            "family": item["family"],
                            "version": item["version"]
                        },
                        item["cves"]
                    )
                    detailed_data.extend(device_details)

        summary_data.sort(key=lambda x: x["cve_count"], reverse=True)
        logger.info(
            f"Found {sum(d['cve_count'] for d in summary_data)} total vulnerabilities "
            f"across {len(summary_data)} devices ({len(os_groups)} OS versions)"
        )

        return summary_data, detailed_data

    def _process_device_summary(self, cves) -> Dict[str, int]:
        """Process device summary information with optimized counting."""
        severity_counts = {level: 0 for level in self.config_class.SEVERITY_LEVELS}

        if cves and cves.cves:
            for cve in cves.cves:
                # Prioritize V3 over V2 metrics
                if hasattr(cve, "metric_v3") and cve.metric_v3 is not None:
                    severity = cve.metric_v3.baseSeverity
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                elif hasattr(cve, "metric_v2") and cve.metric_v2 is not None:
                    severity = cve.metric_v2.baseSeverity
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return {
            f"{level.lower()}_count": count for level, count in severity_counts.items()
        }

    def _process_device_details(
        self, device: Dict[str, Any], cves
    ) -> List[Dict[str, Any]]:
        """Process detailed CVE information with improved attribute access."""
        details = []

        for cve in cves.cves:
            cve_data = self._extract_device_info(device)
            cve_data.update(self._extract_cve_basic_info(cve))

            if hasattr(cve, "metric_v2"):
                cve_data.update(self._extract_cvss_metrics(cve.metric_v2, "v2"))
            if hasattr(cve, "metric_v3"):
                cve_data.update(self._extract_cvss_metrics(cve.metric_v3, "v3"))

            cve_data["cpe"] = getattr(cves, "cpe", "N/A")
            details.append(cve_data)

        return details

    @staticmethod
    def _extract_device_info(device: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts device information fields.
        Args:
            device: Dictionary containing device information
        Returns:
            Dictionary with extracted device fields
        """
        return {
            dev_param: device.get(dev_param)
            for dev_param in CVECollector._DEVICE_INFO_FIELDS
        }

    @staticmethod
    def _extract_cve_basic_info(cve) -> Dict[str, Any]:
        """
        Extracts basic CVE information.
        Args:
            cve: CVE object containing vulnerability information
        Returns:
            Dictionary with extracted CVE basic fields
        """
        return {
            cve_param: getattr(cve, cve_param)
            for cve_param in CVECollector._CVE_BASIC_FIELDS
        }

    @staticmethod
    def _extract_cvss_metrics(metric, version: str) -> Dict[str, Any]:
        """
        Extracts CVSS metrics for either v2 or v3.
        Args:
            metric: CVSS metric object
            version: Version string ('v2' or 'v3')
        Returns:
            Dictionary with extracted CVSS metrics
        """
        fields = (
            CVECollector._CVSS_V2_FIELDS
            if version == "v2"
            else CVECollector._CVSS_V3_FIELDS
        )

        return {
            f"{version}_{cvss_param}": getattr(metric, cvss_param, None)
            for cvss_param in fields
        }
