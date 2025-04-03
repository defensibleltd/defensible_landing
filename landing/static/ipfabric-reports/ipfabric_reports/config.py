#!/usr/bin/env python3
"""
IP Fabric Report Generator - Configuration Module.

This module defines configuration classes for all report types in the IP Fabric
report generator. It contains settings, constants, and configuration parameters
that control report generation behavior.

Configuration Classes:
    ConfigBase: Base configuration class with common attributes
    ReportStyleConfig: Visual styling and chart colors
    NetworkSummaryConfig: Network summary report settings
    ManagementProtocolConfig: Management protocol report configuration
    PortCapacityReportConfig: Port capacity analysis settings
    OverviewReportConfig: Network overview report configuration
    OverviewCompareReportConfig: Snapshot comparison settings
    DiscoveryReportConfig: Discovery report parameters
    CVEReportConfig: Vulnerability report configuration

Each config class defines:
    - Report type identifier
    - Report name
    - Required data fields
    - Introduction text
    - Data collection parameters
    - Display settings
    - Processing rules

Usage:
    Configurations are used by their corresponding report types
    to control data collection, processing, and presentation.
"""

# Standard library imports
from typing import Any, Dict, List


class ConfigBase:
    REPORT_TYPE: str = ""
    REPORT_NAME: str = ""
    REPORT_DESCRIPTION: str = ""
    REPORT_INTRO: List[str] = []
    ITEMS: List[Dict[str, Any]] = []

    @classmethod
    def get_items(cls) -> List[Dict[str, Any]]:
        return cls.ITEMS

    @classmethod
    def get_attribute(cls, attr: str) -> List[Any]:
        return [item[attr] for item in cls.ITEMS if attr in item]


class NetworkSummaryConfig(ConfigBase):
    ITEMS: List[Dict[str, str]] = [
        {"name": "IP Fabric URL", "method": "base_url"},
        {"name": "IP Fabric Version", "method": "os_version"},
        {"name": "Snapshot Name", "method": "snapshot.name"},
        {"name": "Snapshot ID", "method": "snapshot_id"},
        {"name": "Network sites/groups", "method": "inventory.sites.count"},
        {"name": "Network devices", "method": "inventory.devices.count"},
    ]


class PerSiteSummaryConfig(ConfigBase):
    ITEMS: List[Dict[str, str]] = [
        {"name": "Network devices", "method": "inventory.devices.count"},
        {"name": "Network interfaces", "method": "inventory.interfaces.count"},
        {
            "name": "Unique VLANs",
            "method": "technology.vlans.site_summary.all",
            "key": "vlanId",
        },
        {
            "name": "Unique VRFs",
            "method": "technology.routing.vrf_detail.all",
            "key": "vrf",
        },
        {
            "name": "Managed Networks",
            "method": "technology.managed_networks.networks.count",
        },
        {"name": "Network endpoints", "method": "inventory.hosts.count"},
        {
            "name": "ARP Entries",
            "method": "technology.addressing.arp_table.count",
        },
        {
            "name": "IPv4 Routes",
            "method": "technology.routing.routes_ipv4.count",
        },
        {
            "name": "IPv6 Routes",
            "method": "technology.routing.routes_ipv6.count",
        },
    ]


