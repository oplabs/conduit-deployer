""" Deploy a Seaport conduit deployer that opens a channel to Seaport and
transfers ownership. """
import click
from ape import accounts, project
from ape.cli import network_option, NetworkBoundCommand
from eth_abi import decode
from eth_utils import encode_hex, to_checksum_address

# NewConduit(address,bytes32)
NEW_CONDUIT = "0x4397af6128d529b8ae0442f99db1296d5136062597a15bbc61c1b2a6431a7d15"
SEAPORT_14 = "0x00000000000001ad428e4906aE43D8F9852d0dD6"


@click.command(cls=NetworkBoundCommand)
@network_option()
@click.option("-a", "--account", help="Account to use for deployment")
@click.option(
    "-o",
    "--owner",
    type=str,
    required=True,
    help="The prefix characters to generate for",
)
def cli(
    network,
    account,
    owner,
):
    deployer = accounts.load(account) if account else accounts[0]

    if "-fork" in network:
        # Hardhat 0 account
        accounts.test_accounts["0x1e59ce931B4CFea3fe4B875411e280e173cB7A9C"].transfer(
            deployer, int(1e17)
        )

    print(f"Deploying conduit using {deployer}")

    deploy_conduit = deployer.deploy(project.DeployConduit, owner)

    print(f"Deployment tx: {deploy_conduit.receipt.txn_hash}")

    new_conduit_ev = next(
        log
        for log in deploy_conduit.receipt.logs
        if log["topics"][0].hex() == NEW_CONDUIT
    )
    conduit_address, conduit_key = decode(
        ["address", "bytes32"], new_conduit_ev["data"]
    )
    conduit_address = to_checksum_address(conduit_address)

    print(f"Conduit Key: {encode_hex(conduit_key)}")
    print(f"Conduit Address: {conduit_address}")

    conduit_controller = project.ConduitControllerInterface.at(
        "0x00000000F9490004C11Cef243f5400493c00Ad63"
    )

    known_address, exists = conduit_controller.getConduit(conduit_key)

    # Validate deployment
    assert exists is True
    assert known_address == conduit_address
    assert deploy_conduit.address == conduit_controller.ownerOf(conduit_address)
    assert owner == conduit_controller.getPotentialOwner(conduit_address)
    assert conduit_key == conduit_controller.getKey(conduit_address)
    assert conduit_controller.getChannelStatus(conduit_address, SEAPORT_14) is True
