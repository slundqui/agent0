"""User strategy that opens a single short and doesn't close until liquidation"""
from elfpy.agents.agent import Agent
from elfpy.markets.hyperdrive import Market, MarketActionType
import elfpy.types as types

# pylint: disable=duplicate-code


class Policy(Agent):
    """simple short thatonly has one long open at a time"""

    def __init__(self, wallet_address, budget=100):
        """call basic policy init then add custom stuff"""
        self.amount_to_trade = 100
        super().__init__(wallet_address, budget)

    def action(self, market: Market) -> "list[types.Trade]":
        """
        implement user strategy
        short if you can, only once
        """
        action_list = []
        shorts = list(self.wallet.shorts.values())
        has_opened_short = bool(any(short.balance > 0 for short in shorts))
        can_open_short = self.get_max_short(market) >= self.amount_to_trade
        if can_open_short and not has_opened_short:
            action_list.append(
                self.create_hyperdrive_action(
                    action_type=MarketActionType.OPEN_SHORT,
                    trade_amount=self.amount_to_trade,
                )
            )
        action_list = [types.Trade(market=types.MarketType.HYPERDRIVE, trade=trade) for trade in action_list]
        return action_list