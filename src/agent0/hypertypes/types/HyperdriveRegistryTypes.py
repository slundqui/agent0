"""Dataclasses for all structs in the HyperdriveRegistry contract.

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

from web3.types import ABIEvent, ABIEventParams

AdminUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="admin", type="address"),
    ],
    name="AdminUpdated",
    type="event",
)

FactoryInfoUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="factory", type="address"),
        ABIEventParams(indexed=True, name="data", type="uint256"),
    ],
    name="FactoryInfoUpdated",
    type="event",
)

InstanceInfoUpdated = ABIEvent(
    anonymous=False,
    inputs=[
        ABIEventParams(indexed=True, name="instance", type="address"),
        ABIEventParams(indexed=True, name="data", type="uint256"),
        ABIEventParams(indexed=True, name="factory", type="address"),
    ],
    name="InstanceInfoUpdated",
    type="event",
)


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


EndIndexTooLargeError = ErrorInfo(
    inputs=[],
    name="EndIndexTooLarge",
    selector="0xe0f7becb",
    signature="EndIndexTooLarge()",
)

InputLengthMismatchError = ErrorInfo(
    inputs=[],
    name="InputLengthMismatch",
    selector="0xaaad13f7",
    signature="InputLengthMismatch()",
)

InvalidFactoryError = ErrorInfo(
    inputs=[],
    name="InvalidFactory",
    selector="0x7a44db95",
    signature="InvalidFactory()",
)

InvalidIndexesError = ErrorInfo(
    inputs=[],
    name="InvalidIndexes",
    selector="0x764e6b56",
    signature="InvalidIndexes()",
)

UnauthorizedError = ErrorInfo(
    inputs=[],
    name="Unauthorized",
    selector="0x82b42900",
    signature="Unauthorized()",
)
