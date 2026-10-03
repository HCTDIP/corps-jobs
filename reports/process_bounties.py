"""CLI tool to process bounty reports"""

import argparse
import json
from pathlib import Path
from src.bounty import process_railway_bounty_data
from src.jobs.feed import enrich_job_feed_with_bounties

def main():
    parser = argparse.ArgumentParser(description="Process bounty reports")
    parser.add_argument("--input", required=True, help="Path to raw bounty data")
    parser.add_argument("--output", required=True, help="Path to output JSON")

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        raw_data = f.read()

    bounties = process_railway_bounty_data(raw_data)

    with open(args.output, 'w') as f:
        json.dump([b.__dict__ for b in bounties], f, indent=2)

if __name__ == "__main__":
    main()
    