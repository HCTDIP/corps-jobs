#!/usr/bin/env python3
"""
Automated script to fetch and update Railway bounty issues from cloud radar.
"""

import json
import requests
from datetime import datetime
import yaml
import os

# Configuration
CONFIG_PATH = "config/bounty_tracker.yml"
REPORT_PATH = "reports/railway_bounty_latest.json"
RADAR_API_URL = "https://api.cloud-radar.com/v1/bounties/railway"

# Load configuration
with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

# Fetch bounty data from radar
def fetch_bounty_data():
    try:
        response = requests.get(RADAR_API_URL, headers={"Authorization": os.getenv("RADAR_API_KEY")})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bounty data: {e}")
        return None

# Process raw radar data into structured format
def process_bounty_data(raw_data):
    processed = {
        "metadata": {
            "source": "railway-radar",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total": raw_data.get("total", 0),
            "hot": raw_data.get("hot", 0),
            "new": raw_data.get("new", 0)
        },
        "bounties": []
    }
    
    for item in raw_data.get("items", []):
        bounty = {
            "id": f"bounty-{datetime.utcnow().strftime('%Y%m%d')}-{len(processed['bounties']) + 1}",
            "title": item.get("title", ""),
            "type": config.get("type_mapping", {}).get(item.get("type", "question"), "question"),
            "status": item.get("status", "inactive"),
            "bounty": item.get("bounty", 0),
            "competition": item.get("competition", "medium"),
            "region": item.get("region", "global"),
            "last_updated": item.get("last_updated", ""),
            "tags": item.get("tags", [])
        }
        processed["bounties"].append(bounty)
    
    return processed

# Save processed data to report file
def save_bounty_report(data):
    with open(REPORT_PATH, 'w') as f:
        json.dump(data, f, indent=2)

# Main execution
if __name__ == "__main__":
    raw_data = fetch_bounty_data()
    if raw_data:
        processed_data = process_bounty_data(raw_data)
        save_bounty_report(processed_data)
        print(f"Successfully updated bounty report at {REPORT_PATH}")
    else:
        print("Failed to update bounty report")