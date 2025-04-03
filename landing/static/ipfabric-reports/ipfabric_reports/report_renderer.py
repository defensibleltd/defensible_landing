#!/usr/bin/env python3
"""
Report Renderer Module.

This module contains the ReportRenderer class that is responsible for
rendering the HTML and PDF reports using Jinja2 templates and WeasyPrint.
"""

# Standard library imports
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Third-party imports
from jinja2 import Environment, FileSystemLoader
from loguru import logger
import pandas as pd
from weasyprint import HTML, urls


class ReportRenderer:
    def __init__(
        self,
        logo_path: str,
        template_dir: Path = "src/templates",
        output_dir: str = "export",
        generate_html: bool = False,
    ):
        """
        Initialize the ReportRenderer.

        Args:
            template_dir: Directory containing the templates
            output_dir: Directory where reports will be saved
            generate_html: Whether to generate HTML files alongside PDFs
        """
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.generate_html = generate_html
        self.package_dir = Path(__file__).resolve().parent
        self.env.globals["image_path"] = str(self.package_dir / logo_path)
        self.timestamp = datetime.now().strftime("%Y-%m-%d_T%H-%M")

    def _render_html(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render HTML content from a template.

        Args:
            template_name: Name of the template file
            context: Data to be rendered in the template

        Returns:
            Rendered HTML content as a string
        """
        # Ensure we have report_name in context for the footer
        if "report_name" not in context:
            context["report_name"] = context.get("report_type", "Report").replace(
                "_", " "
            )

        context["current_time"] = self.timestamp

        template = self.env.get_template(template_name)
        return template.render(context)

    def _save_html(self, html_content: str, filename: str) -> Optional[Path]:
        """
        Save HTML content to a file if HTML generation is enabled.

        Args:
            html_content: HTML content to save
            filename: Name of the file to save

        Returns:
            Path to the saved HTML file or None if HTML generation is disabled
        """
        if not self.generate_html:
            return None

        file_path = self.output_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            logger.success(f"✔ Saving HTML file to: {file_path}")

    def _save_pdf(self, html_content: str, css_path: Path, filename: str) -> None:
        """
        Write a PDF from HTML content.
        """
        pdf_path = self.output_dir / filename
        HTML(string=html_content).write_pdf(pdf_path, stylesheets=[css_path])
        logger.success(f"✔ Saving PDF file to: {pdf_path}")

    def render_pdf_report(
        self,
        template_name: str,
        report_data: Dict[str, Any],
        css_path: Path,
        save_html: bool = False,
    ) -> None:
        """
        Render a report to PDF (and optionally HTML).

        Args:
            template_name: Name of the template file
            report_data: Data to be rendered in the report
            css_path: Path to the CSS file
            save_html: Whether to save the HTML file

        Returns:
            nothing
        """
        report_type_str = report_data.get("report_details").get("type")
        # Add site filter to filename if present
        if report_data.get("site_filter"):
            report_type_str = f"{report_type_str}-{report_data['site_filter']}"

        # Render HTML template with data
        html_content = self._render_html(template_name, report_data)
        base_filename = f"{report_type_str}_{self.timestamp}"

        # Save HTML file if enabled
        if save_html:
            self._save_html(html_content, f"{base_filename}.html")

        # Create PDF
        self._save_pdf(html_content, css_path, f"{base_filename}.pdf")

    def render_xlsx_report(self, report_data: Dict[str, Any]) -> None:
        """
        Render a report as an XLSX file.

        Args:
            report_data: Data to be rendered in the report

        Returns:
            nothing
        """
        report_type_str = report_data.get("report_details").get("type")
        # Add site filter to filename if present
        if report_data.get("site_filter"):
            report_type_str = f"{report_type_str}-{report_data['site_filter']}"

        xlsx_filename = f"{report_type_str}_{self.timestamp}.xlsx"
        file_path = self.output_dir / xlsx_filename

        with pd.ExcelWriter(file_path) as writer:
            report_data["trunk_mismatch_report"].to_excel(
                writer, sheet_name="Summary - Trunks Mismatch", index=False
            )
            report_data["full_trunk_report"].to_excel(
                writer, sheet_name="Full Report - Trunks", index=False
            )
            logger.success(f"Saving XLSX file to: {file_path}")
