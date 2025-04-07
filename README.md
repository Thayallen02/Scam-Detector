
## 📘 Scam Detection Logic Documentation

### Overview
This tool identifies potentially fraudulent cryptocurrency addresses (Bitcoin and Ethereum) by combining public blacklist lookups with blockchain behavior analysis.

---

### 🔍 Address Type Detection

| Address Type | Pattern Used                            | Description                                      |
|--------------|-----------------------------------------|--------------------------------------------------|
| Bitcoin      | `^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$`     | Matches base58-encoded legacy Bitcoin addresses  |
| Ethereum     | `^0x[a-fA-F0-9]{40}$`                   | Matches 42-character hex Ethereum addresses      |

---

### 🪙 Bitcoin Scam Detection

#### 1. Reported Scam Lookup
- The app fetches known scam addresses from:
  [mitchellkrogza/Badd-Boyz-Bitcoin-Scammers](https://github.com/mitchellkrogza/Badd-Boyz-Bitcoin-Scammers)
- The input address is matched against this blacklist.

#### 2. Blockchain Activity Analysis
- **API Used**: `https://blockchain.info/rawaddr/{address}`

| Metric                     | Description                                          |
|----------------------------|------------------------------------------------------|
| Total Inputs               | Number of times the address received BTC            |
| Total Outputs              | Number of times BTC was sent from the address       |
| Large Transactions         | Transactions with outputs > **1 BTC**               |
| High-Recipient Transactions| Transactions with > **10 outputs** (recipients)     |

#### 3. Scam Behavior Criteria
The address is flagged as suspicious if:
```python
large_transactions > 2 or high_recipient_txs > 2
```

---

### 💎 Ethereum Scam Detection

#### 1. Transaction History Retrieval
- **API Used**: `https://api.etherscan.io/api`
- **Endpoint**: `module=account&action=txlist&address={address}`

#### 2. Blockchain Behavior Analysis

| Metric             | Description                                |
|--------------------|--------------------------------------------|
| Total Inward       | Count of ETH received                      |
| Total Outward      | Count of ETH sent                          |
| Large Transactions | Outgoing transfers > **1 ETH**             |

#### 3. Scam Behavior Criteria
The address is flagged as suspicious if:
```python
large_transactions > 2
```

---

### ✅ Result Summary

| Feature                      | Bitcoin                     | Ethereum                  |
|-----------------------------|-----------------------------|---------------------------|
| Reported scam list checked  | ✅ Yes                      | ❌ No                    |
| Blockchain data analyzed    | ✅ Blockchain.info           | ✅ Etherscan             |
| Large transaction threshold | >1 BTC                      | >1 ETH                   |
| High-output detection       | >10 recipients per tx       | ❌ Not applicable        |
| Scam behavior flagging rule | >2 large or high-output txs | >2 large outgoing txs    |
