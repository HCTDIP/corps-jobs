"""Test bounty filtering logic"""

from src.bounty.railway_parser import RailwayBountyParser
from src.models.bounty import Bounty

def test_hot_bounty_detection():
    parser = RailwayBountyParser("")
    bounty = Bounty(
        platform="test",
        title="Test",
        amount=10,
        replies=5,
        days_old=0,
        is_hot=False,
        is_new=False
    )

    assert parser._is_hot(5, 0) is True
    assert parser._is_hot(3, 0) is True
    assert parser._is_hot(5, 1) is False
    