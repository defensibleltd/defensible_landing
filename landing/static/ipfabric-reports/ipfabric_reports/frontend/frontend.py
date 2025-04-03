import os
import streamlit as st
import pandas as pd
from os import listdir
from os.path import isfile, join

from ipfabric_reports.report_registry import ReportRegistry
from ipfabric_reports import IPFabricReportGenerator


from ipfabric import IPFClient


class ReportFrontend:
    def __init__(self):
        st.set_page_config(
            page_title="IP Fabric Reports", page_icon="📊", layout="wide"
        )
        self.ensure_export_dir()

    def run(self):
        st.title("IP Fabric Report Generator")
        st.write(
            """
        Welcome to the IP Fabric Report Generator.
        Generate and view reports from your IP Fabric instance.
        """
        )

        self.show_connection_form()
        self.show_report_form()
        self.display_reports()

    def show_connection_form(self):
        with st.form("IPF Connection"):
            st.header("IP Fabric Connection")
            ipf_url = st.text_input("IP Fabric URL", value="https://ipfabric.io")
            ipf_token = st.text_input("IP Fabric Token", value="", type="password")
            snapshot_id = st.text_input(
                "Snapshot ID", placeholder="Enter snapshot ID...", value="$last"
            )
            if ipf_url == "https://ipfabric.io":
                st.write("Please enter your IP Fabric URL and token.")
            submit = st.form_submit_button("Connect to IP Fabric")
            if submit:
                try:
                    ipf_client = IPFClient(
                        base_url=ipf_url, auth=ipf_token, snapshot_id=snapshot_id
                    )
                    st.session_state["ipf_client"] = ipf_client
                    st.success("Connected to IP Fabric")
                    return True
                except Exception as e:
                    st.error(f"Failed to connect: {str(e)}")
                    return False
            return False

    def show_report_form(self):
        if "ipf_client" not in st.session_state:
            st.error("Please connect to IP Fabric first.")
            return
        else:
            ipf_client = st.session_state["ipf_client"]
        with st.form("Report Configuration"):
            report_types = ReportRegistry.list_reports()
            for report, report_info in report_types.items():
                st.write(f"##### {report.upper()}\n{report_info}")

            selected_report = st.selectbox("Select Report Type", options=report_types)

            col1, col2 = st.columns(2)
            with col1:
                site_filter_applied = st.checkbox("Apply Site Filter", value=False)
                all_sites = ipf_client.inventory.sites.all()
                site_names = [site["id"] for site in all_sites]
                site_filter = st.selectbox(
                        "Site Filter",
                        options=site_names,
                        placeholder="Enter site name...",
                    )
                if site_filter_applied or selected_report == "cve":
                    site_filter = site_filter
                else:
                    site_filter = None

            with col2:
                report_style = st.file_uploader("Report Style CSS", type="css")
                nvd_api_key = st.text_input("NVD API Key", type="password")

            submit = st.form_submit_button("Generate Report")
            if submit:
                if not site_filter_applied:
                    site_filter = None
                self.generate_report(
                    selected_report,
                    site_filter,
                    ipf_client.snapshot_id,
                    report_style,
                    nvd_api_key,
                )

    def generate_report(
        self, report_type, site_filter, snapshot_id, report_style, nvd_api_key
    ):
        with st.spinner("Generating report..."):
            report_generator = IPFabricReportGenerator(
                ipf_client=st.session_state["ipf_client"],
                site_filter=site_filter,
                report_type=report_type,
                report_style=report_style,
                snapshot_id=snapshot_id,
                nvd_api_key=nvd_api_key,
            )
            report_generator.generate_report()
            st.success(f"Report '{report_type}' generated successfully!")

    def display_reports(self):
        st.header("Available Reports")

        export_path = os.path.join(os.getcwd(), "export")
        files = [f for f in listdir(export_path) if isfile(join(export_path, f))]

        if not files:
            st.info("No reports available. Generate a report using the form above.")
            return

        selected_file = st.selectbox("Select a report to view", files)

        if selected_file:
            file_path = os.path.join(export_path, selected_file)

            if selected_file.endswith(".html"):
                with open(file_path, "r") as f:
                    st.html(f.read())
            elif selected_file.endswith((".xlsx", ".csv")):
                df = (
                    pd.read_csv(file_path)
                    if selected_file.endswith(".csv")
                    else pd.read_excel(file_path)
                )
                st.dataframe(df)
            else:
                st.warning("This file format cannot be previewed")

            with open(file_path, "rb") as file:
                st.download_button(
                    label="Download Report",
                    data=file,
                    file_name=selected_file,
                    mime="application/octet-stream",
                )

    @staticmethod
    def ensure_export_dir():
        if not os.path.exists("export"):
            os.makedirs("export")


if __name__ == "__main__":
    frontend = ReportFrontend()
    frontend.run()
