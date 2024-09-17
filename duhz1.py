from colorama import Fore, init  
from hdwallet import HDWallet  
from hdwallet.symbols import BTC, ETH
import random  
import requests  
import os  
import time  

init(autoreset=True)

def eth_balance(addr: str) -> str:
    url = f"https://ethereum.atomicwallet.io/api/v2/address/19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt"
    try:
        req = requests.get(url).json()
        ret = dict(req)['balance']
        return int(ret) / 1000000000000000000
    except KeyError:
        print("Erro: Falha ao buscar saldo Ethereum.")
        return 0

def get_balance(addr):
    rl = f"https://bitcoin.atomicwallet.io/api/v2/address/19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt"
    try:
        req = requests.get(rl).json()
        ret = dict(req)['balance']
        return int(ret) / 10000000000
    except KeyError:
        print("Erro: Falha ao buscar saldo Bitcoin.")
        return 0


def main():
    os.system('clear') 
    print(Fore.GREEN, "Carregando...", Fore.RESET)  
    time.sleep(2)  

    z = 1  
    ff = 0  
    while True:
        try:
            private_key = "".join(random.choice("0123456789abcdef") for _ in range(64))
            hd_btc: HDWallet = HDWallet(BTC)
            hd_eth: HDWallet = HDWallet(ETH)
            hd_btc.from_private_key(private_key)
            hd_eth.from_private_key(private_key)

            eth_addr = hd_eth.p2pkh_address()
            btc_addr1 = hd_btc.p2pkh_address()
            btc_addr2 = hd_btc.p2wpkh_address()
            btc_addr3 = hd_btc.p2wpkh_in_p2sh_address()
            btc_addr4 = hd_btc.p2wsh_in_p2sh_address()
            btc_addr5 = hd_btc.p2sh_address()

            value5 = get_balance(btc_addr5)
            value4 = get_balance(btc_addr4)
            value3 = get_balance(btc_addr3)
            value2 = get_balance(btc_addr2)
            value1 = get_balance(btc_addr1)
            val_et = eth_balance(eth_addr)

            os.system('clear')

            print(Fore.YELLOW, "#Executavel 1#", Fore.RESET)
            print(f"Procuradas: {z} Encontradas: {ff}")

            print(f"{Fore.WHITE}BTC Address (P2PKH)  | BAL: {Fore.MAGENTA}{value1} | {Fore.YELLOW}{btc_addr1}")
            print(f"{Fore.WHITE}BTC Address (BECH32) | BAL: {Fore.MAGENTA}{value2} | {Fore.YELLOW}{btc_addr2}")
            print(f"{Fore.WHITE}BTC Address (P2WPKH) | BAL: {Fore.MAGENTA}{value3} | {Fore.YELLOW}{btc_addr3}")
            print(f"{Fore.WHITE}BTC Address (P2WSH)  | BAL: {Fore.MAGENTA}{value4} | {Fore.YELLOW}{btc_addr4}")
            print(f"{Fore.WHITE}BTC Address (P2SH)   | BAL: {Fore.MAGENTA}{value5} | {Fore.YELLOW}{btc_addr5}")
            print(f"{Fore.WHITE}ETH Address (ETH)    | BAL: {Fore.MAGENTA}{val_et} | {Fore.YELLOW}{eth_addr}")
            print(f"{Fore.WHITE}Private Key (HEX)    | {Fore.MAGENTA}{private_key}")
            print("=" * 70)

            z += 1  

            if value1 > 0:
                ff += 1
                open('P2PKH btcWin1.txt', 'a').write(f'{btc_addr1}\n{private_key}\n')
            if value2 > 0:
                ff += 1
                open('BECH32 btcWin1.txt', 'a').write(f'{btc_addr2}\n{private_key}\n')
            if value3 > 0:
                ff += 1
                open('P2WPKH btcWin1.txt', 'a').write(f'{btc_addr3}\n{private_key}\n')
            if value4 > 0:
                ff += 1
                open('P2WSH btcWin1.txt', 'a').write(f'{btc_addr4}\n{private_key}\n')
            if value5 > 0:
                ff += 1
                open('P2SH btcWin1.txt', 'a').write(f'{btc_addr5}\n{private_key}\n')
            if val_et > 0:
                ff += 1
                open('ETH btcWin1.txt', 'a').write(f'{eth_addr}\n{private_key}\n')
            else:
                continue
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print("Reiniciando...")
            time.sleep(5)
            main()

if __name__ == "__main__":
    main()
