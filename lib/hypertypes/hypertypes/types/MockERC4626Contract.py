"""A web3.py Contract class for the MockERC4626 contract."""

# contracts have PascalCase names
# pylint: disable=invalid-name

# contracts control how many attributes and arguments we have in generated code
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments

# we don't need else statement if the other conditionals all have return,
# but it's easier to generate
# pylint: disable=no-else-return

# This file is bound to get very long depending on contract sizes.
# pylint: disable=too-many-lines

from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any, Tuple, Type, TypeVar, cast

from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes

from typing_extensions import Self
from web3 import Web3
from web3.contract.contract import Contract, ContractFunction, ContractFunctions
from web3.exceptions import FallbackNotFound
from web3.types import ABI, BlockIdentifier, CallOverride, TxParams


T = TypeVar("T")

structs = {}


def tuple_to_dataclass(cls: type[T], tuple_data: Any | Tuple[Any, ...]) -> T:
    """
    Converts a tuple (including nested tuples) to a dataclass instance.  If cls is not a dataclass,
    then the data will just be passed through this function.

    Arguments
    ---------
    cls: type[T]
        The dataclass type to which the tuple data is to be converted.
    tuple_data: Any | Tuple[Any, ...]
        A tuple (or nested tuple) of values to convert into a dataclass instance.

    Returns
    -------
    T
        Either an instance of cls populated with data from tuple_data or tuple_data itself.
    """
    if not is_dataclass(cls):
        return cast(T, tuple_data)

    field_types = {field.name: field.type for field in fields(cls)}
    field_values = {}

    for (field_name, field_type), value in zip(field_types.items(), tuple_data):
        field_type = structs.get(field_type, field_type)
        if is_dataclass(field_type):
            # Recursively convert nested tuples to nested dataclasses
            field_values[field_name] = tuple_to_dataclass(field_type, value)
        elif isinstance(value, tuple) and not getattr(field_type, "_name", None) == "Tuple":
            # If it's a tuple and the field is not intended to be a tuple, assume it's a nested dataclass
            field_values[field_name] = tuple_to_dataclass(field_type, value)
        else:
            # Otherwise, set the primitive value directly
            field_values[field_name] = value

    return cls(**field_values)