class ManagementProtocolConfig(ConfigBase):
    REPORT_NAME = "Management Protocols Distribution"
    REPORT_TYPE = "management-protocol"
    REPORT_DESCRIPTION = "Report showing the distribution of management protocols across the network or site."
    REPORT_INTRO = [
        "The Management Protocols PDF report provides an overview of the distribution of management protocols"
        " servers in the network. The data was collected using IP Fabric's SDK and includes information about the"
        " following management protocols: SNMP, NTP, sFlow, NetFlow, Syslog, AAA, and DNS.",
        "The report includes a pie chart for each management protocol section that shows the percentage"
        " of servers using each protocol. The table for distribution details provides more granular information"
        " about the distribution of servers' IPs.",
        "This report can be used to identify potential areas for improvement in the network's management"
        " infrastructure. For example, if a particular management protocol is not being used by many servers,"
        " it may be possible to decommission the servers that are running that protocol.",
    ]
    ITEMS: List[Dict[str, str]] = [
        {
            "name": "AAA Tacacs Servers",
            "key": "ip",
            "method": "technology.management.aaa_servers.all",
            "filters": {"protocol": ["like", "tac"]},
        },
        {
            "name": "AAA Radius Servers",
            "key": "ip",
            "method": "technology.management.aaa_servers.all",
            "filters": {"protocol": ["like", "rad"]},
        },
        {
            "name": "NTP Sources",
            "key": "source",
            "method": "technology.management.ntp_sources.all",
        },
        {
            "name": "Syslog Servers",
            "key": "host",
            "method": "technology.management.logging_remote.all",
        },
        {
            "name": "SNMP Trap Hosts",
            "key": "dstHost",
            "method": "technology.management.snmp_trap_hosts.all",
        },
        {
            "name": "NetFlow Collectors",
            "key": "collector",
            "method": "technology.management.netflow_collectors.all",
        },
        {
            "name": "sFlow Collectors",
            "key": "collector",
            "method": "technology.management.sflow_collectors.all",
        },
        {
            "name": "DNS Resolvers",
            "key": "ip",
            "method": "technology.management.dns_resolver_servers.all",
        },
    ]


class PortCapacityReportConfig(ConfigBase):
    REPORT_NAME = "Port Capacity"
    REPORT_TYPE = "port-capacity"
    REPORT_DESCRIPTION = (
        "Report showing the capacity of active network ports in the network or site."
    )
    REPORT_INTRO = [
        "The Port Capacity Report provides an overview of the port utilization and availability across your"
        " network devices. This report includes information about the status of ports, including those that"
        " are up, down, administratively down, or in an error state.",
        "The report includes a summary table showing overall network port statistics and a detailed table"
        " breaking down port status for each device in the network.",
        "This report can be used to identify potential capacity issues, underutilized devices, and areas"
        " where port optimization might be necessary.",
    ]
    INTERFACE_ADMIN_DOWN_REASON = [
        "admin",
        "admin-down",
        "parent-admin-down",
        "disable",
        "disabled",
    ]
    EXCLUDE_INTF_NAME = (
        r"^(ae|bond|dock|ifb|lo|lxc|mgm|npu\d+_vl|oob|po|ssl|tep|tu|ucse|unb|veth|virtu|vl|vxl|wan"
        r"|/Common/)|\.\d+"
    )
    INTERFACE_COLUMNS = [
        "hostname",
        "sn",
        "intName",
        "siteName",
        "l1",
        "l2",
        "reason",
        "dscr",
        "mac",
        "duplex",
        "speed",
        "bandwidth",
        "speedValue",
        "speedType",
        "media",
        "errDisabled",
        "mtu",
        "primaryIp",
        "hasTransceiver",
        "transceiverType",
    ]


class OverviewSummaryConfig(ConfigBase):
    ITEMS = [
        {"name": "Network Sites", "method": "inventory.sites.count"},
        {"name": "Network Devices", "method": "inventory.devices.count"},
        {"name": "Network Hosts", "method": "inventory.hosts.count"},
        {"name": "Network Interfaces", "method": "inventory.interfaces.count"},
        {"name": "Network Inventory", "method": "inventory.devices.all"},
    ]


