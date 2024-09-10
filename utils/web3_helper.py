from web3 import Web3


def connect_to_bartio_rpc(proxy) -> Web3:
    w3 = Web3(
        provider=Web3.HTTPProvider(
            endpoint_uri='https://bartio.rpc.berachain.com',
            request_kwargs={"proxies": {"http":  proxy,
                                        "https": proxy}}
            )
        )
    
    return w3


def check_BERA_balance(address: str, proxy: str) -> float:
    w3 = connect_to_bartio_rpc("http://"+ proxy)
    checksum_address = w3.to_checksum_address(address)
    balance_wei = w3.eth.get_balance(checksum_address)
    balance = w3.from_wei(balance_wei, 'ether')

    return float(balance)


if __name__=="__main__":
    pass

