import eth_abi
from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from fixedpointmath import FixedPoint
from hexbytes import HexBytes
from web3.types import RPCEndpoint

from agent0 import LocalChain, LocalHyperdrive
from agent0.ethpy.base import (
    ETH_CONTRACT_ADDRESS,
    get_account_balance,
    set_anvil_account_balance,
    smart_contract_transact,
)
from agent0.ethpy.hyperdrive import (
    DeployedHyperdriveFactory,
    DeployedHyperdrivePool,
    HyperdriveDeployType,
    deploy_base_and_vault,
    deploy_hyperdrive_coordinator,
    deploy_hyperdrive_factory,
    deploy_hyperdrive_from_factory,
)
from agent0.hypertypes import LPMathContract, StETHHyperdriveTestContract
from agent0.hypertypes.types.StETHHyperdriveTestContract import stethhyperdrivetest_bytecode


class StethHyperdrive(LocalHyperdrive):
    """Steth hyperdrive instance that connects to the mainnet steth yield source."""

    # We overwrite deploy functions for steth hyperdrive
    def _deploy_hyperdrive(self, config: LocalHyperdrive.Config, chain: LocalChain):

        # The test instance contract assumes a specific account
        # when deploying.
        # TODO we hard code this for now, but we should be able to replicate
        # the mapping that is done in solidity:
        # https://github.com/delvtech/hyperdrive/blob/98e3419e188300f7729c61d9fe4acc81764f72b4/test/utils/BaseTest.sol#L70
        alice_addr = "0x901eE2C858917C6ff3dd81F7b4710078123489F3"

        # Call anvil's impersonate account on this address
        response = chain._web3.provider.make_request(
            method=RPCEndpoint("anvil_impersonateAccount"), params=[alice_addr]
        )
        # ensure response is valid
        if "result" not in response:
            raise KeyError("Response did not have a result.")

        # We explicitly call set_anvil_account_balance to fund alice
        _ = set_anvil_account_balance(chain._web3, alice_addr, FixedPoint(100).scaled_value)

        (factory_deploy_config, pool_deploy_config) = self._build_deploy_config(config)

        # Since we can't create a LocalAccount for an impersonated address,
        # we use a separate deployer for deploying things on our side
        deployer_account = chain.get_deployer_account()

        # Deploy the factory
        deployed_hyperdrive_factory = deploy_hyperdrive_factory(
            chain._web3,
            deployer_account,
            factory_deploy_config,
        )

        # Deploy the LP math contract
        lp_math_contract = LPMathContract.deploy(w3=chain._web3, account=deployer_account)
        # Deploying the target deployer contracts requires linking to the LPMath contract.
        # We do this by replacing the `linked_str` pattern with address of lp_math_contract.
        # The `linked_str` pattern is the identifier of the LP Math contract for
        # "contracts/src/libraries/LPMath.sol"
        linked_str = "__$2b4fa6f02a36eedfe41c65e8dd342257d3$__"
        linked_contract_addr = lp_math_contract.address[2:].lower()
        StETHHyperdriveTestContract.bytecode = HexBytes(
            str(stethhyperdrivetest_bytecode).replace(linked_str, linked_contract_addr)
        )

        # Deploy the test instance
        test_instance_contract = StETHHyperdriveTestContract.deploy(
            chain._web3,
            deployer_account,
        )

        # Use the test instance to deploy the coordinator using
        out = test_instance_contract.functions.deployCoordinator(
            deployed_hyperdrive_factory.factory_contract.address
        ).transact({"from": alice_addr, "gas": int(1e8)})
        pass
        # function_name = deploy_function.fn_name
        # function_args = deploy_function.args
        # receipt = smart_contract_transact(
        #     chain._web3,
        #     test_instance_contract,
        #     alice_addr,
        #     function_name,
        #     *function_args,
        # )
        # if receipt["status"] != 1:
        #     raise ValueError(f"Failed adding the Hyperdrive deployer to the factory.\n{receipt=}")

        # TODO get the returned coordinator address
        pass

        # Add the
