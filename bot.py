import requests
import time
import sys
import uuid
import random
from eth_account import Account
from web3 import Web3
from colorama import Fore, Style, init
from datetime import datetime
import pytz
import os

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

RPC_URL = "https://rpc-testnet.celeschain.xyz"
CHAIN_ID = 22225
EXPLORER_URL = "https://testnet-explorer.celeschain.xyz"

ROUTER_ADDRESS = Web3.to_checksum_address("0xb87314F0850839AB3B0DB394b5014F134a2C037d")
SEND_TO_ADDRESS = Web3.to_checksum_address("0x2bf1bbfa2bbc07e47290385936ab27a0c697fb5b")
WCLES_ADDRESS = Web3.to_checksum_address("0xcfc4fa68042509a239fa33f7a559860c875dca70")
CUSDC_ADDRESS = Web3.to_checksum_address("0x1BAb49aA82197ee8B5131A09CfE2fE0BF1603103")

ERC20_ABI = [{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"}]
ROUTER_ABI = [{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"}]

class CelesBot:
    def __init__(self):
        self.use_proxy = False
    
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}CELESCHAIN AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self):
        delay = random.randint(2, 5)
        time.sleep(delay)
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    
    def load_file(self, f):
        try:
            return [l.strip() for l in open(f, 'r') if l.strip()]
        except:
            return []
    
    def get_web3(self):
        return Web3(Web3.HTTPProvider(RPC_URL))
    
    def api_request(self, method, endpoint, payload=None, params=None, proxy=None):
        url = f"https://testnet.celeschain.xyz/api/{endpoint}"
        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://testnet.celeschain.xyz",
            "referer": "https://testnet.celeschain.xyz/task",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        }
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            if method == "GET":
                return requests.get(url, headers=headers, params=params, proxies=proxies, timeout=15).json()
            return requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=15).json()
        except:
            return {}
    
    def approve_token(self, w3, pk, address, token, spender, amount):
        try:
            ctr = w3.eth.contract(address=token, abi=ERC20_ABI)
            if ctr.functions.allowance(address, spender).call() >= amount:
                return True
            
            tx = ctr.functions.approve(spender, 2**256-1).build_transaction({
                'from': address,
                'nonce': w3.eth.get_transaction_count(address),
                'gas': 100000,
                'gasPrice': int(w3.eth.gas_price*1.1),
                'chainId': CHAIN_ID
            })
            signed = w3.eth.account.sign_transaction(tx, pk)
            w3.eth.send_raw_transaction(signed.rawTransaction)
            time.sleep(5)
            return True
        except:
            return False
    
    def do_send_token(self, w3, pk, address):
        tx = {
            'to': SEND_TO_ADDRESS,
            'value': w3.to_wei(0.00001, 'ether'),
            'gas': 25000,
            'gasPrice': int(w3.eth.gas_price*1.1),
            'nonce': w3.eth.get_transaction_count(address),
            'chainId': CHAIN_ID
        }
        signed = w3.eth.account.sign_transaction(tx, pk)
        return w3.eth.send_raw_transaction(signed.rawTransaction)
    
    def do_swap(self, w3, pk, address):
        ctr = w3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)
        tx = ctr.functions.swapExactETHForTokens(
            0,
            [WCLES_ADDRESS, CUSDC_ADDRESS],
            address,
            int(time.time())+1200
        ).build_transaction({
            'from': address,
            'value': w3.to_wei(0.00001, 'ether'),
            'gas': 300000,
            'gasPrice': int(w3.eth.gas_price*1.1),
            'nonce': w3.eth.get_transaction_count(address),
            'chainId': CHAIN_ID
        })
        signed = w3.eth.account.sign_transaction(tx, pk)
        return w3.eth.send_raw_transaction(signed.rawTransaction)
    
    def do_add_liq(self, w3, pk, address):
        if not self.approve_token(w3, pk, address, CUSDC_ADDRESS, ROUTER_ADDRESS, 1000):
            return None
        ctr = w3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)
        tx = ctr.functions.addLiquidityETH(
            CUSDC_ADDRESS,
            1000,
            0,
            0,
            address,
            int(time.time())+1200
        ).build_transaction({
            'from': address,
            'value': w3.to_wei(0.00001, 'ether'),
            'gas': 350000,
            'gasPrice': int(w3.eth.gas_price*1.1),
            'nonce': w3.eth.get_transaction_count(address),
            'chainId': CHAIN_ID
        })
        signed = w3.eth.account.sign_transaction(tx, pk)
        return w3.eth.send_raw_transaction(signed.rawTransaction)
    
    def process_task(self, task, user_id, pk, address, proxy, w3):
        t_id = task["_id"]
        t_type = task["taskType"]
        t_title = task["title"]
        task_status = task.get("status", "UNKNOWN")
        
        if task_status == "COMPLETED":
            self.log(f"{t_title}: Claimed", "WARNING")
            return
        
        self.log(f"Processing Task: {t_title}", "INFO")
        
        tx_hash = None
        my_addr_checksum = w3.to_checksum_address(address)

        try:
            if t_type == "CHECK_IN":
                progress = self.api_request("POST", "tasks/progress-checkin", {"taskId": t_id, "userId": user_id}, proxy=proxy)
                if progress.get("code") == "success":
                    tx_hash = "checkin_done"
                
            elif t_type == "FAUCET":
                self.api_request("POST", "faucet", {"account": address, "deviceID": str(uuid.uuid4())}, proxy=proxy)
                tx_hash = "faucet_done"
                
            elif t_type == "SEND_TOKEN":
                tx_hash = self.do_send_token(w3, pk, my_addr_checksum)
                
            elif t_type == "SWAP":
                tx_hash = self.do_swap(w3, pk, my_addr_checksum)
                
            elif "LIQUIDITY" in t_type:
                tx_hash = self.do_add_liq(w3, pk, my_addr_checksum)
                
            else:
                tx_hash = "social_done"
        
        except Exception as e:
            error_detail = str(e)
            if "insufficient funds" in error_detail.lower():
                self.log(f"{t_title}: Insufficient balance", "ERROR")
            elif "nonce" in error_detail.lower():
                self.log(f"{t_title}: Nonce error", "ERROR")
            else:
                self.log(f"{t_title}: Failed - {error_detail[:50]}", "ERROR")
            return

        if tx_hash:
            if tx_hash not in ["social_done", "checkin_done", "faucet_done"]:
                self.log(f"TX Hash: {w3.to_hex(tx_hash)[:16]}...", "INFO")
                time.sleep(5)
                verif = self.api_request("POST", "tasks/progress-onchain", {"userId": user_id, "taskId": t_id, "amount": 1}, proxy=proxy)
                if verif.get("code") != "success":
                    self.log(f"{t_title}: Verification failed", "ERROR")
                    return

            time.sleep(1)
            claim = self.api_request("POST", "tasks/claim", {"userId": user_id, "taskId": t_id}, proxy=proxy)
            
            claim_code = claim.get("code", "")
            claim_msg = claim.get("message", "")
            
            if claim_code == "success":
                reward = claim.get('data', {}).get('rewardXP', 0)
                self.log(f"Claim Success! Reward: +{reward} XP", "SUCCESS")
            elif claim_code == "error":
                if "already" in claim_msg.lower() or "claimed" in claim_msg.lower() or "completed" in claim_msg.lower():
                    self.log(f"{t_title}: Claimed", "WARNING")
                elif "Claim Error" in claim_msg:
                    self.log(f"{t_title}: Claimed", "WARNING")
                else:
                    self.log(f"{t_title}: {claim_msg}", "ERROR")
            else:
                self.log(f"{t_title}: Unknown response - {claim}", "ERROR")
    
    def run(self):
        self.print_banner()
        
        choice = self.show_menu()
        
        if choice == '1':
            self.log("Running with proxy", "INFO")
            self.use_proxy = True
        else:
            self.log("Running without proxy", "INFO")
            self.use_proxy = False
        
        accounts = self.load_file("accounts.txt")
        proxies = self.load_file("proxy.txt")
        
        if not accounts:
            self.log("accounts.txt is empty or not found!", "ERROR")
            return
        
        self.log(f"Loaded {len(accounts)} accounts successfully", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        TASK_ORDER = ["CHECK_IN", "FAUCET", "SEND_TOKEN", "SWAP", "ADD_LIQUIDITY"]
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            total_accounts = len(accounts)
            
            for i, pk in enumerate(accounts):
                if not pk.startswith("0x"):
                    pk = "0x" + pk
                try:
                    acc = Account.from_key(pk)
                    addr = acc.address
                except:
                    self.log(f"Invalid private key: {pk[:10]}...", "ERROR")
                    continue
                
                self.log(f"Account #{i+1}/{total_accounts}", "INFO")
                
                px = None
                if self.use_proxy and proxies:
                    px = proxies[i % len(proxies)]
                    self.log(f"Proxy: {px[:30]}...", "INFO")
                else:
                    self.log(f"Proxy: No Proxy", "INFO")
                
                self.log(f"{addr[:6]}...{addr[-4:]}", "INFO")
                
                self.random_delay()
                
                u = self.api_request("GET", "users/get-user-by-address", params={"userAddress": addr.lower()}, proxy=px)
                if not u.get("data"):
                    self.log("Login failed", "ERROR")
                    continue
                    
                uid = u["data"]["_id"]
                xp = u['data'].get('XpPoints', 0)
                self.log(f"Login successful!", "SUCCESS")
                self.log(f"Total Points: {xp}", "SUCCESS")

                tasks = self.api_request("GET", "tasks/get-user-tasks", params={"userAddress": uid}, proxy=px).get("data", {}).get("tasks", [])
                
                w3 = self.get_web3()
                
                for task_type in TASK_ORDER:
                    matching_tasks = [t for t in tasks if t["taskType"] == task_type]
                    for task in matching_tasks:
                        self.process_task(task, uid, pk, addr, px, w3)
                        self.random_delay()
                
                success_count += 1
                
                if i < total_accounts - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            
            wait_time = 86400
            self.countdown(wait_time)

if __name__ == "__main__":
    bot = CelesBot()
    bot.run()
