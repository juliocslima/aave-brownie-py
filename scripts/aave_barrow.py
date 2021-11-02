from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from brownie import config, network, interface
from web3 import Web3

"""
1. Swap our ETH for WETH
2. Deposit some ETH into Aave
3. Borrow some asset with the ETH collateral
  3.1. Sell that borrowed asset. (Short selling)
4. Reapy everything back

Testing:
Integration test: Kovan
Unit testes: Mainnet-fork (Mock all of mainnet!)
"""
amount = Web3.toWei(0.1, "ether")


def get_lending_pool():

    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active(
        )]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token ...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    lending_pool = get_lending_pool()
    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing...")
    tx = lending_pool.deposit(erc20_address, amount,
                              account.address, 0, {"from": account})
    tx.wait(1)
    print("deposited!")