class InterfaceConfig(ConfigBase):
    ITEMS = [
        {
            "name": "Active Interfaces",
            "method": "snapshot.interface_active_count",
        },
        {"name": "Edge Interfaces", "method": "snapshot.interface_edge_count"},
        {
            "name": "Switchports",
            "method": "technology.interfaces.switchport.count",
        },
        {
            "name": "Port Channels",
            "method": "technology.port_channels.member_status_table.count",
        },
        {
            "name": "IPv4 Tunnels",
            "method": "technology.interfaces.tunnels_ipv4.count",
        },
        {
            "name": "IPv6 Tunnels",
            "method": "technology.interfaces.tunnels_ipv6.count",
        },
        {
            "name": "IPv4 Interfaces",
            "method": "technology.addressing.managed_ip_ipv4.count",
        },
        {
            "name": "IPv6 Interfaces",
            "method": "technology.addressing.managed_ip_ipv6.count",
        },
    ]


class SecurityConfig(ConfigBase):
    ITEMS = [
        {
            "name": "IPsec Gateways",
            "method": "technology.security.ipsec_gateways.count",
        },
        {
            "name": "IPsec Tunnels",
            "method": "technology.security.ipsec_tunnels.count",
        },
    ]


class NetworkConfig(ConfigBase):
    ITEMS = [
        {
            "name": "Unique VRFs",
            "method": "technology.routing.vrf_detail.all",
            "key": "vrf",
        },
        {
            "name": "Managed Networks",
            "method": "technology.managed_networks.networks.count",
        },
        {
            "name": "ARP Entries",
            "method": "technology.addressing.arp_table.count",
        },
    ]


class SwitchingConfig(ConfigBase):
    ITEMS = [
        {
            "name": "Unique VLANs",
            "method": "technology.vlans.site_summary.all",
            "key": "vlanId",
        },
        {
            "name": "Unique STP VLANs",
            "method": "technology.stp.vlans.all",
            "key": "vlanId",
        },
        {"name": "STP Bridges", "method": "technology.stp.bridges.count"},
        {"name": "STP Virtual Ports", "method": "technology.stp.ports.count"},
        {
            "name": "Unique STP Instances by rootId",
            "method": "technology.stp.instances.all",
            "key": "rootId",
        },
        {"name": "STP Neighbors", "method": "technology.stp.neighbors.count"},
        {
            "name": "Detected MAC Addresses",
            "method": "technology.addressing.mac_table.count",
        },
    ]


class TrunkMismatchConfig(ConfigBase):
    REPORT_NAME = "Trunk Links Mismatch Analysis"
    REPORT_TYPE = "trunk-mismatch"
    REPORT_DESCRIPTION = (
        "Report to show the Vlan(s) mismatch for all the trunk ports  "
        "using the information from switchport (config) and spanning-tree tables."
    )
    REPORT_INTRO = [
        "The Trunk Links Mismatch Analysis report provides a comprehensive assessment of VLAN trunk misconfigurations "
        "across your network infrastructure. The data is collected using IP Fabric's SDK to identify inconsistencies "
        "between connected trunk ports that could impact network connectivity.",
        "This report includes detailed statistics about affected devices, their severity levels based on the number "
        "of mismatched ports, and specific VLAN mismatches on each trunk link. It can be used to identify potential "
        "network segmentation issues, troubleshoot connectivity problems, and ensure consistent VLAN configurations "
        "across trunk links.",
        "The analysis categorizes mismatches into severity levels (CRITICAL: 5+ affected ports, WARNING: "
        "3-4 affected ports, NORMAL: 1-2 affected ports) and provides actionable insights by showing exact "
        "VLAN mismatches between connected interfaces, enabling network administrators to quickly identify "
        "and resolve configuration discrepancies.",
    ]
    ITEMS: List[Dict[str, str]] = [
        {
            "name": "Trunk Switchport",
            "method": "technology.interfaces.switchport.all",
            "filters": {"edge": ["eq", False], "mode": ["like", "trunk"]},
            "export": "df",
        },
        {
            "name": "STP Virtual Ports",
            "method": "technology.stp.ports.all",
            "export": "df",
        },
        {
            "name": "Connectivity Matrix L2",
            "method": "technology.interfaces.connectivity_matrix.all",
            "filters": {"protocol": ["eq", "stp"]},
            "export": "df",
        },
        {
            "name": "Inconsistent Trunk Links",
            "method": "technology.stp.inconsistencies_ports_vlan_mismatch.all",
            "export": "df",
        },
    ]

    FULL_REPORT_COLUMNS = [
        "siteName",
        "localHost",
        "localInt",
        "localTrunkVlan",
        "missingAllowedVlansLocal",
        "missingStpVlansLocal",
        "localMedia",
        "remoteMedia",
        "missingAllowedVlansRemote",
        "missingStpVlansRemote",
        "remoteTrunkVlan",
        "remoteInt",
        "remoteHost",
        "nonMissingVlans",
    ]

    SUMMARY_REPORT_COLUMNS = [
        "localHost",
        "localInt",
        "remoteInt",
        "remoteHost",
        "localTrunkVlan",
        "remoteTrunkVlan",
        "missingAllowedVlansLocal",
        "missingAllowedVlansRemote",
        "missingStpVlansLocal",
        "missingStpVlansRemote",
    ]


