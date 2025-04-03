#!/usr/bin/env python3
"""
IP Fabric Report Generator - Report Types Module.

This module defines all available report types for the IP Fabric report generator.
Each report type is implemented as a class that inherits from BaseReport and
provides specific data collection, processing, and formatting logic.

Available Report Types:
    - CVEReport: Security vulnerabilities analysis
    - DiscoveryReport: Network discovery and device analysis
    - ManagementProtocolReport: Management protocols distribution analysis
    - OverviewReport: General network overview and statistics
    - OverviewCompareReport: Comparison between snapshots
    - PortCapacityReport: Port capacity and utilization analysis
    - TrunkMismatchReport: Trunk configuration mismatch analysis

Each report type:
    - Uses a specific data collector for fetching data
    - Implements custom data processing logic
    - Provides formatted output for rendering
    - Handles report-specific configurations
    - Generates both summary and detailed data

Dependencies:
    - Data collectors for fetching IP Fabric data
    - Configuration classes for report settings
    - Utility modules for data processing and visualization
"""

# Standard library imports
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Tuple, Type, Union

# Third-party imports
import pandas as pd
from loguru import logger

# Local imports
from .config import TrunkMismatchConfig
from .data_collectors import (
    BaseDataCollector,
    CVECollector,
    DiscoveryReportCollector,
    ManagementProtocolCollector,
    OverviewCollector,
    OverviewCompareCollector,
    PerSiteSummaryCollector,
    PortCapacityCollector,
    SnapshotSummaryCollector,
    TrunkMismatchCollector,
)
from .modules import (
    get_distribution_ratio,
    plot_pie_chart,
    cleanup_connectivity_matrix,
    parse_vlans,
    format_vlans,
)


class BaseReport(ABC):
    collector_class: Type[BaseDataCollector] = None

    def __init__(
        self,
        ipf,
        export_dir: str,
        site_filter: str = None,
        nvd_api_key: str = None,
        inventory_filter: str = None,
        snapshot_id: str = "$last",
        snapshot_id_prev: str = "$prev",
    ):
        self.ipf = ipf
        self.site_filter = site_filter
        self.nvd_api_key = nvd_api_key
        self.inventory_filter = inventory_filter
        self.snapshot_id = snapshot_id
        self.snapshot_id_prev = snapshot_id_prev
        self.export_dir = export_dir

        if self.collector_class is None:
            raise ValueError("collector_class must be set in subclasses")

    def save_csv_report(
        self, data: Union[List[Dict[str, Any]], pd.DataFrame], file_name: str
    ) -> None:
        """
        Save data to a CSV file in the export directory.

        Args:
            data: List of dictionaries or pandas DataFrame to save
            file_name: Base name for the CSV file (without extension)
        """
        if not data:
            logger.info(" -- No data to save to CSV")
            return

        # Convert to DataFrame if necessary
        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_T%H-%M")
        site_suffix = f"-{self.site_filter}" if self.site_filter else ""
        csv_filepath = f"{self.export_dir}/{file_name}{site_suffix}-{timestamp}.csv"

        # Save to CSV
        df.to_csv(csv_filepath, index=False)
        logger.success(f"✔ Saving CSV file to: {csv_filepath}")

    @classmethod
    def get_report_details(cls) -> Dict[str, str]:
        """
        Get the details of the report.
        Returns:
            Dictionary containing the report details
        """
        return cls.collector_class.get_report_details()

    @abstractmethod
    def collect_data(self) -> Dict[str, Any]:
        pass

    def get_summary(self) -> Dict[str, Any]:
        """
        Get the summary data for the report.
        Returns:
            Dictionary containing the summary data
        """
        summary_data = SnapshotSummaryCollector(self.ipf)
        summary_to_dict = summary_data.return_data()
        return summary_to_dict

    def get_site_summary(self) -> Dict[str, Any]:
        """
        Get the summary data for the report per specific site.
        Returns:
            Dictionary containing the per site summary data
        """
        if not self.site_filter:
            return {}

        per_site_summary_data = PerSiteSummaryCollector(self.ipf, self.site_filter)
        site_summary_to_dict = per_site_summary_data.return_data()
        return site_summary_to_dict


