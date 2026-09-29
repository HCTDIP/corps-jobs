"""Test railway bounty parser"""

import pytest
from src.bounty.railway_parser import RailwayBountyParser

SAMPLE_RAILWAY_DATA = """[railway-radar] 2026-09-29 01:17Z total=29 hot=2 new=1
🆕 Server Performance Issue on Pro Plan – Project B Not Responding / Login Failing $30 5 replies 7m by
[+4] Successful Railway deployment keeps publishing GitHub deployment failure $10 2 replies 2
[+4] Clarification of exact-commit deployment and rollback side effects $5 1 replies 1
"""

def test_railway_parser():
    parser = RailwayBountyParser(SAMPLE_RAILWAY_DATA)
    bounties = parser.parse()

    assert len(bounties) == 2
    assert bounties[0].title == "Successful Railway deployment keeps publishing GitHub deployment failure"
    assert bounties[0].amount == 10
    assert bounties[0].is_new
    assert bounties[0].competition_level == "low"

    assert bounties[1].title == "Clarification of exact-commit deployment and rollback side effects"
    assert bounties[1].amount == 5
    assert not bounties[1].is_new
    