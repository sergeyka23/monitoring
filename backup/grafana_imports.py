import os
import json
import requests
from dotenv import load_dotenv
from DataCoreFlow.DataCoreFlowConfig import DataCoreFlowConfig
dcf_config = DataCoreFlowConfig()

# Load environment variables from .env file
load_dotenv("grafana_exports_config.env")

# Grafana API configuration
GRAFANA_API_URL = os.getenv("GRAFANA_API_URL")
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY")
GRAFANA_HEADERS = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "application/json"
}

# Paths to the directories for datasources, dashboards, and alerts
IMPORT_DIR = os.path.join(".", "grafana_exports", dcf_config.global_configs["ClientName"])
DATASOURCE_DIR = os.path.join(IMPORT_DIR, "datasource")
DASHBOARD_DIR = os.path.join(IMPORT_DIR, "dashboards")
ALERTS_DIR = os.path.join(IMPORT_DIR, "alerts")


# Function to import data sources
def import_data_source():
    for filename in os.listdir(DATASOURCE_DIR):
        if filename.endswith(".json"):  # Check if the file is a JSON file
            data_source_file = os.path.join(DATASOURCE_DIR, filename)

            with open(data_source_file, 'r') as f:
                data_source_json = json.load(f)

            # Make the POST request to import the data source
            response = requests.post(f"{GRAFANA_API_URL}/datasources", headers=GRAFANA_HEADERS, json=data_source_json)

            if response.status_code == 200:
                print(f"Data source '{filename}' imported successfully.")
            else:
                print(f"Failed to import data source '{filename}'. Status code: {response.status_code}")
                print(response.json())
        else:
            raise FileNotFoundError(f"Found a file not a JSON in {DATASOURCE_DIR}")


# Function to import dashboards
def import_dashboards():
    for filename in os.listdir(DASHBOARD_DIR):
        if filename.endswith(".json"):  # Check if the file is a JSON file
            dashboard_file = os.path.join(DASHBOARD_DIR, filename)

            with open(dashboard_file, 'r') as f:
                dashboard_json = json.load(f)

            # Wrapping the dashboard in the expected payload structure
            payload = {
                "dashboard": dashboard_json,
                "folderId": 0,  # You can specify a folder ID or 0 for the default folder
                "overwrite": True  # Overwrite existing dashboards with the same UID
            }

            # Make the POST request to import the dashboard
            response = requests.post(f"{GRAFANA_API_URL}/dashboards/db", headers=GRAFANA_HEADERS, json=payload)

            if response.status_code == 200:
                print(f"Dashboard '{filename}' imported successfully.")
            else:
                print(f"Failed to import dashboard '{filename}'. Status code: {response.status_code}")
                print(response.json())
        else:
            raise FileNotFoundError(f"Found a file not a JSON in {DASHBOARD_DIR}")


# Function to import alert rules
def import_alert_rules():
    for filename in os.listdir(ALERTS_DIR):
        if filename.endswith(".json"):  # Check if the file is a JSON file
            alert_file = os.path.join(ALERTS_DIR, filename)

            with open(alert_file, 'r') as f:
                alert_json = json.load(f)

            # Make the POST request to import the alert rules
            response = requests.post(f"{GRAFANA_API_URL}/v1/provisioning/alert-rules", headers=GRAFANA_HEADERS, json=alert_json[0])

            if response.status_code == 200:
                print(f"Alert rules '{filename}' imported successfully.")
            else:
                print(f"Failed to import alert rules '{filename}'. Status code: {response.status_code}")
                print(response.json())
        else:
            raise FileNotFoundError(f"Found a file not a JSON in {ALERTS_DIR}")


if __name__ == "__main__":
    import_data_source()
    # import_dashboards()
    # import_alert_rules()
