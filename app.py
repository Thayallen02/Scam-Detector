import streamlit as st
import requests
import re

# Etherscan API Key
ETHERSCAN_API_KEY = "EVWY88Y9UDYU4JYTBFHRN7WNPVA253YRTA"

def is_ethereum_address(address):
    """Checks if the given address is a valid Ethereum address."""
    return bool(re.match(r"^0x[a-fA-F0-9]{40}$", address))

def is_bitcoin_address(address):
    """Checks if the given address is a valid Bitcoin address."""
    return bool(re.match(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$", address))

def check_bitcoin_scam_activity(address):
    """Fetches Bitcoin transactions and detects scam-related activity."""
    url = f"https://blockchain.info/rawaddr/{address}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        total_inputs = 0
        total_outputs = 0
        large_transactions = 0
        high_recipient_txs = 0

        HIGH_RECIPIENT_THRESHOLD = 10  # More than 10 recipients
        LARGE_TX_THRESHOLD = 1_000_000  # 1 BTC in satoshis

        for tx in data.get("txs", []):
            inputs = len(tx.get("inputs", []))
            outputs = len(tx.get("out", []))

            total_inputs += inputs
            total_outputs += outputs

            if outputs > HIGH_RECIPIENT_THRESHOLD:
                high_recipient_txs += 1

            for output in tx.get("out", []):
                if output.get("value", 0) > LARGE_TX_THRESHOLD:
                    large_transactions += 1

        if total_inputs == 0 and total_outputs == 0:
            st.write(f"🔍 BTC Address {address}: No transactions found.")
            return

        st.write(f"\n🔍 BTC Address: {address}")
        st.write(f"   📥 Total Inward Transfers: {total_inputs}")
        st.write(f"   📤 Total Outward Transfers: {total_outputs}")
        st.write(f"   💰 Large Transactions (>1 BTC): {large_transactions}")
        st.write(f"   🔀 Transactions with Many Recipients (>10): {high_recipient_txs}")

        if high_recipient_txs > 2 or large_transactions > 2:
            st.write("   ⚠️ Potential Scam Detected!")
        else:
            st.write("   ✅ Legitimate Activity Detected.")

    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching data for BTC address {address}: {e}")

def check_ethereum_scam_activity(address):
    """Fetches Ethereum transactions and detects scam-related activity."""
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "1":
            st.write(f"🔍 ETH Address {address}: No transactions found or invalid address.")
            return

        transactions = data.get("result", [])
        total_inward = 0
        total_outward = 0
        large_transactions = 0
        high_recipient_txs = 0

        HIGH_RECIPIENT_THRESHOLD = 10  # More than 10 recipients
        LARGE_TX_THRESHOLD = 1 * 10**18  # 1 ETH in Wei

        for tx in transactions:
            from_address = tx.get("from", "").lower()
            to_address = tx.get("to", "").lower()
            value = int(tx.get("value", 0))

            if to_address == address.lower():
                total_inward += 1
            if from_address == address.lower():
                total_outward += 1

                if value > LARGE_TX_THRESHOLD:
                    large_transactions += 1

        if total_inward == 0 and total_outward == 0:
            st.write(f"🔍 ETH Address {address}: No transactions found.")
            return

        st.write(f"\n🔍 ETH Address: {address}")
        st.write(f"   📥 Total Inward Transfers: {total_inward}")
        st.write(f"   📤 Total Outward Transfers: {total_outward}")
        st.write(f"   💰 Large Transactions (>1 ETH): {large_transactions}")
        st.write(f"   🔀 Transactions with Many Recipients (>10): {high_recipient_txs}")

        if large_transactions > 2 or high_recipient_txs > 2:
            st.write("   ⚠️ Potential Scam Detected!")
        else:
            st.write("   ✅ Legitimate Activity Detected.")

    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching data for ETH address {address}: {e}")

# Streamlit UI
st.title("Cryptocurrency Scam Activity Checker")
user_input = st.text_area("Enter Bitcoin or Ethereum address(es) (one per line):")
addresses = [addr.strip() for addr in user_input.split("\n") if addr.strip()]

if st.button("Check Addresses"):
    for address in addresses:
        if is_bitcoin_address(address):
            check_bitcoin_scam_activity(address)
        elif is_ethereum_address(address):
            check_ethereum_scam_activity(address)
        else:
            st.write(f"❌ Invalid address format: {address}")
