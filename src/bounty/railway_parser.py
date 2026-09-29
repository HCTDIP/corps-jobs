import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from src.models.bounty import Bounty

class RailwayBountyParser:
    def __init__(self, raw_data: str):
        self.raw_data = raw_data
        self.bounties: List[Bounty] = []

    def parse(self) -> List[Bounty]:
        """Parse raw railway radar output into structured bounty objects"""
        lines = self.raw_data.split('\
')
        for line in lines[1:]:  # Skip header
            if not line.strip() or line.startswith('['):
                continue

            bounty = self._parse_line(line)
            if bounty:
                self.bounties.append(bounty)

        return self.bounties

    def _parse_line(self, line: str) -> Optional[Bounty]:
        """Parse individual bounty line"""
        # Pattern matches: [+4] Successful Railway deployment keeps publishing GitHub deployment failure $10 2 replies 2
        match = re.match(
            r'\[\+?\d*\]\s+(.*?)\s+\$(\d+)\s+(\d+)\s+replies\s+(\d+)',
            line.strip()
        )

        if not match:
            return None

        title = match.group(1)
        amount = int(match.group(2))
        replies = int(match.group(3))
        days_old = int(match.group(4))

        return Bounty(
            platform='railway',
            title=title,
            amount=amount,
            replies=replies,
            days_old=days_old,
            is_hot=self._is_hot(replies, days_old),
            is_new=days_old < 2
        )

    def _is_hot(self, replies: int, days_old: int) -> bool:
        """Determine if bounty qualifies as 'hot'"""
        return replies >= 5 or (days_old < 1 and replies >= 3)
    