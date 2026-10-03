"""Job feed integration with bounty data"""

from typing import List
from src.bounty import process_railway_bounty_data
from src.models.bounty import Bounty
from src.models.job import Job

def enrich_job_feed_with_bounties(raw_jobs: List[Job], raw_bounty_data: str) -> List[Job]:
    """Add bounty opportunities to existing job feed"""
    bounties = process_railway_bounty_data(raw_bounty_data)

    # Filter for high-value opportunities
    target_bounties = [
        b for b in bounties
        if (b.is_hot or b.is_new) and b.amount >= 10
    ]

    # Create job entries for bounties
    bounty_jobs = [
        Job(
            title=f"Bounty: {b.title}",
            description=f"${b.amount} bounty on {b.platform} - {b.competition_level} competition",
            platform=b.platform,
            is_bounty=True,
            bounty_amount=b.amount,
            bounty_replies=b.replies,
            bounty_days_old=b.days_old
        )
        for b in target_bounties
    ]

    return raw_jobs + bounty_jobs
    