class MockERC4626DOMAIN_SEPARATORContractFunction(ContractFunction):
    """ContractFunction for the DOMAIN_SEPARATOR method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626DOMAIN_SEPARATORContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bytes:
        """returns bytes"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bytes

        return cast(bytes, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626AllowanceContractFunction(ContractFunction):
    """ContractFunction for the allowance method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str, arg2: str) -> "MockERC4626AllowanceContractFunction":
        clone = super().__call__(arg1, arg2)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626ApproveContractFunction(ContractFunction):
    """ContractFunction for the approve method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, spender: str, amount: int) -> "MockERC4626ApproveContractFunction":
        clone = super().__call__(spender, amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626AssetContractFunction(ContractFunction):
    """ContractFunction for the asset method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626AssetContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626AuthorityContractFunction(ContractFunction):
    """ContractFunction for the authority method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626AuthorityContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626BalanceOfContractFunction(ContractFunction):
    """ContractFunction for the balanceOf method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str) -> "MockERC4626BalanceOfContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626CanCallContractFunction(ContractFunction):
    """ContractFunction for the canCall method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, user: str, target: str, functionSig: bytes) -> "MockERC4626CanCallContractFunction":
        clone = super().__call__(user, target, functionSig)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626ConvertToAssetsContractFunction(ContractFunction):
    """ContractFunction for the convertToAssets method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, shares: int) -> "MockERC4626ConvertToAssetsContractFunction":
        clone = super().__call__(shares)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626ConvertToSharesContractFunction(ContractFunction):
    """ContractFunction for the convertToShares method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, assets: int) -> "MockERC4626ConvertToSharesContractFunction":
        clone = super().__call__(assets)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626DecimalsContractFunction(ContractFunction):
    """ContractFunction for the decimals method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626DecimalsContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626DepositContractFunction(ContractFunction):
    """ContractFunction for the deposit method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, _assets: int, _receiver: str) -> "MockERC4626DepositContractFunction":
        clone = super().__call__(_assets, _receiver)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626DoesRoleHaveCapabilityContractFunction(ContractFunction):
    """ContractFunction for the doesRoleHaveCapability method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, role: int, functionSig: bytes) -> "MockERC4626DoesRoleHaveCapabilityContractFunction":
        clone = super().__call__(role, functionSig)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626DoesUserHaveRoleContractFunction(ContractFunction):
    """ContractFunction for the doesUserHaveRole method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, user: str, role: int) -> "MockERC4626DoesUserHaveRoleContractFunction":
        clone = super().__call__(user, role)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626GetRateContractFunction(ContractFunction):
    """ContractFunction for the getRate method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626GetRateContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626GetRolesWithCapabilityContractFunction(ContractFunction):
    """ContractFunction for the getRolesWithCapability method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: bytes) -> "MockERC4626GetRolesWithCapabilityContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bytes:
        """returns bytes"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bytes

        return cast(bytes, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626GetTargetCustomAuthorityContractFunction(ContractFunction):
    """ContractFunction for the getTargetCustomAuthority method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str) -> "MockERC4626GetTargetCustomAuthorityContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626GetUserRolesContractFunction(ContractFunction):
    """ContractFunction for the getUserRoles method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str) -> "MockERC4626GetUserRolesContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bytes:
        """returns bytes"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bytes

        return cast(bytes, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626IsCapabilityPublicContractFunction(ContractFunction):
    """ContractFunction for the isCapabilityPublic method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: bytes) -> "MockERC4626IsCapabilityPublicContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626IsCompetitionModeContractFunction(ContractFunction):
    """ContractFunction for the isCompetitionMode method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626IsCompetitionModeContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626MaxDepositContractFunction(ContractFunction):
    """ContractFunction for the maxDeposit method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str) -> "MockERC4626MaxDepositContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626MaxMintContractFunction(ContractFunction):
    """ContractFunction for the maxMint method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str) -> "MockERC4626MaxMintContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626MaxRedeemContractFunction(ContractFunction):
    """ContractFunction for the maxRedeem method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, owner: str) -> "MockERC4626MaxRedeemContractFunction":
        clone = super().__call__(owner)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626MaxWithdrawContractFunction(ContractFunction):
    """ContractFunction for the maxWithdraw method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, owner: str) -> "MockERC4626MaxWithdrawContractFunction":
        clone = super().__call__(owner)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626MintContractFunction(ContractFunction):
    """ContractFunction for the mint method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, _shares: int, _receiver: str) -> "MockERC4626MintContractFunction":
        clone = super().__call__(_shares, _receiver)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626NameContractFunction(ContractFunction):
    """ContractFunction for the name method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626NameContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626NoncesContractFunction(ContractFunction):
    """ContractFunction for the nonces method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, arg1: str) -> "MockERC4626NoncesContractFunction":
        clone = super().__call__(arg1)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626OwnerContractFunction(ContractFunction):
    """ContractFunction for the owner method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626OwnerContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626PermitContractFunction(ContractFunction):
    """ContractFunction for the permit method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(
        self,
        owner: str,
        spender: str,
        value: int,
        deadline: int,
        v: int,
        r: bytes,
        s: bytes,
    ) -> "MockERC4626PermitContractFunction":
        clone = super().__call__(owner, spender, value, deadline, v, r, s)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> None:
        """No return value"""
        super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626PreviewDepositContractFunction(ContractFunction):
    """ContractFunction for the previewDeposit method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, assets: int) -> "MockERC4626PreviewDepositContractFunction":
        clone = super().__call__(assets)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626PreviewMintContractFunction(ContractFunction):
    """ContractFunction for the previewMint method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, shares: int) -> "MockERC4626PreviewMintContractFunction":
        clone = super().__call__(shares)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626PreviewRedeemContractFunction(ContractFunction):
    """ContractFunction for the previewRedeem method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, shares: int) -> "MockERC4626PreviewRedeemContractFunction":
        clone = super().__call__(shares)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626PreviewWithdrawContractFunction(ContractFunction):
    """ContractFunction for the previewWithdraw method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, assets: int) -> "MockERC4626PreviewWithdrawContractFunction":
        clone = super().__call__(assets)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626RedeemContractFunction(ContractFunction):
    """ContractFunction for the redeem method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, _shares: int, _receiver: str, _owner: str) -> "MockERC4626RedeemContractFunction":
        clone = super().__call__(_shares, _receiver, _owner)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626SetAuthorityContractFunction(ContractFunction):
    """ContractFunction for the setAuthority method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, newAuthority: str) -> "MockERC4626SetAuthorityContractFunction":
        clone = super().__call__(newAuthority)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> None:
        """No return value"""
        super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626SetPublicCapabilityContractFunction(ContractFunction):
    """ContractFunction for the setPublicCapability method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, functionSig: bytes, enabled: bool) -> "MockERC4626SetPublicCapabilityContractFunction":
        clone = super().__call__(functionSig, enabled)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> None:
        """No return value"""
        super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626SetRateContractFunction(ContractFunction):
    """ContractFunction for the setRate method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, _rate_: int) -> "MockERC4626SetRateContractFunction":
        clone = super().__call__(_rate_)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> None:
        """No return value"""
        super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626SetRoleCapabilityContractFunction(ContractFunction):
    """ContractFunction for the setRoleCapability method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, role: int, functionSig: bytes, enabled: bool) -> "MockERC4626SetRoleCapabilityContractFunction":
        clone = super().__call__(role, functionSig, enabled)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> None:
        """No return value"""
        super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626SetTargetCustomAuthorityContractFunction(ContractFunction):
    """ContractFunction for the setTargetCustomAuthority method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, target: str, customAuthority: str) -> "MockERC4626SetTargetCustomAuthorityContractFunction":
        clone = super().__call__(target, customAuthority)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> None:
        """No return value"""
        super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626SetUserRoleContractFunction(ContractFunction):
    """ContractFunction for the setUserRole method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, user: str, role: int, enabled: bool) -> "MockERC4626SetUserRoleContractFunction":
        clone = super().__call__(user, role, enabled)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> None:
        """No return value"""
        super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626SymbolContractFunction(ContractFunction):
    """ContractFunction for the symbol method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626SymbolContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> str:
        """returns str"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = str

        return cast(str, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626TotalAssetsContractFunction(ContractFunction):
    """ContractFunction for the totalAssets method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626TotalAssetsContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626TotalSupplyContractFunction(ContractFunction):
    """ContractFunction for the totalSupply method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self) -> "MockERC4626TotalSupplyContractFunction":
        clone = super().__call__()
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626TransferContractFunction(ContractFunction):
    """ContractFunction for the transfer method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, to: str, amount: int) -> "MockERC4626TransferContractFunction":
        clone = super().__call__(to, amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626TransferFromContractFunction(ContractFunction):
    """ContractFunction for the transferFrom method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, _from: str, to: str, amount: int) -> "MockERC4626TransferFromContractFunction":
        clone = super().__call__(_from, to, amount)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> bool:
        """returns bool"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = bool

        return cast(bool, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626TransferOwnershipContractFunction(ContractFunction):
    """ContractFunction for the transferOwnership method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, newOwner: str) -> "MockERC4626TransferOwnershipContractFunction":
        clone = super().__call__(newOwner)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> None:
        """No return value"""
        super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call

        return None

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626WithdrawContractFunction(ContractFunction):
    """ContractFunction for the withdraw method."""

    # super() call methods are generic, while our version adds values & types
    # pylint: disable=arguments-differ

    def __call__(self, _assets: int, _receiver: str, _owner: str) -> "MockERC4626WithdrawContractFunction":
        clone = super().__call__(_assets, _receiver, _owner)
        self.kwargs = clone.kwargs
        self.args = clone.args
        return self

    def call(
        self,
        transaction: TxParams | None = None,
        block_identifier: BlockIdentifier = "latest",
        state_override: CallOverride | None = None,
        ccip_read_enabled: bool | None = None,
    ) -> int:
        """returns int"""
        raw_values = super().call(transaction, block_identifier, state_override, ccip_read_enabled)
        # Define the expected return types from the smart contract call
        return_types = int

        return cast(int, self._call(return_types, raw_values))

    def _call(self, return_types, raw_values):
        # cover case of multiple return values
        if isinstance(return_types, list):
            # Ensure raw_values is a tuple for consistency
            if not isinstance(raw_values, list):
                raw_values = (raw_values,)

            # Convert the tuple to the dataclass instance using the utility function
            converted_values = tuple(
                (tuple_to_dataclass(return_type, value) for return_type, value in zip(return_types, raw_values))
            )

            return converted_values

        # cover case of single return value
        converted_value = tuple_to_dataclass(return_types, raw_values)
        return converted_value


