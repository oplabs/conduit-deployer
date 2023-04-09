""" Generate a private key for a deployer account that will deploy a Seaport
conduit with a vanity address with the given prefix """
import click
import rlp
from ape_test import TestAccount
from ape.cli import network_option, NetworkBoundCommand
from eth_account import Account
from eth_utils import encode_hex, decode_hex, to_checksum_address
from web3 import Web3

CONDUIT_CONTROLLER = "0x00000000F9490004C11Cef243f5400493c00Ad63"
CREATION_CODE_HASH = (
    "0x023d904f2503c37127200ca07b976c3a53cc562623f67023115bf311f5805059"
)


def derive_deploy_address(eoa, nonce=0):
    """Figure out what the address for the deployed contract would be"""
    return to_checksum_address(
        encode_hex(Web3.keccak(rlp.encode([decode_hex(eoa), nonce])))[26:]
    )


def derive_conduit_address(controller, conduit_key, conduit_creation_code_hash):
    """Figure out what the address for the conduit would be, given the
    deployment conditions"""
    return to_checksum_address(
        encode_hex(
            Web3.solidity_keccak(
                ["bytes1", "address", "bytes32", "bytes32"],
                [
                    "0xff",
                    controller,
                    conduit_key,
                    conduit_creation_code_hash,
                ],
            )
        )[26:]
    )


@click.command(cls=NetworkBoundCommand)
@network_option()
@click.option("-a", "--account", help="Account to use for deployment")
@click.option(
    "-p",
    "--prefix",
    type=str,
    default="000",
    help="The prefix generate for",
)
@click.option(
    "-o",
    "--owner",
    type=str,
    required=True,
    help="The prefix characters to generate for",
)
@click.option(
    "-r",
    "--runs",
    type=int,
    default=int(1e9),
    help="The max amount of runs to do",
)
def cli(
    network,
    account,
    prefix,
    owner,
    runs,
):
    print(f"Generating for a prefix of {prefix}")

    for i in range(0, runs):
        eacct = Account.create()
        acct = TestAccount(
            index=0, address_str=eacct.address, private_key=eacct.key.hex()
        )

        # Get the address of deployed deployer contract
        contract_address = derive_deploy_address(acct.address, 0)

        # Get the address of the conduit created by deployer contract
        expected_conduit_address = derive_conduit_address(
            CONDUIT_CONTROLLER, contract_address.ljust(66, "0"), CREATION_CODE_HASH
        )

        if expected_conduit_address[2:].startswith(prefix):
            print(f"{i}: {expected_conduit_address} - {eacct.key.hex()}")
