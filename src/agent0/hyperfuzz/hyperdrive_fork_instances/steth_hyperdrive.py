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
from agent0.hypertypes import StETHHyperdriveTestContract


class StethHyperdrive(LocalHyperdrive):
    """Steth hyperdrive instance that connects to the mainnet steth yield source."""

    # We overwrite deploy functions for steth hyperdrive
    def _deploy_hyperdrive(self, config: LocalHyperdrive.Config, chain: LocalChain):

        (factory_deploy_config, pool_deploy_config) = self._build_deploy_config(config)
        deployer_account = chain.get_deployer_account()

        # Deploy the factory
        deployed_hyperdrive_factory = deploy_hyperdrive_factory(
            chain._web3,
            deployer_account,
            factory_deploy_config,
        )

        # Deploy the test instance
        test_instance_contract = StETHHyperdriveTestContract.deploy(
            chain._web3,
            deployer_account,
        )

        # Use the test instance to deploy the coordinator
        deploy_function = test_instance_contract.functions.deployCoordinator(
            deployed_hyperdrive_factory.factory_contract.address
        )
        function_name = deploy_function.fn_name
        function_args = deploy_function.args
        receipt = smart_contract_transact(
            chain._web3,
            test_instance_contract,
            deployer_account,
            function_name,
            *function_args,
        )
        if receipt["status"] != 1:
            raise ValueError(f"Failed adding the Hyperdrive deployer to the factory.\n{receipt=}")

        # TODO get the returned coordinator address
        pass

        # Add the
