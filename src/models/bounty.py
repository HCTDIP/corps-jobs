"""Bounty data model"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Bounty:
    platform: str
    title: str
    amount: int
    replies: int
    days_old: int
    is_hot: bool
    is_new: bool

    @property
    def competition_level(self) -> str:
        """Determine competition level based on replies and age"""
        if self.days_old < 2 and self.replies < 3:
            return "low"
        return "medium"
    