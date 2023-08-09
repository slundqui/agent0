"""Policies for expert system trading bots"""
from __future__ import annotations

from typing import NamedTuple

from agent0.base.policies import BasePolicy

from .random_agent import RandomAgent
from .smart_long import LongLouie
from .smart_short import ShortSally


class Policies(NamedTuple):
    """All policies in elfpy."""

    base_policy = BasePolicy
    random_agent = RandomAgent
    long_louie = LongLouie
    short_sally = ShortSally