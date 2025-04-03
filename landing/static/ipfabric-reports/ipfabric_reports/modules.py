#!/usr/bin/env python3
"""
IP Fabric Report Generator - Utility Modules.

This module provides utility functions for data processing and visualization
in the IP Fabric report generator. It contains reusable helper functions that
are used across different report types.

Functions:
    count_unique_occurrences: Count unique items in a dataset
    get_distribution_ratio: Calculate distribution percentages
    plot_pie_chart: Generate pie charts for data visualization

Visualization Features:
    - Pie chart generation with customizable colors
    - Base64 encoding for embedded images
    - Matplotlib figure configuration
    - Custom color schemes from ReportStyleConfig

Data Processing Features:
    - Distribution calculations
    - Ratio computations
    - Data aggregation helpers
    - Format conversion utilities

Usage:
    These utilities are used internally by report types for:
    - Data analysis and transformation
    - Chart generation
    - Distribution calculations
    - Visual report enhancement
"""

# Standard library imports
import base64
import io
import json
import os
from typing import Any, Dict, List

# Third-party imports
import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger

MAX_VLANS = 4094


def get_distribution_ratio(
    data: List[Dict[str, Any]], key: str
) -> Dict[str, Dict[str, Any]]:
    """
    Calculate the distribution ratio of a key in a list of dictionaries.
    :param data: List of dictionaries
    :param key: Key to calculate the distribution ratio for
    Returns: Dictionary with the percentage and count of distribution ratio for each unique value of the key
    """

    try:
        len_values = len(data)
        distribution = {}

        for item in data:
            distribution_key = item.get(key)
            if distribution_key:
                distribution[distribution_key] = (
                    distribution.get(distribution_key, 0) + 1
                )

        return {
            k: {"percentage": round((v / len_values) * 100, 2), "count": v}
            for k, v in distribution.items()
        }
    except Exception as e:
        raise ValueError(
            logger.error(f"Error calculating distribution ratio: {str(e)} from data: {data.get('name')}")
        )


def count_unique_occurrences(data: List[Dict[str, Any]], key: str) -> int:
    """
    Efficiently count the number of unique occurrences of items for a specific key in a list of dictionaries.

    :param data: List of dictionaries containing the data
    :param key: The key to count unique occurrences for
    :return: An integer representing the count of unique values for the specified key
    """
    return len(set(item[key] for item in data if key in item))


def load_chart_colors(json_file_path):
    """
    Load the chart colors from a JSON file.

    :param json_file_path: The path to the JSON file containing the chart colors
    :return: A list of chart colors
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            return data.get('chart_colors', [])
    except Exception as e:
        raise ValueError(
            logger.error(f"Error loading chart colors from {json_file_path}: {str(e)}")
        )


def plot_pie_chart(data: dict) -> str:
    """
    Create a pie chart from the data and return the image as a base64 encoded string.

    :param data: A dictionary containing the data to plot
    :return: A base64 encoded string representing the image of the pie chart
    """
    json_file_path = os.path.join('ipfabric_reports', 'styles', 'themes', 'chart_colors.json')

    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"Chart color file not found at {json_file_path}")

    colors = load_chart_colors(json_file_path)

    # Create a new figure with a smaller size
    plt.figure(figsize=(6, 4))

    # Create the pie chart
    wedges, texts, autotexts = plt.pie(
        data.values(),
        labels=data.keys(),
        autopct="%1.1f%%",
        colors=colors,
        textprops={"fontsize": 8},
    )

    # Enhance the appearance
    plt.setp(autotexts, fontsize=8, weight="bold")
    plt.setp(texts, fontsize=8)

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()

    # Encode the bytes buffer to base64
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # Create the data URI for the image
    img_data = f"data:image/png;base64,{img_base64}"

    return img_data


def cleanup_connectivity_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame, taking into account the symmetry condition.
    In the connectivity matrix, some connections can appear twice with the opposite src/dst,
    the goal here is to remove those duplicates, by applying a frozenset for the src and dst,
    then removing the duplicates.

    Args:
        df: A pandas DataFrame.

    Returns:
        A pandas DataFrame without duplicate rows.
    """

    # Create frozensets for local and remote connections
    df["local_set"] = df.apply(
        lambda row: frozenset([row["localSn"], row["localHost"], row["localInt"], row["protocol"]]),
        axis=1,
    )
    df["remote_set"] = df.apply(
        lambda row: frozenset(
            [
                row["remoteSn"],
                row["remoteHost"],
                row["remoteInt"],
                row["protocol"],
            ]
        ),
        axis=1,
    )

    # Create a combined set for symmetry check
    df["combined_set"] = df.apply(
        lambda row: frozenset([row["local_set"], row["remote_set"]]),
        axis=1,
    )

    # Identify duplicates for removal, but keep the first occurrence!!!!!
    df["is_duplicate"] = df.duplicated(subset="combined_set", keep="first")

    # Keep only the first occurrence of each unique connection
    return df[~df["is_duplicate"]].drop(["local_set", "remote_set", "combined_set", "is_duplicate"], axis=1)