class ManagementProtocolReport(BaseReport):
    collector_class = ManagementProtocolCollector

    def collect_data(self) -> Dict[str, Any]:
        mgmt_data = self.collector_class(self.ipf, site_filter=self.site_filter)
        data_dict = mgmt_data.return_data()

        mgmt_protocols = []
        for transformed_name, item in data_dict.items():
            proto_data = item.get("value", None)
            if proto_data:
                name = item["name"]
                key = item["key"]
                distribution = get_distribution_ratio(proto_data, key)
                plot = plot_pie_chart(
                    {k: v["percentage"] for k, v in distribution.items()}
                )
                mgmt_protocols.append(
                    {
                        "name": name,
                        "description": f"Distribution of configured {name} in the network.",
                        "server_name": f"{name.rstrip('s')}",
                        "distribution": distribution,
                        "plot": plot,
                    }
                )

        return {
            "network_summary": self.get_summary(),
            "report_details": self.get_report_details(),
            "mgmt_protocols": mgmt_protocols,
            "site_filter": self.site_filter,
            "site_summary": self.get_site_summary(),
        }


class PortCapacityReport(BaseReport):
    collector_class = PortCapacityCollector

    def collect_data(self) -> Dict[str, Any]:
        port_capacity_data = self.collector_class(
            self.ipf, self.site_filter, self.snapshot_id
        )
        data = port_capacity_data.get_data()
        interfaces_report = data["interfaces_report"]
        site_report = data["site_report"]

        # Sort interfaces_report and site_report by siteName
        interfaces_report.sort(key=lambda x: x["siteName"])
        site_report.sort(key=lambda x: x["siteName"])

        self.save_csv_report(interfaces_report, self.get_report_details().get("type"))

        return {
            "report_details": self.get_report_details(),
            "network_summary": self.get_summary(),
            "interfaces_report": interfaces_report,
            "site_report": site_report,
            "site_filter": self.site_filter,
            "port_summary": self._get_port_summary(interfaces_report),
            "site_summary": self.get_site_summary(),
        }

    @staticmethod
    def _get_port_summary(port_data) -> Dict[str, Any]:
        total_ports = sum(device["total"] for device in port_data)
        ports_up = sum(device["l1&l2 up"] for device in port_data)
        ports_down = sum(device["l1&l2 down"] for device in port_data)
        ports_admin_down = sum(device["admin-down"] for device in port_data)
        ports_err_disabled = sum(device["err-disabled"] for device in port_data)
        overall_utilization = (
            round((ports_up / total_ports) * 100, 2) if total_ports > 0 else 0
        )

        return {
            "Total Ports": total_ports,
            "Ports up": ports_up,
            "Ports down": ports_down,
            "Ports admin_down": ports_admin_down,
            "Err Disabled": ports_err_disabled,
            "Overall Util (%)": overall_utilization,
        }


class OverviewReport(BaseReport):
    collector_class = OverviewCollector

    def collect_data(self) -> Dict[str, Any]:
        overview_data = self.collector_class(
            self.ipf, self.site_filter, self.snapshot_id
        )
        overview_data.get_data()
        data = overview_data.return_data()

        return {
            "report_details": self.get_report_details(),
            "network_summary": self.get_summary(),
            "sections": data,
            "site_filter": self.site_filter,
            "site_summary": self.get_site_summary(),
        }


