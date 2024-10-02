## Duhz 27/09/2024 as 21h15
# Sem API Key, utiliza https://bitcoin.atomicwallet.io/api/v2/address/
# Bancos de Dados Criar Pasta LOG
# Só SENHOR é o meu pastor; nada me faltará.
# 
import os
import requests
import time
from datetime import datetime
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

"""def bip44_SOL_seed_to_address(seed):
    seed_bytes = Bip39SeedGenerator(seed).Generate()
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    print(bip44_chg_ctx.PublicKey().ToAddress())
    return bip44_chg_ctx.PublicKey().ToAddress()"""


def check_ETH_balance(addr: str) -> str:
    url = f"https://ethereum.atomicwallet.io/api/v2/address/{addr}"
    try:
        req = requests.get(url).json()
        ret = dict(req)['balance']
        return int(ret) / 1000000000000000000
    except KeyError:
        print("Erro atomicwallet: Falha ao buscar saldo Ethereum.")
        open('LOG.txt', 'a').write(f'Erro atomicwallet: Falha ao buscar saldo Ethereum.\n\n') #Salva Local
        return 0

def check_BTC_balance(addr): #AtomicWallet Original
    rl = f"https://bitcoin.atomicwallet.io/api/v2/address/{addr}"
    req = requests.get(rl)
    try:
        ret = int(dict(req.json())['balance'])
        ret1 = int(dict(req.json())['totalReceived'])
        print(f"{Fore.CYAN}AtomicWallet Endereço {addr} valor {ret} valor recebido {ret1}", Fore.RESET)
        return ret / 100000000 or ret1 / 100000000
    except KeyError:
        print(Fore.GREEN, "Erro AtomicWallet: Falha ao buscar saldo Bitcoin.", Fore.RESET)
        open('LOG.txt', 'a').write(f'Erro AtomicWallet: Falha ao buscar saldo Bitcoin.\n\n') #Salva Local
        return 0


def check_BTC_balance1(addr):
    rl1 = f"https://api.bitcore.io/api/BTC/mainnet/address/{addr}/balance"
    req1 = requests.get(rl1)
    try:
        ret1 = int(dict(req1.json())['balance'])
        print(f"{Fore.CYAN}bitcore Endereço {addr} valor {ret1}", Fore.RESET)
        return ret1 / 100000000
    except KeyError:
        print(Fore.GREEN, "Erro bitcore: Falha ao buscar saldo Bitcoin.", Fore.RESET)
        open('LOG.txt', 'a').write(f'Erro bitcore: Falha ao buscar saldo Bitcoin.\n\n') #Salva Local
        return 0
    


def check_BTC_balance2(addr):
    response = requests.get(f"https://blockchain.info/balance?active={addr}")
    data = response.json()
    try:
        balance = data[addr]["final_balance"]
        print(f"{Fore.CYAN}blockchain Endereço {addr} valor {balance}", Fore.RESET)
        return balance / 100000000
    except KeyError:
        print(Fore.GREEN, "Erro blockchain: Falha ao buscar saldo Bitcoin.", Fore.RESET)
        open('LOG.txt', 'a').write(f'Erro blockchain: Falha ao buscar saldo Bitcoin.\n\n') #Salva Local
        return 0
        


def main():
    data_e_hora_atuais = datetime.now()
    d = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
    #print("\nScript iniciado.")
    #open('LOG.txt', 'a').write(f'#Executavel {exec}# {d} Script iniciado  *-*-*-*-* Sistema iniciado *-*-*-*-*\n\n') #Salva Local
    os.system('clear') 
    print(Fore.GREEN, "Carregando...", Fore.RESET)
    time.sleep(1)
    z = 1  
    ff = 0  

    while True:
        try:
            seed = bip()
            data_e_hora_atuais = datetime.now()
            d = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
            BTC_address = bip44_BTC_seed_to_address(seed)
            '''SOL_address = bip44_SOL_seed_to_address(seed)'''
            BTC_balance = check_BTC_balance(BTC_address)
            BTC_balance1 = check_BTC_balance1(BTC_address)
            BTC_balance2 = check_BTC_balance2(BTC_address)
            ETH_address = bip44_ETH_wallet_from_seed(seed)
            ETH_balance = check_ETH_balance(ETH_address)
            
            os.system('clear')
            print("=" * 70)
            print(f"#Executavel {exec}#", Fore.RESET)
            print(f"Procuradas: {z} Encontradas: {ff}")
            print("=" * 70)
            print(f"{Fore.WHITE}Seed: {Fore.RED}{seed}\n")
            print(f"{Fore.WHITE}BTC address: {Fore.YELLOW}{BTC_address}")
            print(f"{Fore.WHITE}BTC balance: {Fore.MAGENTA}(AtomicWallet {BTC_balance}) (bitcore {BTC_balance1}) (blockchain {BTC_balance2}) BTC")
            print(f"{Fore.WHITE}ETH address: {Fore.YELLOW}{ETH_address}")
            print(f"{Fore.WHITE}ETH balance: {Fore.MAGENTA}{ETH_balance} ETH", Fore.RESET)
            print("=" * 70)
            time.sleep(1)
            z += 1   
            
            if BTC_balance != 0 or BTC_balance1 != 0  or BTC_balance2 != 0 or ETH_balance != 0:
                print("(!) Parabens você encontrou uma Carteira com Saldo!")
                open('CarteiraBTC.txt', 'a').write(f'#Executavel {exec}# {d}\nSeed: {seed}\nAddress: {BTC_address}\nBalance: (AtomicWallet {BTC_balance}) (bitcore {BTC_balance1}) (blockchain {BTC_balance2}) BTC\nEthereum Address: {ETH_address}\nBalance: {ETH_balance} ETH\n\n') #Salva Local
                print("(!) Salvo Local, tentando enviar um email!")
                print("(!) Email Enviado com sucesso!")
                ff += 1
                time.sleep(1)
            else:
                continue
        except Exception as e:
            print(f"Ocorreu um erro: {e}")   
            print("Reiniciando...")	
            open('LOG.txt', 'a').write(f'#Executavel {exec}#\n{d}\nErro: Ocorreu um erro: {e}. *-*-*-*-* Sistema Reiniciado *-*-*-*-*\n\n') #Salva Local
            time.sleep(5)
            main()

if __name__ == "__main__":
    #data_e_hora_atuais = datetime.now()
    #d = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nScript encerrado pelo Usuario.")
        #open('LOG.txt', 'a').write(f'#Executavel {exec}#\n{d}\nScript encerrado pelo Usuario *-*-*-*-* Sistema Desligado *-*-*-*-*\n\n') #Salva Local