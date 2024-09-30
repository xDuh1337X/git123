## Duhz 27/09/2024 as 21h15
# Sem API Key, utiliza https://bitcoin.atomicwallet.io/api/v2/address/
# Bancos de Dados Criar Pasta LOG
# Só SENHOR é o meu pastor; nada me faltará.
# 
import os
import requests
import time
from colorama import Fore  
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    Bip39WordsNum,
)
#https://etherscan.io/

#-*-*-*-*-*-*-*-*-*
exec = 2
#-*-*-*-*-*-*-*-*-*

def bip():
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)

def bip44_ETH_wallet_from_seed(seed):
    seed_bytes = Bip39SeedGenerator(seed).Generate()
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    bip44_acc_ctx = (
        bip44_mst_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )
    eth_address = bip44_acc_ctx.PublicKey().ToAddress()
    return eth_address

def bip44_BTC_seed_to_address(seed):
    seed_bytes = Bip39SeedGenerator(seed).Generate()
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)
    return bip44_addr_ctx.PublicKey().ToAddress()

def check_ETH_balance(addr: str) -> str:
    url = f"https://ethereum.atomicwallet.io/api/v2/address/{addr}"
    try:
        req = requests.get(url).json()
        ret = dict(req)['balance']
        return int(ret) / 1000000000000000000
    except KeyError:
        print("Erro: Falha ao buscar saldo Ethereum.")
        return 0

def check_BTC_balance(addr):
    rl = f"https://bitcoin.atomicwallet.io/api/v2/address/{addr}"
    try:
        req = requests.get(rl).json()
        ret = dict(req)['balance']
        return int(ret) / 100000000
    except KeyError:
        print("Erro: Falha ao buscar saldo Bitcoin.")
        return 0


def main():
    os.system('clear') 
    print(Fore.GREEN, "Carregando...", Fore.RESET)
    time.sleep(1)
    z = 1  
    ff = 0  

    while True:
        try:
            seed = bip()
            BTC_address = bip44_BTC_seed_to_address(seed)
            BTC_balance = check_BTC_balance(BTC_address)
            ETH_address = bip44_ETH_wallet_from_seed(seed)
            ETH_balance = check_ETH_balance(ETH_address)
            
            os.system('clear')
            print("=" * 70)
            print(f"#Executavel {exec}#", Fore.RESET)
            print(f"Procuradas: {z} Encontradas: {ff}")
            print("=" * 70)
            print(f"{Fore.WHITE}Seed: {Fore.RED}{seed}\n{Fore.WHITE}BTC address: {Fore.YELLOW}{BTC_address}\n{Fore.WHITE}BTC balance: {Fore.MAGENTA}{BTC_balance} BTC\n{Fore.WHITE}ETH address: {Fore.YELLOW}{ETH_address}\n{Fore.WHITE}ETH balance: {Fore.MAGENTA}{ETH_balance} ETH", Fore.RESET)
            print("=" * 70)
            #time.sleep(0.5)
            z += 1   
            
            if BTC_balance != 0 or ETH_balance != 0:
                print("(!) Parabens você encontrou uma Carteira com Saldo!")
                open('CarteiraBTC.txt', 'a').write(f'Seed: {seed}\nAddress: {BTC_address}\nBalance: {BTC_balance} BTC\nEthereum Address: {ETH_address}\nBalance: {ETH_balance} ETH\n\n') #Salva Local
                print("(!) Salvo Local, tentando enviar um email!")
                print("(!) Email Enviado com sucesso!")
                ff += 1
                time.sleep(0.10)
            else:
                continue
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print("Reiniciando...")
            time.sleep(5)
            main()

if __name__ == "__main__":
    main()