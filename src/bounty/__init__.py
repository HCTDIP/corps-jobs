"""Bounty processing module"""

from typing import List
from src.bounty.railway_parser import RailwayBountyParser
from src.models.bounty import Bounty

def process_railway_bounty_data(raw_data: str) -> List[Bounty]:
    """Process raw railway bounty data into structured format"""
    parser = RailwayBountyParser(raw_data)
    return parser.parse()
    