class RoutingConfig(ConfigBase):
    ITEMS = [
        {
            "name": "IPv4 Routes",
            "method": "technology.routing.routes_ipv4.count",
        },
        {
            "name": "IPv6 Routes",
            "method": "technology.routing.routes_ipv6.count",
        },
        {"name": "(A) - Attached Routes", "protocol": "A"},
        {"name": "(B) - BGP Routes", "protocol": "B"},
        {"name": "(C) - Connected Routes", "protocol": "C"},
        {"name": "(D) - EIGRP Routes", "protocol": "D"},
        {"name": "(IS-IS) - IS-IS Routes", "protocol": "IS-IS"},
        {"name": "(L) - Local Routes", "protocol": "L"},
        {"name": "(LDP) - MPLS Routes", "protocol": "LDP"},
        {"name": "(O) - OSPF Routes", "protocol": "O"},
        {"name": "(OMP) - OMP Routes", "protocol": "omp"},
        {"name": "(R) - RIP Routes", "protocol": "R"},
        {"name": "(S) - Static Routes", "protocol": "S"},
        {"name": "(V) - VPN Routes", "protocol": "V"},
        {"name": "(X) - Other routes", "protocol": "X"},
        {
            "name": "Multicast Routes",
            "method": "technology.multicast.mroute_table.count",
        },
    ]


class WirelessConfig(ConfigBase):
    ITEMS = [
        {
            "name": "Wireless Controllers",
            "method": "technology.wireless.controllers.count",
        },
        {
            "name": "Wireless Access Points",
            "method": "technology.wireless.access_points.count",
        },
        {
            "name": "Wireless Clients",
            "method": "technology.wireless.clients.count",
        },
    ]


class OverviewReportConfig(ConfigBase):
    REPORT_NAME = "Network Data Overview"
    REPORT_TYPE = "overview"
    REPORT_DESCRIPTION = (
        "Report providing summary data for available sections "
        "(Vendors, Device Types, Interfaces, etc)."
    )
    REPORT_INTRO = [
        "The Network Overview Report provides a comprehensive snapshot of your network's current state. This report"
        " includes key information about network devices, interfaces, addressing, switching, routing,"
        " and wireless infrastructure.",
        "The report includes summary tables showing overall network statistics and detailed breakdowns of various "
        "network aspects.",
        "This report can be used to gain a quick understanding of your network's size and complexity, identify areas "
        "of focus for optimization, and track changes over time.",
    ]
    OVERVIEW_SECTIONS = {
        "Overview Summary": OverviewSummaryConfig,
        "Vendors Overview": None,
        "Device Types": None,
        "Interfaces": InterfaceConfig,
        "Security": SecurityConfig,
        "Network": NetworkConfig,
        "Switching": SwitchingConfig,
        "Routing": RoutingConfig,
        "Wireless": WirelessConfig,
    }


