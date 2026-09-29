#!/usr/bin/env python3
"""
Automated bounty tracker updater for Railway issues.
"""

import json
import os
from datetime import datetime

REPORT_PATH = "reports/railway_bounty_latest.json"

class BountyTracker:
    def __init__(self):
        self.bounties = []

    def load_existing(self):
        """Load existing bounty data from JSON file."""
        if os.path.exists(REPORT_PATH):
            with open(REPORT_PATH, 'r') as f:
                self.bounties = json.load(f)

    def add_bounty(self, title, bounty_type, competition, reward, tags):
        """Add new bounty entry with auto-generated ID."""
        bounty_id = f"railway-{datetime.now().strftime('%Y%m%d')}-{len(self.bounties)+1:03d}"
        self.bounties.append({
            "id": bounty_id,
            "title": title,
            "type": bounty_type,
            "competition": competition,
            "reward": reward,
            "status": "open",
            "source": "cloud-radar",
            "tags": tags,
            "last_updated": datetime.now().isoformat() + "Z"
        })

    def save(self):
        """Save bounty data to JSON file."""
        with open(REPORT_PATH, 'w') as f:
            json.dump(self.bounties, f, indent=2)

    def mark_duplicate(self, title):
        """Mark existing bounty as duplicate."""
        for bounty in self.bounties:
            if bounty["title"] == title:
                bounty["status"] = "duplicate"

if __name__ == "__main__":
    tracker = BountyTracker()
    tracker.load_existing()

    # Add new bounties from issue #16
    tracker.add_bounty(
        title="Multiple production deployments crashing – please investigate project/account configuration",
        bounty_type="configuration",
        competition="low",
        reward=20,
        tags=["production", "deployment", "crash"]
    )

    tracker.add_bounty(
        title="Sudden DNS issue on production system",
        bounty_type="infrastructure",
        competition="low",
        reward=20,
        tags=["dns", "production", "network"]
    )

    tracker.add_bounty(
        title="Clarification of exact-commit deployment and rollback side effects",
        bounty_type="configuration",
        competition="low",
        reward=0,
        tags=["deployment", "rollback", "clarification"]
    )

    # Mark duplicate entry
    tracker.mark_duplicate(
        title="Multiple production deployments crashing – please investigate project/account configuration"
    )

    tracker.save()