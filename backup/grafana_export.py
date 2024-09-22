import os
import json
import requests
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from DataCoreFlow.DataCoreFlowConfig import DataCoreFlowConfig
dcf_config = DataCoreFlowConfig()

load_dotenv("grafana_exports_config.env")
# Configuration
GRAFANA_API_URL = os.getenv("GRAFANA_API_URL")
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY")
GRAFANA_HEADERS = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "application/json"
}
EXPORT_DIR = os.path.join(".","grafana_exports", dcf_config.global_configs["ClientName"] )
DASHBOARD_DIR = os.path.join(EXPORT_DIR, "dashboards")
ALERTS_DIR = os.path.join(EXPORT_DIR, "alerts")
DATASOURCE_DIR = os.path.join(EXPORT_DIR, "datasource")
GIT_REPO_PATH = os.getenv("GIT_REPO_PATH")

# Create necessary directories
os.makedirs(DASHBOARD_DIR, exist_ok=True)
os.makedirs(ALERTS_DIR, exist_ok=True)
os.makedirs(DATASOURCE_DIR, exist_ok=True)
# Function to export dashboards
def export_dashboards():
    response = requests.get(f"{GRAFANA_API_URL}/search?type=dash-db", headers=GRAFANA_HEADERS)
    dashboards = response.json()

    for dashboard in dashboards:
        uid = dashboard['uid']
        title = dashboard['title'].replace(" ", "_")
        response = requests.get(f"{GRAFANA_API_URL}/dashboards/uid/{uid}", headers=GRAFANA_HEADERS)
        dashboard_json = response.json()['dashboard']

        with open(os.path.join(DASHBOARD_DIR, f"{title}_{uid}.json"), 'w') as f:
            json.dump(dashboard_json, f, indent=4)

# Function to export alert rules (if defined separately)
def export_alert_rules():
    response = requests.get(f"{GRAFANA_API_URL}/v1/provisioning/alert-rules", headers=GRAFANA_HEADERS)
    # response = requests.get("http:/localhost:3000/api/v1/provisioning/alert-rules/")
    alerts = response.json()

    with open(os.path.join(ALERTS_DIR, "alert-rules.json"), 'w') as f:
        json.dump(alerts, f, indent=4)


# Function to export data sources
# Function to export data sources
def export_data_sources():
    response = requests.get(f"{GRAFANA_API_URL}/datasources", headers=GRAFANA_HEADERS)
    data_sources = response.json()

    for data_source in data_sources:
        name = data_source['name'].replace(" ", "_")
        with open(os.path.join(DATASOURCE_DIR, f"{name}.json"), 'w') as f:
            json.dump(data_source, f, indent=4)


# Function to commit and push changes to the Git repository
def commit_and_push():
    os.chdir(GIT_REPO_PATH)
    subprocess.run(["git", "add", "."])
    commit_message = f"Auto-export: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    # export_dashboards()
    # export_alert_rules()
    export_data_sources()
    # commit_and_push()
