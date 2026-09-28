# Railway Bounty Tracker

This repository tracks and automates the collection of Railway bounty issues from cloud radar.

## Features
- Automated bounty data collection via API
- Structured JSON reporting
- Competition analysis
- Region-specific tracking

## Bounty Data Structure
The `reports/railway_bounty_latest.json` file contains:
- Metadata (source, timestamp, counts)
- Individual bounty entries with:
  - Unique ID
  - Title and description
  - Type (question/bug/feature)
  - Status (new/active/inactive)
  - Bounty amount
  - Competition level
  - Region
  - Tags for categorization

## Automation
The `scripts/fetch_railway_bounties.py` script:
- Fetches data from cloud radar API
- Processes raw data into structured format
- Updates the report file
- Can be scheduled via cron

## Configuration
The `config/bounty_tracker.yml` file defines:
- Type mappings
- Competition levels
- Region mappings
- Bounty categories
- Update frequency

## Usage
1. Set up API credentials in environment variables
2. Run the script manually or via cron:
   ```bash
   python3 scripts/fetch_railway_bounties.py
   ```
3. Monitor the `reports/` directory for updates

## Bounty Categories
The system categorizes bounties into:
- Deployment issues
- Networking problems
- Configuration questions
- Integration errors

## Competition Analysis
Bounties are classified by competition level:
- Low: Few replies, recent activity
- Medium: Moderate engagement
- High: High competition, many replies

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.