def format_vlans(vlan_list: list) -> str:
    """
    Format a list of VLAN numbers into a human-readable string.

    This function takes a list of VLAN numbers, removes duplicates,
    sorts them, and then formats them into a string that represents
    individual VLANs and ranges of consecutive VLANs. For example,
    a list of VLANs like [1, 2, 3, 5, 6, 8] would be formatted as
    "1-3, 5-6, 8".

    Args:
        vlan_list (list): A list of VLAN numbers (integers). The list
                        may contain duplicates and is not required
                        to be sorted.

    Returns:
        str: A formatted string representing the VLANs. If the input
            list is empty, an empty string is returned. The output
            string consists of individual VLANs and ranges of
            consecutive VLANs, separated by commas.

    Example:
        >>> format_vlans([1, 2, 3, 5, 6, 8])
        '1-3, 5-6, 8'

        >>> format_vlans([10, 12, 13, 15])
        '10, 12-13, 15'

        >>> format_vlans([])
        ''
    """
    if not vlan_list:
        return ""
    # Sort the VLAN list to ensure proper ordering
    vlan_list = sorted(set(vlan_list))  # Remove duplicates and sort
    formatted_vlans = []

    # Initialize the range tracking
    start = vlan_list[0]
    end = vlan_list[0]

    for vlan in vlan_list[1:]:
        # Validate each VLAN
        if not isinstance(vlan, int):
            raise TypeError(f"VLAN must be an integer, got {type(vlan)}")

        if vlan < 1 or vlan > MAX_VLANS + 1:
            raise ValueError(f"VLAN {vlan} out of valid range (1-4094)")

        if vlan == end + 1:  # Check if the current VLAN is consecutive
            end = vlan  # Extend the range
        else:
            # If we've reached the end of a range, add it to the list
            if start == end:
                formatted_vlans.append(str(start))  # Single VLAN
            else:
                formatted_vlans.append(f"{start}-{end}")  # Range of VLANs
            start = end = vlan  # Start a new range

    # Add the last range or single VLAN
    if start == end:
        formatted_vlans.append(str(start))
    else:
        formatted_vlans.append(f"{start}-{end}")

    # Join the formatted VLANs with commas
    return ",".join(formatted_vlans)


def parse_vlans(vlan_string: str) -> list:
    """
    Parse a string of VLANs into a list of integers.

    This static method takes a string representation of VLANs, which
    may include individual VLANs and ranges (e.g., "1,2,3,5-10"),
    and converts it into a list of integers representing all VLANs.
    Ranges are expanded to include all VLANs within the specified
    range.

    Args:
        vlan_string (str): A string containing VLANs separated by
                        commas. Individual VLANs can be specified
                        as integers, and ranges can be specified
                        using a dash (e.g., "1-5").

    Returns:
        list: A list of integers representing the parsed VLANs.
            If the input string is empty, an empty list is returned.

    Example:
        >>> parse_vlans("1,2,3,5-7")
        [1, 2, 3, 5, 6, 7]

        >>> parse_vlans("10-12,15")
        [10, 11, 12, 15]

        >>> parse_vlans("")
        []
    """
    # Check if the input string is empty
    if not vlan_string or not vlan_string.strip():
        return []
    # Remove any whitespace from the input string
    vlan_string = vlan_string.replace(" ", "")

    vlans = []
    # Split the input string by commas
    for part in vlan_string.split(","):
        if not part:
            continue

        # Check if the part is a range
        if "-" in part:
            start, end = map(int, part.split("-"))
            # Validate range
            if start < 1 or end < 1 or start > end or end > MAX_VLANS + 1:
                raise ValueError(f"Invalid VLAN range: {part}")
            # Generate the range of VLANs and add to the list, ADD +1 TO INCLUDE THE END VLAN
            vlans.extend(range(start, end + 1))
        else:
            # Otherwise, it's a single VLAN, convert to int and add to the list
            vlan = int(part)
            # Validate single VLAN
            if vlan < 1 or vlan > MAX_VLANS + 1:
                raise ValueError(f"VLAN out of valid range: {vlan}")
            vlans.append(vlan)
    return vlans