class OverviewCompareReportConfig(ConfigBase):
    REPORT_NAME = "Overview Data Comparison"
    REPORT_TYPE = "overview-compare"
    REPORT_DESCRIPTION = (
        "Report comparing two IP Fabric snapshots based on Overview Report."
    )
    REPORT_INTRO = [
        "The Network Overview Comparison Report provides a comprehensive comparison of your network's state between"
        " two snapshots. This report includes key information about changes in network devices, interfaces,"
        " addressing, switching, routing, and wireless infrastructure.",
        "The report includes summary tables showing overall network statistics and detailed breakdowns of various"
        " network aspects, highlighting the differences between the two snapshots.",
        "This report can be used to gain a quick understanding of your network's changes over time, identify trends,"
        " and track the impact of network modifications.",
    ]


class DiscoveryReportConfig(ConfigBase):
    REPORT_NAME = "Undiscovered Network Elements"
    REPORT_TYPE = "discovery"
    REPORT_DESCRIPTION = (
        "Report combining undiscovered IPs from Connectivity Report "
        "with CDP/LLDP unmanaged neighbors,and matrix unmanaged neighbors."
    )
    REPORT_INTRO = [
        "The Discovery Report provides a comprehensive overview of the IP Fabric Discovery process results, with"
        " a primary focus on undiscovered IP addresses within your network. This report combines data from"
        " the discovery process with additional context from various network tables to provide a detailed"
        " analysis of potential network blind spots.",
        "Key components of this report include:",
        "<strong>Discovery Results:</strong> Presents a summary of the IP addresses that were not successfully"
        " discovered during the network scanning process, including error types and discovery statuses.",
        "<strong>Connectivity Context:</strong> Enriches the discovery data with information from the Connectivity"
        " Report, providing additional insights into why certain IP addresses may not have been discovered.",
        "<strong>CDP/LLDP Context:</strong> Incorporates data from CDP (Cisco Discovery Protocol) and LLDP (Link"
        " Layer Discovery Protocol) to identify any undiscovered devices that are known to their neighbors"
        " but not directly accessible during the discovery process.",
        "<strong>Routing Protocols Context:</strong> Utilizes data from routing protocols (such as BGP, OSPF,"
        " and EIGRP) to highlight undiscovered IP addresses that are part of the routing tables but not"
        " directly discoverable.",
        "This report is designed to help network administrators and engineers:</br>"
        "<ul>"
        "<li>Identify and investigate IP addresses that could not be discovered during the network scanning"
        " process.</li>"
        "<li>Understand the reasons behind discovery failures, whether they are due to access issues,"
        " misconfigurations, or other factors.</li>"
        "<li>Discover potential security risks or misconfigurations in the network by highlighting devices"
        " that are known to exist (through CDP/LLDP or routing tables) but could not be directly accessed.</li>"
        "<li>Improve the overall network discovery process by providing insights into areas that may require"
        " additional attention or configuration changes.</li>"
        "</ul>",
    ]
    ITEMS: List[Dict[str, str]] = [
        {
            "name": "Connectivity Report",
            "method": "fetch_all",
            "uri": "tables/reports/discovery-tasks",
        },
        {
            "name": "CDP Unmanaged Neighbors",
            "method": "technology.neighbors.neighbors_unmanaged.all",
            "columns": [
                "localHost",
                "localInt",
                "remoteInt",
                "remoteHost",
                "remoteIp",
                "remoteIpv6List",
                "capabilities",
            ],
        },
        {
            "name": "Matrix Unmanaged Neighbors",
            "method": "technology.interfaces.connectivity_matrix_unmanaged_neighbors_detail.all",
            "columns": ["neiIp", "protocol"],
            "filters": {"and": [{"protocol": ["reg", "bgp|ospf|eigrp"]}]},
        },
    ]
    PROTOCOLS = ["ospf", "bgp", "eigrp"]
    COLUMN_TRANSLATIONS = {
        "attemptCount": "Attempts",
        "errorReasons": "Error Reasons",
        "dnsName": "DNS Name",
        "hasLogFile": "Log File",
        "errorType": "Error Type",
        "mac": "MAC Address",
        "objectId": "Object ID",
        "slug": "API Slug",
        "ip": "IP Address",
        "errorMessage": "Error Message",
        "source": "Discovery Source",
        "context": "Virtual Context",
        "vendor": "MAC Vendor",
        "status": "Discovery Status",
        "localHost": "xDP Local Device",
        "localInt": "xDP Local Interface",
        "remoteInt": "xDP Remote Interface",
        "remoteHost": "xDP Remote Device",
        "remoteIp": "xDP Remote IP",
        "remoteIpv6List": "xDP Remote IPv6",
        "capabilities": "xDP Capabilities",
        "ospf": "Matrix OSPF",
        "bgp": "Matrix BGP",
        "eigrp": "Matrix EIGRP",
    }


