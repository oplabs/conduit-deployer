""" Sweep an accounts entire balance of native currency (ETH/MATIC/etc) to
another. """
import click
from ape import accounts, networks
from ape.cli import network_option, NetworkBoundCommand


@click.command(cls=NetworkBoundCommand)
@network_option()
@click.option("-a", "--account", required=True, help="Account to use for deployment")
@click.option(
    "-d",
    "--dest",
    type=str,
    required=True,
    help="The destination account to sweep native currency",
)
@click.option(
    "-p",
    "--gas-price",
    type=float,
    help="The gas price, in gwei, to use for the transaction",
)
def cli(
    network,
    account,
    dest,
    gas_price,
):
    sender = accounts.load(account)
    gas_price = gas_price * 1e9 if gas_price else networks.network.provider.gas_price

    print(f"Sweeping {round(sender.balance / 1e18, 5)} ETH from {account} to {dest}")
    print(f"Gas Price: {round(gas_price / 1e9, 5)} gwei")

    gas_limit = 21000
    tx_cost = gas_price * gas_limit
    sender.transfer(
        dest, sender.balance - tx_cost, gas_price=gas_price, gas_limit=gas_limit
    )