class OverviewCompareReport(BaseReport):
    collector_class = OverviewCompareCollector

    def collect_data(self) -> Dict[str, Any]:
        last_data = self._collect_snapshot_data(self.snapshot_id)
        prev_data = self._collect_snapshot_data(self.snapshot_id_prev)

        comparison_data = self._compare_data(last_data, prev_data)

        last_summary = self._collect_snapshot_data(self.snapshot_id)["Overview Summary"]
        prev_summary = self._collect_snapshot_data(self.snapshot_id_prev)[
            "Overview Summary"
        ]

        return {
            "report_details": self.get_report_details(),
            "network_summary": self.get_summary(),
            "sections": comparison_data,
            "site_filter": self.site_filter,
            "site_summary": self.get_site_summary(),
            "last_snapshot": self.snapshot_id,
            "prev_snapshot": self.snapshot_id_prev,
            "last_snapshot_summary": dict(last_summary),
            "prev_snapshot_summary": dict(prev_summary),
        }

    def _collect_snapshot_data(self, snapshot_id: str) -> Dict[str, Any]:
        overview_report = OverviewReport(self.ipf, self.site_filter, snapshot_id)
        return overview_report.collect_data()["sections"]

    @staticmethod
    def _compare_data(
        last_data: Dict[str, Any], prev_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        comparison = {}
        for section, items in last_data.items():
            comparison[section] = []
            for item_name, last_value in items:
                prev_value = next(
                    (v for n, v in prev_data[section] if n == item_name), None
                )
                if (
                    prev_value is not None
                    and isinstance(last_value, (int, float))
                    and isinstance(prev_value, (int, float))
                ):
                    delta = last_value - prev_value
                    comparison[section].append(
                        (item_name, f"{last_value} ({delta:+d})")
                    )
                elif isinstance(last_value, dict) and isinstance(prev_value, dict):
                    delta = last_value.get("count", 0) - prev_value.get("count", 0)
                    comparison[section].append(
                        (
                            item_name,
                            f"{last_value.get('count', 0)} ({delta:+d})",
                        )
                    )
        return comparison


class DiscoveryReport(BaseReport):
    collector_class = DiscoveryReportCollector

    def collect_data(self) -> Dict[str, Any]:
        collector = self.collector_class(self.ipf)
        data = collector.get_data()

        self.save_csv_report(data, self.get_report_details().get("type"))

        return {
            "network_summary": self.get_summary(),
            "report_details": self.get_report_details(),
            "sections": self._discovery_details(data),
        }

    @staticmethod
    def _discovery_details(
        data: List[Dict[str, Any]],
    ) -> Dict[str, List[Tuple[str, Any]]]:
        df = pd.DataFrame(data)

        sections = {
            "(un) Discovery Overview": [
                ("Total Unique IPs", df["IP Address"].nunique()),
                ("Total Devices", len(df)),
                ("Total Unique MAC Addresses", df["MAC Address"].nunique()),
            ],
            "Undiscovered IPs by source": [
                (source, count)
                for source, count in df["Discovery Source"].value_counts().items()
            ],
            "Detected Vendors by MAC Address": [
                (vendor, count)
                for vendor, count in df["MAC Vendor"].value_counts().items()
            ],
            "Error Type Distribution": [
                (error_type, count)
                for error_type, count in df["Error Type"].value_counts().items()
            ],
            "Discovery Status Distribution": [
                (status, count)
                for status, count in df["Discovery Status"].value_counts().items()
            ],
            "CDP Information": [
                (
                    "IPs seen with xDP",
                    df[df["xDP Remote Device"].notna()]["IP Address"].nunique(),
                ),
            ],
            "Routing Protocol Information": [
                (
                    f"IPs seen over {protocol}",
                    df[df[protocol] == "Y"]["IP Address"].nunique(),
                )
                for protocol in ["Matrix BGP", "Matrix OSPF", "Matrix EIGRP"]
            ],
        }

        return sections


class CVEReport(BaseReport):
    collector_class = CVECollector

    def collect_data(self) -> Dict[str, Any]:

        def _create_cve_details(cve_data):
            """
            Transform detailed CVE data to group by OS version with a list of CVEs under each OS.
            """
            # Handle empty data case
            if not cve_data:
                return []

            # Convert to DataFrame
            df = pd.DataFrame(cve_data)

            # First, get unique OS versions and their hostnames
            os_groups = (
                df.groupby(["vendor", "family", "version"])["hostname"]
                .agg(list)
                .reset_index()
            )

            # Create the transformed data
            transformed_data = []

            for _, os_group in os_groups.iterrows():
                # Get all CVEs for this OS version
                os_cves = df[
                    (df["vendor"] == os_group["vendor"])
                    & (df["family"] == os_group["family"])
                    & (df["version"] == os_group["version"])
                ].drop_duplicates(subset=["cve_id"])

                # Create OS entry with hostname list and CVEs
                os_entry = {
                    "vendor": os_group["vendor"],
                    "family": os_group["family"],
                    "version": os_group["version"],
                    "hostname_list": list(
                        set(os_group["hostname"])
                    ),  # removes duplicates
                    "cves": os_cves.drop(
                        ["hostname", "vendor", "family", "version"], axis=1
                    ).to_dict("records"),
                }

                transformed_data.append(os_entry)

            return transformed_data

        def _create_stats(stats_data):
            """
            Generate summary statistics for the CVE report.
            """
            # Handle empty data case
            if not stats_data:
                return {
                    'total_cves': 0,
                    'critical_high_cves': 0,
                    'avg_cvss_score': 0.0,
                    'severity_stats': [
                        {
                            'level': severity,
                            'count': 0,
                            'percentage': 0.0
                        }
                        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
                    ]
                }

            # Convert to DataFrame
            severity_data = pd.DataFrame(stats_data)
            total_cves = len(severity_data)
            
            return {
                'total_cves': total_cves,
                'critical_high_cves': len(severity_data[severity_data['v3_baseSeverity'].isin(['CRITICAL', 'HIGH'])]),
                'avg_cvss_score': float(severity_data['v3_baseScore'].mean()) if not severity_data.empty else 0.0,
                'severity_stats': [
                    {
                        'level': severity,
                        'count': len(severity_data[severity_data['v3_baseSeverity'] == severity]),
                        'percentage': round(
                            len(severity_data[severity_data['v3_baseSeverity'] == severity]) / total_cves * 100, 1
                        ) if total_cves > 0 else 0.0
                    }
                    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
                ],
            }

        # Initialize the collector and fetch data
        collector = self.collector_class(
            self.ipf, self.site_filter, self.nvd_api_key, self.inventory_filter
        )
        cve_summary, cve_details = collector.get_data()

        # Generate CSV report with detailed data
        self.save_csv_report(cve_details, self.get_report_details().get("type"))

        return {
            "report_details": self.get_report_details(),
            "network_summary": self.get_summary(),
            "cve_summary": cve_summary,
            "cve_details": _create_cve_details(cve_details),
            "site_filter": self.site_filter,
            "site_summary": self.get_site_summary(),
            **_create_stats(cve_details),
        }


class TrunkMismatchReport(BaseReport):
    collector_class = TrunkMismatchCollector

    def collect_data(self) -> Dict[str, Any]:
        logger.info("Collecting data for Trunk Mismatch Report...")
        trunk_data = self.collector_class(
            self.ipf, site_filter=self.site_filter, snapshot_id=self.snapshot_id
        )

        data_dict = trunk_data.return_data()
        trunk_switchport_df = data_dict["trunk_switchport"]["value"]

        if trunk_switchport_df.empty:
            raise ValueError("No trunk ports found in the network.")

        stp_virtual_ports_df = data_dict["stp_virtual_ports"]["value"]
        connectivity_matrix_l2_df = data_dict["connectivity_matrix_l2"]["value"]
        inconsistencies_df = data_dict["inconsistent_trunk_links"]["value"]

        logger.info("Analysing data for Trunk Mismatch Report...")
        
        # Remove duplicate from connectivity_matrix_l2_df:
        connectivity_matrix_l2_df = cleanup_connectivity_matrix(connectivity_matrix_l2_df)
        # DO NOT USE the drop_duplicates() BELOW, IT DOESN'T RETURN the EXPECTED RESULTs, use the cleanup_connectivity_matrix function
        # conn_matrix_dedup_df = connectivity_matrix_l2_df.drop_duplicates(subset=["localHost", "localInt", "remoteHost", "remoteInt"])

        # Add the trunk information to connecitvity matrix, and remove the non trunk entries
        trunk_vlans_full_df = self.merge_connectivity_matrix_trunk_info(connectivity_matrix_l2_df, trunk_switchport_df)

        # STP VIRTUAL PORTS - Find which VLANS are missing on either side of the trunk
        # this will also highlight any missing VLANs on the device, and not just on the switchport configuration
        # --> merge_full_trunk_stp_virtual_ports
        trunk_vlans_stp_full_df = self.merge_full_trunk_stp_virtual_ports(
            trunk_vlans_full_df=trunk_vlans_full_df,
            stp_virtual_ports_df=stp_virtual_ports_df,
        )
        trunk_vlans_stp_summary_df = trunk_vlans_stp_full_df[
            (
                trunk_vlans_stp_full_df["missingStpVlansLocal"].notna()
                & (trunk_vlans_stp_full_df["missingStpVlansLocal"] != "")
            )
            | (
                trunk_vlans_stp_full_df["missingStpVlansRemote"].notna()
                & (trunk_vlans_stp_full_df["missingStpVlansRemote"] != "")
            )
        ]

        # SWITCHPORT CONFIGURATION - Find which VLANS are missing on either side of the trunk
        trunk_vlans_allowed_full_df = self.check_vlan_remote_local(
            connectivity_matrix_df=trunk_vlans_full_df
        )
        trunk_vlans_allowed_summary_df = trunk_vlans_allowed_full_df[
            (
                trunk_vlans_allowed_full_df["missingAllowedVlansLocal"].notna()
                & (trunk_vlans_allowed_full_df["missingAllowedVlansLocal"] != "")
            )
            | (
                trunk_vlans_allowed_full_df["missingAllowedVlansRemote"].notna()
                & (trunk_vlans_allowed_full_df["missingAllowedVlansRemote"] != "")
            )
        ]

        # Generate the report
        merge_keys = ["localHost", "localInt", "remoteHost", "remoteInt"]

        full_df = (
            trunk_vlans_allowed_full_df.set_index(merge_keys)
            .combine_first(trunk_vlans_stp_full_df.set_index(merge_keys))
            .reset_index()
        )
        summary_df = (
            trunk_vlans_allowed_summary_df.set_index(merge_keys)
            .combine_first(trunk_vlans_stp_summary_df.set_index(merge_keys))
            .reset_index()
        )

        return {
            "report_details": self.get_report_details(),
            "network_summary": self.get_summary(),
            "site_filter": self.site_filter,
            "site_summary": self.get_site_summary(),
            "trunk_mismatch_report": self._reorder_columns_perdev(summary_df),
            "full_trunk_report": self._reorder_columns_full(full_df),
            "trunk_mismatch_summary_pdf": self._reorder_columns_summary_pdf(summary_df),
            "trunk_mismatch_details_pdf": inconsistencies_df,
        }

    @staticmethod
    def merge_connectivity_matrix_trunk_info(
        connectivity_matrix_df: pd.DataFrame, trunk_switchport_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merges the trunk information to the deduplicated Connectivity Matrix.

        Args:
            connectivity_matrix_df: The Connectivity Matrix DataFrame.
            trunk_switchport_df: The Dataframe of trunk ports, from the switchport table of IP Fabric

        Returns:
            df: The Connectivity Matrix DataFrame with the trunk information.
        """

        # Create a mapping between device,interface and their trunkVlan
        trunk_map = dict(
            zip(
                zip(
                    trunk_switchport_df["hostname"],
                    trunk_switchport_df["intName"],
                ),
                trunk_switchport_df["trunkVlan"],
            )
        )

        # Add local trunk VLAN columns
        connectivity_matrix_df["localTrunkVlan"] = connectivity_matrix_df.apply(
            lambda row: trunk_map.get((row["localHost"], row["localInt"])),
            axis=1,
        )

        # Add remote trunk VLAN columns
        connectivity_matrix_df["remoteTrunkVlan"] = connectivity_matrix_df.apply(
            lambda row: trunk_map.get((row["remoteHost"], row["remoteInt"])),
            axis=1,
        )

        # Filter out rows where EITHER local or remote trunk VLAN is None or empty
        return connectivity_matrix_df[
            (
                connectivity_matrix_df["localTrunkVlan"].notna()
                & (connectivity_matrix_df["localTrunkVlan"] != "")
            )
            & (
                connectivity_matrix_df["remoteTrunkVlan"].notna()
                & (connectivity_matrix_df["remoteTrunkVlan"] != "")
            )
        ]

    @staticmethod
    def merge_full_trunk_stp_virtual_ports(
        trunk_vlans_full_df: pd.DataFrame,
        stp_virtual_ports_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Efficiently merges STP Virtual Ports information to the full trunk DataFrame.

        Args:
            trunk_vlans_full_df: The full trunk DataFrame.
            stp_virtual_ports_df: The STP Virtual Ports DataFrame.

        Returns:
            DataFrame with STP Virtual Ports missing VLANs information.
        """
        # Precompute STP port mappings
        stp_ports_map = (
            stp_virtual_ports_df.groupby(["hostname", "intName"])["vlanId"]
            .apply(set)
            .to_dict()
        )

        df = trunk_vlans_full_df.copy()

        def calculate_missing_vlans(row):
            local_stp_vlans = stp_ports_map.get(
                (row["localHost"], row["localInt"]), set()
            )
            remote_stp_vlans = stp_ports_map.get(
                (row["remoteHost"], row["remoteInt"]), set()
            )

            # Only calculate if both local and remote hosts are known
            if local_stp_vlans or remote_stp_vlans:
                missing_local = list(remote_stp_vlans - local_stp_vlans)
                missing_remote = list(local_stp_vlans - remote_stp_vlans)

                return (
                    format_vlans(missing_local) if missing_local else None,
                    format_vlans(missing_remote) if missing_remote else None,
                )

            return None, None

        # Apply the calculation
        df[["missingStpVlansLocal", "missingStpVlansRemote"]] = df.apply(
            calculate_missing_vlans, axis=1, result_type="expand"
        )

        return df

    @staticmethod
    def check_vlan_remote_local(connectivity_matrix_df: pd.DataFrame):
        """
        Check the VLANs on the remote and local side of the trunk.

        Args:
            connectivity_matrix_df: The Connectivity Matrix unique DataFrame.

        Returns:
            DataFrame with missing/matching VLANs information.
        """

        def process_trunk_vlans(row):
            # Skip if either trunk VLAN is missing
            if pd.isna(row["localTrunkVlan"]) or pd.isna(row["remoteTrunkVlan"]):
                return pd.Series(
                    {
                        "missingAllowedVlansLocal": None,
                        "missingAllowedVlansRemote": None,
                        "nonMissingVlans": None,
                    }
                )

            # Parse VLANs
            local_vlans = set(parse_vlans(row["localTrunkVlan"]))
            remote_vlans = set(parse_vlans(row["remoteTrunkVlan"]))

            # Calculate missing and matching VLANs
            missing_vlans_local = list(remote_vlans - local_vlans)
            missing_vlans_remote = list(local_vlans - remote_vlans)
            matching_vlans = list(local_vlans & remote_vlans)

            return pd.Series(
                {
                    "missingAllowedVlansLocal": format_vlans(missing_vlans_local),
                    "missingAllowedVlansRemote": format_vlans(missing_vlans_remote),
                    "nonMissingVlans": format_vlans(matching_vlans),
                }
            )

        # Create a copy of the DataFrame
        df = connectivity_matrix_df.copy()

        # Apply the VLAN processing
        df[
            [
                "missingAllowedVlansLocal",
                "missingAllowedVlansRemote",
                "nonMissingVlans",
            ]
        ] = df.apply(process_trunk_vlans, axis=1)

        return df

    @staticmethod
    def _reorder_columns_full(df: pd.DataFrame) -> pd.DataFrame:
        df = df[TrunkMismatchConfig.FULL_REPORT_COLUMNS].copy()
        return df

    @staticmethod
    def _reorder_columns_perdev(df: pd.DataFrame) -> pd.DataFrame:
        df = df[TrunkMismatchConfig.SUMMARY_REPORT_COLUMNS].copy()
        return df

    @staticmethod
    def _reorder_columns_summary_pdf(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate and reorder columns for the summary report.
        Returns a DataFrame with one row per device showing total affected ports.
        """
        # Group by device and site, count the affected ports
        summary_df = (
            df.groupby(["localHost", "siteName"])
            .size()
            .reset_index(name="affected_ports")
        )

        # Sort by number of affected ports (descending) and then by hostname
        summary_df = summary_df.sort_values(
            ["affected_ports", "localHost"], ascending=[False, True]
        )

        # Add severity based on affected ports count
        def get_severity(count):
            if count >= 5:
                return "CRITICAL"
            elif count >= 3:
                return "WARNING"
            return "NORMAL"

        summary_df["severity"] = summary_df["affected_ports"].apply(get_severity)

        return summary_df

    @staticmethod
    def _reorder_columns_details_pdf(df: pd.DataFrame) -> pd.DataFrame:
        """
        Reorder columns for the detailed report.
        """
        columns = [
            "localHost",  # Local Device
            "localInt",  # Local Interface
            "localTrunkVlan",  # Local VLANs
            "remoteTrunkVlan",  # Remote VLANs
            "remoteInt",  # Remote Interface
            "remoteHost",  # Remote Device
        ]

        # Reorder columns and handle any missing columns
        df = df[columns]

        # Sort by local hostname and interface
        df = df.sort_values(["localHost", "localInt"])

        # Replace None/NaN with "None" string for better display
        df = df.fillna("None")

        return df