class CVEReportConfig(ConfigBase):
    REPORT_NAME = "Common Vulnerabilities and Exposures (CVE)"
    REPORT_TYPE = "cve"
    REPORT_DESCRIPTION = (
        "Report showing CVE vulnerabilities for network devices in a specific site."
    )
    REPORT_INTRO = [
        "The CVE Vulnerability report provides a comprehensive analysis of potential security vulnerabilities"
        " in network devices based on their operating system versions. The data is collected using IP Fabric's"
        " SDK and enriched with vulnerability information from the National Vulnerability Database (NVD).",
        "This report includes detailed information about each device's operating system, known vulnerabilities,"
        " and their severity levels. It can be used to identify potential security risks and prioritize system"
        " updates or patches.",
        "The analysis covers vendor-specific vulnerabilities and provides actionable insights for maintaining"
        " network security.",
    ]

    # CSV Data Structure
    CSV_FIELDS = {
        "device_info": [
            {"name": "hostname", "description": "Device hostname"},
            {"name": "vendor", "description": "Device vendor"},
            {"name": "family", "description": "Device family"},
            {"name": "version", "description": "OS version"},
        ],
        "cve_basic": [
            {"name": "cve_id", "description": "CVE identifier"},
            {"name": "description", "description": "CVE description"},
            {"name": "url", "description": "Reference URL"},
        ],
        "cvss_v2": [
            {"name": "version", "description": "CVSS version"},
            {"name": "baseScore", "description": "Base score"},
            {"name": "baseSeverity", "description": "Severity rating"},
            {"name": "accessVector", "description": "Access vector"},
            {"name": "accessComplexity", "description": "Access complexity"},
            {
                "name": "confidentialityImpact",
                "description": "Confidentiality impact",
            },
            {"name": "integrityImpact", "description": "Integrity impact"},
            {
                "name": "availabilityImpact",
                "description": "Availability impact",
            },
            {
                "name": "exploitabilityScore",
                "description": "Exploitability score",
            },
            {"name": "impactScore", "description": "Impact score"},
        ],
        "cvss_v3": [
            {"name": "version", "description": "CVSS version"},
            {"name": "baseScore", "description": "Base score"},
            {"name": "baseSeverity", "description": "Severity rating"},
            {"name": "attackVector", "description": "Attack vector"},
            {"name": "attackComplexity", "description": "Attack complexity"},
            {
                "name": "privilegesRequired",
                "description": "Required privileges",
            },
            {"name": "userInteraction", "description": "User interaction"},
            {"name": "scope", "description": "Scope"},
            {
                "name": "confidentialityImpact",
                "description": "Confidentiality impact",
            },
            {"name": "integrityImpact", "description": "Integrity impact"},
            {
                "name": "availabilityImpact",
                "description": "Availability impact",
            },
            {
                "name": "exploitabilityScore",
                "description": "Exploitability score",
            },
            {"name": "impactScore", "description": "Impact score"},
        ],
        "additional": [
            {"name": "cpe", "description": "CPE identifier"},
        ],
    }

    # Severity levels for classification
    SEVERITY_LEVELS = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
