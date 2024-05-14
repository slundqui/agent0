"""Dataclasses for all structs in the LPMath contract.

DO NOT EDIT.  This file was generated by pypechain.  See documentation at
https://github.com/delvtech/pypechain """

# super() call methods are generic, while our version adds values & types
# pylint: disable=arguments-differ

# contracts have PascalCase names
# pylint: disable=invalid-name
# contracts control how many attributes and arguments we have in generated code
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# unable to determine which imports will be used in the generated code
# pylint: disable=unused-import
# we don't need else statement if the other conditionals all have return,
# but it's easier to generate
# pylint: disable=no-else-return
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PresentValueParams:
    """PresentValueParams struct."""

    shareReserves: int
    shareAdjustment: int
    bondReserves: int
    vaultSharePrice: int
    initialVaultSharePrice: int
    minimumShareReserves: int
    minimumTransactionAmount: int
    timeStretch: int
    longsOutstanding: int
    longAverageTimeRemaining: int
    shortsOutstanding: int
    shortAverageTimeRemaining: int


@dataclass
class DistributeExcessIdleParams:
    """DistributeExcessIdleParams struct."""

    presentValueParams: PresentValueParams
    startingPresentValue: int
    activeLpTotalSupply: int
    withdrawalSharesTotalSupply: int
    idle: int
    netCurveTrade: int
    originalShareReserves: int
    originalShareAdjustment: int
    originalBondReserves: int


@dataclass
class ErrorInfo:
    """Custom contract error information."""

    name: str
    selector: str
    signature: str
    inputs: list[ErrorParams]


@dataclass
class ErrorParams:
    """Parameter info for custom contract errors."""

    name: str
    solidity_type: str
    python_type: str


ExpInvalidExponentError = ErrorInfo(
    inputs=[],
    name="ExpInvalidExponent",
    selector="0x73a2d6b1",
    signature="ExpInvalidExponent()",
)

InvalidPresentValueError = ErrorInfo(
    inputs=[],
    name="InvalidPresentValue",
    selector="0xaa2c6516",
    signature="InvalidPresentValue()",
)

LnInvalidInputError = ErrorInfo(
    inputs=[],
    name="LnInvalidInput",
    selector="0xe61b4975",
    signature="LnInvalidInput()",
)

UnsafeCastToInt256Error = ErrorInfo(
    inputs=[],
    name="UnsafeCastToInt256",
    selector="0x72dd4e02",
    signature="UnsafeCastToInt256()",
)