class MockERC4626ContractFunctions(ContractFunctions):
    """ContractFunctions for the MockERC4626 contract."""

    DOMAIN_SEPARATOR: MockERC4626DOMAIN_SEPARATORContractFunction

    allowance: MockERC4626AllowanceContractFunction

    approve: MockERC4626ApproveContractFunction

    asset: MockERC4626AssetContractFunction

    authority: MockERC4626AuthorityContractFunction

    balanceOf: MockERC4626BalanceOfContractFunction

    canCall: MockERC4626CanCallContractFunction

    convertToAssets: MockERC4626ConvertToAssetsContractFunction

    convertToShares: MockERC4626ConvertToSharesContractFunction

    decimals: MockERC4626DecimalsContractFunction

    deposit: MockERC4626DepositContractFunction

    doesRoleHaveCapability: MockERC4626DoesRoleHaveCapabilityContractFunction

    doesUserHaveRole: MockERC4626DoesUserHaveRoleContractFunction

    getRate: MockERC4626GetRateContractFunction

    getRolesWithCapability: MockERC4626GetRolesWithCapabilityContractFunction

    getTargetCustomAuthority: MockERC4626GetTargetCustomAuthorityContractFunction

    getUserRoles: MockERC4626GetUserRolesContractFunction

    isCapabilityPublic: MockERC4626IsCapabilityPublicContractFunction

    isCompetitionMode: MockERC4626IsCompetitionModeContractFunction

    maxDeposit: MockERC4626MaxDepositContractFunction

    maxMint: MockERC4626MaxMintContractFunction

    maxRedeem: MockERC4626MaxRedeemContractFunction

    maxWithdraw: MockERC4626MaxWithdrawContractFunction

    mint: MockERC4626MintContractFunction

    name: MockERC4626NameContractFunction

    nonces: MockERC4626NoncesContractFunction

    owner: MockERC4626OwnerContractFunction

    permit: MockERC4626PermitContractFunction

    previewDeposit: MockERC4626PreviewDepositContractFunction

    previewMint: MockERC4626PreviewMintContractFunction

    previewRedeem: MockERC4626PreviewRedeemContractFunction

    previewWithdraw: MockERC4626PreviewWithdrawContractFunction

    redeem: MockERC4626RedeemContractFunction

    setAuthority: MockERC4626SetAuthorityContractFunction

    setPublicCapability: MockERC4626SetPublicCapabilityContractFunction

    setRate: MockERC4626SetRateContractFunction

    setRoleCapability: MockERC4626SetRoleCapabilityContractFunction

    setTargetCustomAuthority: MockERC4626SetTargetCustomAuthorityContractFunction

    setUserRole: MockERC4626SetUserRoleContractFunction

    symbol: MockERC4626SymbolContractFunction

    totalAssets: MockERC4626TotalAssetsContractFunction

    totalSupply: MockERC4626TotalSupplyContractFunction

    transfer: MockERC4626TransferContractFunction

    transferFrom: MockERC4626TransferFromContractFunction

    transferOwnership: MockERC4626TransferOwnershipContractFunction

    withdraw: MockERC4626WithdrawContractFunction

    def __init__(
        self,
        abi: ABI,
        w3: "Web3",
        address: ChecksumAddress | None = None,
        decode_tuples: bool | None = False,
    ) -> None:
        super().__init__(abi, w3, address, decode_tuples)
        self.DOMAIN_SEPARATOR = MockERC4626DOMAIN_SEPARATORContractFunction.factory(
            "DOMAIN_SEPARATOR",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="DOMAIN_SEPARATOR",
        )
        self.allowance = MockERC4626AllowanceContractFunction.factory(
            "allowance",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="allowance",
        )
        self.approve = MockERC4626ApproveContractFunction.factory(
            "approve",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="approve",
        )
        self.asset = MockERC4626AssetContractFunction.factory(
            "asset",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="asset",
        )
        self.authority = MockERC4626AuthorityContractFunction.factory(
            "authority",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="authority",
        )
        self.balanceOf = MockERC4626BalanceOfContractFunction.factory(
            "balanceOf",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="balanceOf",
        )
        self.canCall = MockERC4626CanCallContractFunction.factory(
            "canCall",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="canCall",
        )
        self.convertToAssets = MockERC4626ConvertToAssetsContractFunction.factory(
            "convertToAssets",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="convertToAssets",
        )
        self.convertToShares = MockERC4626ConvertToSharesContractFunction.factory(
            "convertToShares",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="convertToShares",
        )
        self.decimals = MockERC4626DecimalsContractFunction.factory(
            "decimals",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="decimals",
        )
        self.deposit = MockERC4626DepositContractFunction.factory(
            "deposit",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="deposit",
        )
        self.doesRoleHaveCapability = MockERC4626DoesRoleHaveCapabilityContractFunction.factory(
            "doesRoleHaveCapability",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="doesRoleHaveCapability",
        )
        self.doesUserHaveRole = MockERC4626DoesUserHaveRoleContractFunction.factory(
            "doesUserHaveRole",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="doesUserHaveRole",
        )
        self.getRate = MockERC4626GetRateContractFunction.factory(
            "getRate",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="getRate",
        )
        self.getRolesWithCapability = MockERC4626GetRolesWithCapabilityContractFunction.factory(
            "getRolesWithCapability",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="getRolesWithCapability",
        )
        self.getTargetCustomAuthority = MockERC4626GetTargetCustomAuthorityContractFunction.factory(
            "getTargetCustomAuthority",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="getTargetCustomAuthority",
        )
        self.getUserRoles = MockERC4626GetUserRolesContractFunction.factory(
            "getUserRoles",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="getUserRoles",
        )
        self.isCapabilityPublic = MockERC4626IsCapabilityPublicContractFunction.factory(
            "isCapabilityPublic",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="isCapabilityPublic",
        )
        self.isCompetitionMode = MockERC4626IsCompetitionModeContractFunction.factory(
            "isCompetitionMode",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="isCompetitionMode",
        )
        self.maxDeposit = MockERC4626MaxDepositContractFunction.factory(
            "maxDeposit",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="maxDeposit",
        )
        self.maxMint = MockERC4626MaxMintContractFunction.factory(
            "maxMint",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="maxMint",
        )
        self.maxRedeem = MockERC4626MaxRedeemContractFunction.factory(
            "maxRedeem",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="maxRedeem",
        )
        self.maxWithdraw = MockERC4626MaxWithdrawContractFunction.factory(
            "maxWithdraw",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="maxWithdraw",
        )
        self.mint = MockERC4626MintContractFunction.factory(
            "mint",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="mint",
        )
        self.name = MockERC4626NameContractFunction.factory(
            "name",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="name",
        )
        self.nonces = MockERC4626NoncesContractFunction.factory(
            "nonces",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="nonces",
        )
        self.owner = MockERC4626OwnerContractFunction.factory(
            "owner",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="owner",
        )
        self.permit = MockERC4626PermitContractFunction.factory(
            "permit",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="permit",
        )
        self.previewDeposit = MockERC4626PreviewDepositContractFunction.factory(
            "previewDeposit",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="previewDeposit",
        )
        self.previewMint = MockERC4626PreviewMintContractFunction.factory(
            "previewMint",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="previewMint",
        )
        self.previewRedeem = MockERC4626PreviewRedeemContractFunction.factory(
            "previewRedeem",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="previewRedeem",
        )
        self.previewWithdraw = MockERC4626PreviewWithdrawContractFunction.factory(
            "previewWithdraw",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="previewWithdraw",
        )
        self.redeem = MockERC4626RedeemContractFunction.factory(
            "redeem",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="redeem",
        )
        self.setAuthority = MockERC4626SetAuthorityContractFunction.factory(
            "setAuthority",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="setAuthority",
        )
        self.setPublicCapability = MockERC4626SetPublicCapabilityContractFunction.factory(
            "setPublicCapability",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="setPublicCapability",
        )
        self.setRate = MockERC4626SetRateContractFunction.factory(
            "setRate",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="setRate",
        )
        self.setRoleCapability = MockERC4626SetRoleCapabilityContractFunction.factory(
            "setRoleCapability",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="setRoleCapability",
        )
        self.setTargetCustomAuthority = MockERC4626SetTargetCustomAuthorityContractFunction.factory(
            "setTargetCustomAuthority",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="setTargetCustomAuthority",
        )
        self.setUserRole = MockERC4626SetUserRoleContractFunction.factory(
            "setUserRole",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="setUserRole",
        )
        self.symbol = MockERC4626SymbolContractFunction.factory(
            "symbol",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="symbol",
        )
        self.totalAssets = MockERC4626TotalAssetsContractFunction.factory(
            "totalAssets",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="totalAssets",
        )
        self.totalSupply = MockERC4626TotalSupplyContractFunction.factory(
            "totalSupply",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="totalSupply",
        )
        self.transfer = MockERC4626TransferContractFunction.factory(
            "transfer",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="transfer",
        )
        self.transferFrom = MockERC4626TransferFromContractFunction.factory(
            "transferFrom",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="transferFrom",
        )
        self.transferOwnership = MockERC4626TransferOwnershipContractFunction.factory(
            "transferOwnership",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="transferOwnership",
        )
        self.withdraw = MockERC4626WithdrawContractFunction.factory(
            "withdraw",
            w3=w3,
            contract_abi=abi,
            address=address,
            decode_tuples=decode_tuples,
            function_identifier="withdraw",
        )


