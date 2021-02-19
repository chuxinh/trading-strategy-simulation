# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from pandas import DataFrame
from typing import List, Tuple


class TradingSimulation:
    """Return a dataframe with historical prices, number of units and portfolio value at a point in time.
    Parameters
    ----------
    df: dataframe of historical prices returned by package yahoofinancials.
    interval: number of day intervals to trade.
    amount: total amount of money to be invested during the back testing period.
    price: default to closing price of the stock.
    same_start_date: default to True so that the first trade took place in the very first record date.
    Returns
    -------
    Dataframe with price, number of units, portfolio value, amount invested and return.
    """

    def __init__(
        self,
        df: DataFrame,
        interval: int,
        amount: float,
        price: str = "close",
        same_start_date: bool = True,
    ) -> None:
        self.df = df
        self.interval = interval
        self.amount = amount
        self.price = price
        self.same_start_date = same_start_date

    def _random_stock_pick(self, df, interval, price, same_start_date) -> Tuple(np.array, np.array):
        num_records = df.shape[0]
        # to create an array per interval for sampling, need to remove extra rows
        rows_to_keep = num_records - num_records % interval
        prices_array = df[:rows_to_keep][price].values.reshape(-1, interval)
        date_array = df[:rows_to_keep].index.values.reshape(-1, interval)
        idx = np.random.randint(0, prices_array.shape[1], prices_array.shape[0])

        if same_start_date:
            idx[0] = 0

        return prices_array[np.arange(len(idx)), idx], date_array[np.arange(len(idx)), idx]

    def compute_portfolio(self) -> DataFrame:
        prices_bought_at, date = self._random_stock_pick(
            self.df, self.interval, self.price, self.same_start_date
        )
        amount_invested_each_trade = self.amount / len(prices_bought_at)
        num_units_each_trade = amount_invested_each_trade / prices_bought_at

        # to calculate the cumulative sum of units purchased at a point in time
        total_units_at_each_trade = np.cumsum(num_units_each_trade)
        # to calculate the cumulative sum of units invested at a point in time
        total_dollar_invested_to_date = np.cumsum(
            np.full_like(total_units_at_each_trade, amount_invested_each_trade)
        )

        # create a dataframe with trading transaction date, number of units and prices on that date
        trading_record = pd.DataFrame(
            {
                "number_of_units": total_units_at_each_trade,
                "prices": prices_bought_at,
                "invested_to_date": total_dollar_invested_to_date,
            },
            index=date,
        )

        # concat the result to the original price records of the stock for calculation of portfolio value each day
        result = pd.concat(
            [self.df[self.price], trading_record[["number_of_units", "invested_to_date"]]], axis=1
        )
        # use forward fill to fill any missing value with the previous number of units
        result.fillna(method="ffill", inplace=True)
        # then fill any missing value with 0; this should only apply to the first few days before the 1st trade
        result.fillna(0, inplace=True)
        result["portfolio_value"] = result[self.price] * result["number_of_units"]
        result["return"] = result["portfolio_value"] / result["invested_to_date"] - 1

        return result

    def _generate_end_value(self, current_price: float) -> float:
        prices_bought_at = self._random_stock_pick(
            self.df, self.interval, self.price, self.same_start_date
        )[0]
        amount_invested_each_trade = self.amount / len(prices_bought_at)
        num_units_each_trade = amount_invested_each_trade / prices_bought_at

        # to calculate number of units to date
        total_units_at_each_trade = np.sum(num_units_each_trade)

        return total_units_at_each_trade * current_price

    def run_simulation(self, current_price: float, n: int = 10000) -> Tuple(List, List):
        results = []
        returns = []

        for i in range(n):
            end_value = self._generate_end_value(current_price)
            end_return = end_value / self.amount - 1
            simulated_results.append(end_value)
            simulated_returns.append(end_return)

        return results, returns
