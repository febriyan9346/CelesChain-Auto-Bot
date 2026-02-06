# CelesChain Auto Bot

**🌐 Register here:** [https://testnet.celeschain.xyz/task?referredBy=XTOP9K](https://testnet.celeschain.xyz/task?referredBy=XTOP9K)

---

## 📌 Overview

CelesChain Auto Bot is an automated task completion tool for the CelesChain Testnet platform. It performs various tasks including check-ins, faucet claims, token swaps, and liquidity provision to earn XP points automatically.

## ✨ Features

- 🔄 **Automated Task Execution**: Complete daily check-ins, faucet claims, token transfers, swaps, and liquidity provision
- 🔁 **Multi-Account Support**: Run multiple accounts simultaneously
- 🌐 **Proxy Support**: Optional proxy configuration for enhanced privacy
- 📊 **Real-time Logging**: Track progress with colored console output
- ⏰ **Auto-Cycle**: Automatic 24-hour cycle after completing all tasks
- 💰 **Smart Transaction Management**: Automatic gas price optimization and nonce handling

## 🛠️ Prerequisites

Before running the bot, ensure you have:

- Python 3.8 or higher
- Active CelesChain testnet account(s)
- Private keys for your wallet(s)
- Testnet CLES tokens (obtained via faucet)

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/febriyan9346/CelesChain-Auto-Bot.git
cd CelesChain-Auto-Bot
```

2. **Install required dependencies**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Create `accounts.txt`

Add your wallet private keys (one per line):

```
0xYOUR_PRIVATE_KEY_1
0xYOUR_PRIVATE_KEY_2
0xYOUR_PRIVATE_KEY_3
```

⚠️ **Security Warning**: Never share your private keys! Keep `accounts.txt` secure and add it to `.gitignore`.

### 2. Create `proxy.txt` (Optional)

If you want to use proxies, add them in the following format (one per line):

```
http://username:password@proxy1.com:8080
http://username:password@proxy2.com:8080
socks5://proxy3.com:1080
```

## 🚀 Usage

Run the bot with:

```bash
python bot.py
```

### Menu Options

When starting the bot, you'll be presented with two options:

1. **Run with proxy** - Uses proxies from `proxy.txt`
2. **Run without proxy** - Direct connection

## 📋 Task Types

The bot automatically handles the following tasks:

| Task Type | Description | Reward |
|-----------|-------------|--------|
| CHECK_IN | Daily check-in | XP Points |
| FAUCET | Claim testnet tokens | XP Points |
| SEND_TOKEN | Transfer tokens | XP Points |
| SWAP | Swap WCLES to cUSDC | XP Points |
| ADD_LIQUIDITY | Add liquidity to pool | XP Points |

## 📊 Features Details

### Automatic Task Processing
- Checks task completion status
- Processes only uncompleted tasks
- Handles transaction verification
- Auto-claims rewards

### Smart Gas Management
- Automatic gas price calculation
- 10% buffer for gas price
- Optimized gas limits per transaction type

### Error Handling
- Insufficient balance detection
- Nonce error management
- Network timeout handling
- Automatic retry mechanism

### Logging System
- Color-coded console output
- Timestamp for each action
- Progress tracking
- Success/Error indicators

## 🔧 Network Configuration

The bot is pre-configured for CelesChain Testnet:

- **RPC URL**: `https://rpc-testnet.celeschain.xyz`
- **Chain ID**: `22225`
- **Explorer**: `https://testnet-explorer.celeschain.xyz`

## 📝 File Structure

```
CelesChain-Auto-Bot/
├── bot.py              # Main bot script
├── accounts.txt        # Your wallet private keys
├── proxy.txt           # Proxy list (optional)
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
└── .gitignore         # Git ignore rules
```

## 🔐 Security Best Practices

1. **Never commit** `accounts.txt` to version control
2. **Keep your private keys** secure and encrypted
3. **Use dedicated wallets** for testnet activities
4. **Enable proxy** if running multiple accounts
5. **Monitor bot activity** regularly

## ⚠️ Disclaimer

This bot is for educational and testing purposes only. Use at your own risk. The developers are not responsible for:

- Loss of funds due to smart contract interactions
- Account bans or restrictions
- Any other consequences of using this automation tool

Always ensure you comply with the terms of service of the platforms you interact with.

## 🐛 Troubleshooting

### Common Issues

**Problem**: `accounts.txt is empty or not found!`
- **Solution**: Create `accounts.txt` file with your private keys

**Problem**: `Insufficient balance`
- **Solution**: Claim tokens from faucet first

**Problem**: `Login failed`
- **Solution**: Check your internet connection and RPC endpoint

**Problem**: `Nonce error`
- **Solution**: Wait a few seconds and let the bot retry

## 🔄 Updates

Stay updated with the latest features and bug fixes:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📞 Support

If you encounter issues or have questions:

- Open an [Issue](https://github.com/febriyan9346/CelesChain-Auto-Bot/issues)
- Check existing issues for solutions
- Contact: [Your Contact Info]

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CelesChain Team for the testnet platform
- Web3.py contributors
- Python community

---

## 💰 Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|----------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

---

**⭐ If you find this bot helpful, please consider giving it a star!**