mockerc4626_abi: ABI = cast(
    ABI,
    [
        {
            "inputs": [
                {
                    "internalType": "contract ERC20Mintable",
                    "name": "_asset",
                    "type": "address",
                },
                {"internalType": "string", "name": "_name", "type": "string"},
                {"internalType": "string", "name": "_symbol", "type": "string"},
                {
                    "internalType": "uint256",
                    "name": "_initialRate",
                    "type": "uint256",
                },
                {
                    "internalType": "address",
                    "name": "_admin",
                    "type": "address",
                },
                {
                    "internalType": "bool",
                    "name": "_isCompetitionMode",
                    "type": "bool",
                },
            ],
            "stateMutability": "nonpayable",
            "type": "constructor",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "owner",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "spender",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Approval",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "contract Authority",
                    "name": "newAuthority",
                    "type": "address",
                },
            ],
            "name": "AuthorityUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "caller",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "owner",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "assets",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "shares",
                    "type": "uint256",
                },
            ],
            "name": "Deposit",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address",
                },
            ],
            "name": "OwnershipTransferred",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "enabled",
                    "type": "bool",
                },
            ],
            "name": "PublicCapabilityUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint8",
                    "name": "role",
                    "type": "uint8",
                },
                {
                    "indexed": True,
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "enabled",
                    "type": "bool",
                },
            ],
            "name": "RoleCapabilityUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "target",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "contract Authority",
                    "name": "authority",
                    "type": "address",
                },
            ],
            "name": "TargetCustomAuthorityUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "from",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Transfer",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "user",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "uint8",
                    "name": "role",
                    "type": "uint8",
                },
                {
                    "indexed": False,
                    "internalType": "bool",
                    "name": "enabled",
                    "type": "bool",
                },
            ],
            "name": "UserRoleUpdated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "caller",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "receiver",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "owner",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "assets",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "shares",
                    "type": "uint256",
                },
            ],
            "name": "Withdraw",
            "type": "event",
        },
        {
            "inputs": [],
            "name": "DOMAIN_SEPARATOR",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"},
                {"internalType": "address", "name": "", "type": "address"},
            ],
            "name": "allowance",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "spender",
                    "type": "address",
                },
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "approve",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "asset",
            "outputs": [
                {
                    "internalType": "contract ERC20",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "authority",
            "outputs": [
                {
                    "internalType": "contract Authority",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "user", "type": "address"},
                {
                    "internalType": "address",
                    "name": "target",
                    "type": "address",
                },
                {
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
            ],
            "name": "canCall",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "shares", "type": "uint256"}],
            "name": "convertToAssets",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "assets", "type": "uint256"}],
            "name": "convertToShares",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "decimals",
            "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_assets",
                    "type": "uint256",
                },
                {
                    "internalType": "address",
                    "name": "_receiver",
                    "type": "address",
                },
            ],
            "name": "deposit",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint8", "name": "role", "type": "uint8"},
                {
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
            ],
            "name": "doesRoleHaveCapability",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint8", "name": "role", "type": "uint8"},
            ],
            "name": "doesUserHaveRole",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "getRate",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
            "name": "getRolesWithCapability",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "", "type": "address"}],
            "name": "getTargetCustomAuthority",
            "outputs": [
                {
                    "internalType": "contract Authority",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "", "type": "address"}],
            "name": "getUserRoles",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
            "name": "isCapabilityPublic",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "isCompetitionMode",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "", "type": "address"}],
            "name": "maxDeposit",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "", "type": "address"}],
            "name": "maxMint",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
            "name": "maxRedeem",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
            "name": "maxWithdraw",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_shares",
                    "type": "uint256",
                },
                {
                    "internalType": "address",
                    "name": "_receiver",
                    "type": "address",
                },
            ],
            "name": "mint",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "", "type": "address"}],
            "name": "nonces",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "owner", "type": "address"},
                {
                    "internalType": "address",
                    "name": "spender",
                    "type": "address",
                },
                {"internalType": "uint256", "name": "value", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "deadline",
                    "type": "uint256",
                },
                {"internalType": "uint8", "name": "v", "type": "uint8"},
                {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                {"internalType": "bytes32", "name": "s", "type": "bytes32"},
            ],
            "name": "permit",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "assets", "type": "uint256"}],
            "name": "previewDeposit",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "shares", "type": "uint256"}],
            "name": "previewMint",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "shares", "type": "uint256"}],
            "name": "previewRedeem",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "assets", "type": "uint256"}],
            "name": "previewWithdraw",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_shares",
                    "type": "uint256",
                },
                {
                    "internalType": "address",
                    "name": "_receiver",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "_owner",
                    "type": "address",
                },
            ],
            "name": "redeem",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "contract Authority",
                    "name": "newAuthority",
                    "type": "address",
                }
            ],
            "name": "setAuthority",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
                {"internalType": "bool", "name": "enabled", "type": "bool"},
            ],
            "name": "setPublicCapability",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "_rate_", "type": "uint256"}],
            "name": "setRate",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint8", "name": "role", "type": "uint8"},
                {
                    "internalType": "bytes4",
                    "name": "functionSig",
                    "type": "bytes4",
                },
                {"internalType": "bool", "name": "enabled", "type": "bool"},
            ],
            "name": "setRoleCapability",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "target",
                    "type": "address",
                },
                {
                    "internalType": "contract Authority",
                    "name": "customAuthority",
                    "type": "address",
                },
            ],
            "name": "setTargetCustomAuthority",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint8", "name": "role", "type": "uint8"},
                {"internalType": "bool", "name": "enabled", "type": "bool"},
            ],
            "name": "setUserRole",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "symbol",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "totalAssets",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "to", "type": "address"},
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "transfer",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "from", "type": "address"},
                {"internalType": "address", "name": "to", "type": "address"},
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "transferFrom",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address",
                }
            ],
            "name": "transferOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_assets",
                    "type": "uint256",
                },
                {
                    "internalType": "address",
                    "name": "_receiver",
                    "type": "address",
                },
                {
                    "internalType": "address",
                    "name": "_owner",
                    "type": "address",
                },
            ],
            "name": "withdraw",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ],
)
# pylint: disable=line-too-long
mockerc4626_bytecode = HexStr(
    "0x6101206040523480156200001257600080fd5b50604051620027ea380380620027ea833981016040819052620000359162000310565b813081818989898181846001600160a01b031663313ce5676040518163ffffffff1660e01b8152600401602060405180830381865afa1580156200007d573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190620000a39190620003c8565b6000620000b1848262000483565b506001620000c0838262000483565b5060ff81166080524660a052620000d662000196565b60c0525050506001600160a01b0392831660e0525050600680548483166001600160a01b0319918216811790925560078054938516939091169290921790915560405133907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e090600090a36040516001600160a01b0382169033907fa3396fd7f6e0a21b50e5089d2da70d5ac0a3bbbd1f617a93f134b7638998019890600090a3505050600c9390935542600d5515156101005250620005cd9350505050565b60007f8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f6000604051620001ca91906200054f565b6040805191829003822060208301939093528101919091527fc89efdaa54c0f20c7adf612882df0950f5a951637e0307cdcb4c672f298b8bc660608201524660808201523060a082015260c00160405160208183030381529060405280519060200120905090565b6001600160a01b03811681146200024857600080fd5b50565b634e487b7160e01b600052604160045260246000fd5b600082601f8301126200027357600080fd5b81516001600160401b03808211156200029057620002906200024b565b604051601f8301601f19908116603f01168101908282118183101715620002bb57620002bb6200024b565b81604052838152602092508683858801011115620002d857600080fd5b600091505b83821015620002fc5785820183015181830184015290820190620002dd565b600093810190920192909252949350505050565b60008060008060008060c087890312156200032a57600080fd5b8651620003378162000232565b60208801519096506001600160401b03808211156200035557600080fd5b620003638a838b0162000261565b965060408901519150808211156200037a57600080fd5b506200038989828a0162000261565b945050606087015192506080870151620003a38162000232565b60a08801519092508015158114620003ba57600080fd5b809150509295509295509295565b600060208284031215620003db57600080fd5b815160ff81168114620003ed57600080fd5b9392505050565b600181811c908216806200040957607f821691505b6020821081036200042a57634e487b7160e01b600052602260045260246000fd5b50919050565b601f8211156200047e57600081815260208120601f850160051c81016020861015620004595750805b601f850160051c820191505b818110156200047a5782815560010162000465565b5050505b505050565b81516001600160401b038111156200049f576200049f6200024b565b620004b781620004b08454620003f4565b8462000430565b602080601f831160018114620004ef5760008415620004d65750858301515b600019600386901b1c1916600185901b1785556200047a565b600085815260208120601f198616915b828110156200052057888601518255948401946001909101908401620004ff565b50858210156200053f5787850151600019600388901b60f8161c191681555b5050505050600190811b01905550565b60008083546200055f81620003f4565b600182811680156200057a57600181146200059057620005c1565b60ff1984168752821515830287019450620005c1565b8760005260208060002060005b85811015620005b85781548a8201529084019082016200059d565b50505082870194505b50929695505050505050565b60805160a05160c05160e051610100516121a06200064a600039600081816104b00152610aba0152600081816103d50152818161072d015281816113d501528181611563015281816116c101528181611759015281816118ab01526119ed01526000610b8101526000610b510152600061038101526121a06000f3fe608060405234801561001057600080fd5b506004361061028a5760003560e01c80637a9e5e4b1161015c578063c53a3985116100ce578063dd62ed3e11610087578063dd62ed3e14610630578063e688747b1461065b578063ea7ca27614610691578063ed0d0efb146106c8578063ef8b30f7146106e8578063f2fde38b146106fb57600080fd5b8063c53a3985146105a5578063c63d75b61461040f578063c6e6f592146105ce578063ce96cb77146105e1578063d505accf146105f4578063d905777e1461060757600080fd5b8063a9059cbb11610120578063a9059cbb14610533578063b3d7f6b914610546578063b460af9414610559578063b70096131461056c578063ba0876521461057f578063bf7e214f1461059257600080fd5b80637a9e5e4b146104d25780637ecebe00146104e55780638da5cb5b1461050557806394bf804d1461051857806395d89b411461052b57600080fd5b806334fcf43711610200578063679aefce116101b9578063679aefce1461044a57806367aff484146104525780636e553f651461046557806370a0823114610478578063728b952b146104985780637a8c63b5146104ab57600080fd5b806334fcf437146103b55780633644e515146103c857806338d52e0f146103d0578063402d267d1461040f5780634b5159da146104245780634cdad5061461043757600080fd5b80630a28a477116102525780630a28a477146103155780630bade8a4146103285780630ea9b75b1461034b57806318160ddd1461036057806323b872dd14610369578063313ce5671461037c57600080fd5b806301e1d1141461028f57806306a36aee146102aa57806306fdde03146102ca57806307a2d13a146102df578063095ea7b3146102f2575b600080fd5b61029761070e565b6040519081526020015b60405180910390f35b6102976102b8366004611c1a565b60096020526000908152604090205481565b6102d26107af565b6040516102a19190611c37565b6102976102ed366004611c85565b61083d565b610305610300366004611c9e565b61086a565b60405190151581526020016102a1565b610297610323366004611c85565b6108d7565b610305610336366004611ce7565b600a6020526000908152604090205460ff1681565b61035e610359366004611d21565b6108f7565b005b61029760025481565b610305610377366004611d68565b6109d8565b6103a37f000000000000000000000000000000000000000000000000000000000000000081565b60405160ff90911681526020016102a1565b61035e6103c3366004611c85565b610ab8565b610297610b4d565b6103f77f000000000000000000000000000000000000000000000000000000000000000081565b6040516001600160a01b0390911681526020016102a1565b61029761041d366004611c1a565b5060001990565b61035e610432366004611da9565b610ba3565b610297610445366004611c85565b610c35565b600c54610297565b61035e610460366004611de0565b610c40565b610297610473366004611e0e565b610d08565b610297610486366004611c1a565b60036020526000908152604090205481565b61035e6104a6366004611e33565b610d1c565b6103057f000000000000000000000000000000000000000000000000000000000000000081565b61035e6104e0366004611c1a565b610da5565b6102976104f3366004611c1a565b60056020526000908152604090205481565b6006546103f7906001600160a01b031681565b610297610526366004611e0e565b610e8f565b6102d2610ea3565b610305610541366004611c9e565b610eb0565b610297610554366004611c85565b610f16565b610297610567366004611e61565b610f35565b61030561057a366004611e98565b610f52565b61029761058d366004611e61565b611050565b6007546103f7906001600160a01b031681565b6103f76105b3366004611c1a565b6008602052600090815260409020546001600160a01b031681565b6102976105dc366004611c85565b611065565b6102976105ef366004611c1a565b611085565b61035e610602366004611edf565b6110a7565b610297610615366004611c1a565b6001600160a01b031660009081526003602052604090205490565b61029761063e366004611e33565b600460209081526000928352604080842090915290825290205481565b610305610669366004611f4d565b6001600160e01b0319166000908152600b602052604090205460ff919091161c600116151590565b61030561069f366004611f80565b6001600160a01b0391909116600090815260096020526040902054600160ff9092161c16151590565b6102976106d6366004611ce7565b600b6020526000908152604090205481565b6102976106f6366004611c85565b6112eb565b61035e610709366004611c1a565b6112f6565b6000610718611374565b6040516370a0823160e01b81523060048201527f00000000000000000000000000000000000000000000000000000000000000006001600160a01b0316906370a0823190602401602060405180830381865afa15801561077c573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906107a09190611fac565b6107aa9190611fdb565b905090565b600080546107bc90611fee565b80601f01602080910402602001604051908101604052809291908181526020018280546107e890611fee565b80156108355780601f1061080a57610100808354040283529160200191610835565b820191906000526020600020905b81548152906001019060200180831161081857829003601f168201915b505050505081565b60025460009080156108615761085c61085461070e565b84908361144e565b610863565b825b9392505050565b3360008181526004602090815260408083206001600160a01b038716808552925280832085905551919290917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925906108c59086815260200190565b60405180910390a35060015b92915050565b60025460009080156108615761085c816108ef61070e565b85919061146c565b61090d336000356001600160e01b031916611492565b6109325760405162461bcd60e51b815260040161092990612028565b60405180910390fd5b8015610962576001600160e01b031982166000908152600b602052604090208054600160ff86161b179055610989565b6001600160e01b031982166000908152600b602052604090208054600160ff86161b191690555b816001600160e01b0319168360ff167fbfe16b2c35ce23dfd1ab0e7b5d086a10060c9b52d1574e1680c881b3b3a2b151836040516109cb911515815260200190565b60405180910390a3505050565b6001600160a01b03831660009081526004602090815260408083203384529091528120546000198114610a3457610a0f838261204e565b6001600160a01b03861660009081526004602090815260408083203384529091529020555b6001600160a01b03851660009081526003602052604081208054859290610a5c90849061204e565b90915550506001600160a01b038085166000818152600360205260409081902080548701905551909187169060008051602061214b83398151915290610aa59087815260200190565b60405180910390a3506001949350505050565b7f000000000000000000000000000000000000000000000000000000000000000015610b4057610af4336000356001600160e01b031916611492565b610b405760405162461bcd60e51b815260206004820152601b60248201527f4d6f636b455243343632363a206e6f7420617574686f72697a656400000000006044820152606401610929565b610b4861153b565b600c55565b60007f00000000000000000000000000000000000000000000000000000000000000004614610b7e576107aa6115cf565b507f000000000000000000000000000000000000000000000000000000000000000090565b610bb9336000356001600160e01b031916611492565b610bd55760405162461bcd60e51b815260040161092990612028565b6001600160e01b031982166000818152600a6020908152604091829020805460ff191685151590811790915591519182527f36d28126bef21a4f3765d7fcb7c45cead463ae4c41094ef3b771ede598544103910160405180910390a25050565b60006108d18261083d565b610c56336000356001600160e01b031916611492565b610c725760405162461bcd60e51b815260040161092990612028565b8015610ca1576001600160a01b03831660009081526009602052604090208054600160ff85161b179055610cc7565b6001600160a01b03831660009081526009602052604090208054600160ff85161b191690555b8160ff16836001600160a01b03167f4c9bdd0c8e073eb5eda2250b18d8e5121ff27b62064fbeeeed4869bb99bc5bf2836040516109cb911515815260200190565b6000610d1261153b565b6108638383611669565b610d32336000356001600160e01b031916611492565b610d4e5760405162461bcd60e51b815260040161092990612028565b6001600160a01b0382811660008181526008602052604080822080546001600160a01b0319169486169485179055517fa4908e11a5f895b13d51526c331ac93cdd30e59772361c5d07874eb36bff20659190a35050565b6006546001600160a01b0316331480610e3a575060075460405163b700961360e01b81526001600160a01b039091169063b700961390610df990339030906001600160e01b03196000351690600401612061565b602060405180830381865afa158015610e16573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610e3a919061208e565b610e4357600080fd5b600780546001600160a01b0319166001600160a01b03831690811790915560405133907fa3396fd7f6e0a21b50e5089d2da70d5ac0a3bbbd1f617a93f134b7638998019890600090a350565b6000610e9961153b565b610863838361173f565b600180546107bc90611fee565b33600090815260036020526040812080548391908390610ed190849061204e565b90915550506001600160a01b0383166000818152600360205260409081902080548501905551339060008051602061214b833981519152906108c59086815260200190565b60025460009080156108615761085c610f2d61070e565b84908361146c565b6000610f3f61153b565b610f4a8484846117ce565b949350505050565b6001600160a01b038083166000908152600860205260408120549091168015610fee5760405163b700961360e01b81526001600160a01b0382169063b700961390610fa590889088908890600401612061565b602060405180830381865afa158015610fc2573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610fe6919061208e565b915050610863565b6001600160e01b031983166000908152600a602052604090205460ff168061104757506001600160e01b031983166000908152600b60209081526040808320546001600160a01b03891684526009909252909120541615155b95945050505050565b600061105a61153b565b610f4a8484846118d2565b60025460009080156108615761085c8161107d61070e565b85919061144e565b6001600160a01b0381166000908152600360205260408120546108d19061083d565b428410156110f75760405162461bcd60e51b815260206004820152601760248201527f5045524d49545f444541444c494e455f455850495245440000000000000000006044820152606401610929565b60006001611103610b4d565b6001600160a01b038a811660008181526005602090815260409182902080546001810190915582517f6e71edae12b1b97f4d1f60370fef10105fa2faae0126114a169c64845d6126c98184015280840194909452938d166060840152608083018c905260a083019390935260c08083018b90528151808403909101815260e08301909152805192019190912061190160f01b6101008301526101028201929092526101228101919091526101420160408051601f198184030181528282528051602091820120600084529083018083525260ff871690820152606081018590526080810184905260a0016020604051602081039080840390855afa15801561120f573d6000803e3d6000fd5b5050604051601f1901519150506001600160a01b038116158015906112455750876001600160a01b0316816001600160a01b0316145b6112825760405162461bcd60e51b815260206004820152600e60248201526d24a72b20a624a22fa9a4a3a722a960911b6044820152606401610929565b6001600160a01b0390811660009081526004602090815260408083208a8516808552908352928190208990555188815291928a16917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925910160405180910390a350505050505050565b60006108d182611065565b61130c336000356001600160e01b031916611492565b6113285760405162461bcd60e51b815260040161092990612028565b600680546001600160a01b0319166001600160a01b03831690811790915560405133907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e090600090a350565b6000600c546000036113865750600090565b60006113a46301e13380600d544261139e919061204e565b90611a14565b905060006108636113c083600c54611a2990919063ffffffff16565b6040516370a0823160e01b81523060048201527f00000000000000000000000000000000000000000000000000000000000000006001600160a01b0316906370a0823190602401602060405180830381865afa158015611424573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906114489190611fac565b90611a29565b600082600019048411830215820261146557600080fd5b5091020490565b600082600019048411830215820261148357600080fd5b50910281810615159190040190565b6007546000906001600160a01b0316801580159061151c575060405163b700961360e01b81526001600160a01b0382169063b7009613906114db90879030908890600401612061565b602060405180830381865afa1580156114f8573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061151c919061208e565b80610f4a57506006546001600160a01b03858116911614949350505050565b6000611545611374565b905080156115c85760405163140e25ad60e31b8152600481018290527f00000000000000000000000000000000000000000000000000000000000000006001600160a01b03169063a0712d6890602401600060405180830381600087803b1580156115af57600080fd5b505af11580156115c3573d6000803e3d6000fd5b505050505b5042600d55565b60007f8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f600060405161160191906120ab565b6040805191829003822060208301939093528101919091527fc89efdaa54c0f20c7adf612882df0950f5a951637e0307cdcb4c672f298b8bc660608201524660808201523060a082015260c00160405160208183030381529060405280519060200120905090565b6000611674836112eb565b9050806000036116b45760405162461bcd60e51b815260206004820152600b60248201526a5a45524f5f53484152455360a81b6044820152606401610929565b6116e96001600160a01b037f000000000000000000000000000000000000000000000000000000000000000016333086611a3e565b6116f38282611ac8565b60408051848152602081018390526001600160a01b0384169133917fdcbc1c05240f31ff3ad067ef1ee35ce4997762752e3a095284754544f4c709d791015b60405180910390a36108d1565b600061174a83610f16565b90506117816001600160a01b037f000000000000000000000000000000000000000000000000000000000000000016333084611a3e565b61178b8284611ac8565b60408051828152602081018590526001600160a01b0384169133917fdcbc1c05240f31ff3ad067ef1ee35ce4997762752e3a095284754544f4c709d79101611732565b60006117d9846108d7565b9050336001600160a01b03831614611849576001600160a01b0382166000908152600460209081526040808320338452909152902054600019811461184757611822828261204e565b6001600160a01b03841660009081526004602090815260408083203384529091529020555b505b6118538282611b22565b60408051858152602081018390526001600160a01b03808516929086169133917ffbde797d201c681b91056529119e0b02407c7bb96a4a2c75c01fc9667232c8db910160405180910390a46108636001600160a01b037f0000000000000000000000000000000000000000000000000000000000000000168486611b84565b6000336001600160a01b03831614611942576001600160a01b038216600090815260046020908152604080832033845290915290205460001981146119405761191b858261204e565b6001600160a01b03841660009081526004602090815260408083203384529091529020555b505b61194b84610c35565b90508060000361198b5760405162461bcd60e51b815260206004820152600b60248201526a5a45524f5f41535345545360a81b6044820152606401610929565b6119958285611b22565b60408051828152602081018690526001600160a01b03808516929086169133917ffbde797d201c681b91056529119e0b02407c7bb96a4a2c75c01fc9667232c8db910160405180910390a46108636001600160a01b037f0000000000000000000000000000000000000000000000000000000000000000168483611b84565b600061086383670de0b6b3a76400008461144e565b60006108638383670de0b6b3a764000061144e565b60006040516323b872dd60e01b81528460048201528360248201528260448201526020600060648360008a5af13d15601f3d1160016000511416171691505080611ac15760405162461bcd60e51b81526020600482015260146024820152731514905394d1915497d19493d357d1905253115160621b6044820152606401610929565b5050505050565b8060026000828254611ada9190611fdb565b90915550506001600160a01b03821660008181526003602090815260408083208054860190555184815260008051602061214b83398151915291015b60405180910390a35050565b6001600160a01b03821660009081526003602052604081208054839290611b4a90849061204e565b90915550506002805482900390556040518181526000906001600160a01b0384169060008051602061214b83398151915290602001611b16565b600060405163a9059cbb60e01b8152836004820152826024820152602060006044836000895af13d15601f3d1160016000511416171691505080611bfc5760405162461bcd60e51b815260206004820152600f60248201526e1514905394d1915497d19052531151608a1b6044820152606401610929565b50505050565b6001600160a01b0381168114611c1757600080fd5b50565b600060208284031215611c2c57600080fd5b813561086381611c02565b600060208083528351808285015260005b81811015611c6457858101830151858201604001528201611c48565b506000604082860101526040601f19601f8301168501019250505092915050565b600060208284031215611c9757600080fd5b5035919050565b60008060408385031215611cb157600080fd5b8235611cbc81611c02565b946020939093013593505050565b80356001600160e01b031981168114611ce257600080fd5b919050565b600060208284031215611cf957600080fd5b61086382611cca565b803560ff81168114611ce257600080fd5b8015158114611c1757600080fd5b600080600060608486031215611d3657600080fd5b611d3f84611d02565b9250611d4d60208501611cca565b91506040840135611d5d81611d13565b809150509250925092565b600080600060608486031215611d7d57600080fd5b8335611d8881611c02565b92506020840135611d9881611c02565b929592945050506040919091013590565b60008060408385031215611dbc57600080fd5b611dc583611cca565b91506020830135611dd581611d13565b809150509250929050565b600080600060608486031215611df557600080fd5b8335611e0081611c02565b9250611d4d60208501611d02565b60008060408385031215611e2157600080fd5b823591506020830135611dd581611c02565b60008060408385031215611e4657600080fd5b8235611e5181611c02565b91506020830135611dd581611c02565b600080600060608486031215611e7657600080fd5b833592506020840135611e8881611c02565b91506040840135611d5d81611c02565b600080600060608486031215611ead57600080fd5b8335611eb881611c02565b92506020840135611ec881611c02565b9150611ed660408501611cca565b90509250925092565b600080600080600080600060e0888a031215611efa57600080fd5b8735611f0581611c02565b96506020880135611f1581611c02565b95506040880135945060608801359350611f3160808901611d02565b925060a0880135915060c0880135905092959891949750929550565b60008060408385031215611f6057600080fd5b611f6983611d02565b9150611f7760208401611cca565b90509250929050565b60008060408385031215611f9357600080fd5b8235611f9e81611c02565b9150611f7760208401611d02565b600060208284031215611fbe57600080fd5b5051919050565b634e487b7160e01b600052601160045260246000fd5b808201808211156108d1576108d1611fc5565b600181811c9082168061200257607f821691505b60208210810361202257634e487b7160e01b600052602260045260246000fd5b50919050565b6020808252600c908201526b15539055551213d49256915160a21b604082015260600190565b818103818111156108d1576108d1611fc5565b6001600160a01b0393841681529190921660208201526001600160e01b0319909116604082015260600190565b6000602082840312156120a057600080fd5b815161086381611d13565b600080835481600182811c9150808316806120c757607f831692505b602080841082036120e657634e487b7160e01b86526022600452602486fd5b8180156120fa576001811461210f5761213c565b60ff198616895284151585028901965061213c565b60008a81526020902060005b868110156121345781548b82015290850190830161211b565b505084890196505b50949897505050505050505056feddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3efa26469706673582212207b9aa166d629a6b0e6b8b077a9cd39bae89feaf6247253ddfce1492ebfd31b0864736f6c63430008130033"
)


class MockERC4626Contract(Contract):
    """A web3.py Contract class for the MockERC4626 contract."""

    abi: ABI = mockerc4626_abi
    bytecode: bytes = HexBytes(mockerc4626_bytecode)

    def __init__(self, address: ChecksumAddress | None = None) -> None:
        try:
            # Initialize parent Contract class
            super().__init__(address=address)
            self.functions = MockERC4626ContractFunctions(mockerc4626_abi, self.w3, address)

        except FallbackNotFound:
            print("Fallback function not found. Continuing...")

    # TODO: add events
    # events: ERC20ContractEvents

    functions: MockERC4626ContractFunctions

    @classmethod
    def factory(cls, w3: Web3, class_name: str | None = None, **kwargs: Any) -> Type[Self]:
        contract = super().factory(w3, class_name, **kwargs)
        contract.functions = MockERC4626ContractFunctions(mockerc4626_abi, w3, None)

        return contract