#!/usr/bin/env python3
"""
Hub Blockchain - Main Application
File: main.py
Purpose: Entry point cho Hub Blockchain Project
Author: Sinh viên - Trường Đại học Ngân Hàng TP.HCM
Instructor: TS. Nguyễn Hoài Đức
Course: Chuỗi khối trong Kinh doanh (BLB 515)
Dependencies: All modules
"""

import sys
import time
import threading
from typing import Optional

# Import core modules
from core.blockchain import Blockchain
from core.transaction import Transaction
from core.node import Node
from core.consensus import create_consensus

# Import network modules
from network.server import BlockchainHTTPServer
from network.p2p import P2PNetwork

# Import utilities
from utils.tools import BlockchainVisualizer, BlockchainAnalyzer, PerformanceMonitor, FileUtils
from utils.crypto import WalletManager

# Import configuration
from config import get_config, create_sample_config

config = get_config()
wallet_manager = WalletManager()

def interactive_cli(blockchain: Blockchain, p2p_network: P2PNetwork):
    """
    Interactive command-line interface for blockchain
    """
    print("\n🚀 Hub Blockchain Interactive CLI")
    print("===================================")
    print("Commands: mine, transaction, chain, status, wallets, help, exit")

    while True:
        command = input("> ").strip().lower()

        if command == "exit":
            print("Exiting...")
            # TODO: Graceful shutdown
            sys.exit(0)
        
        elif command == "help":
            print_help()

        elif command == "mine":
            miner_wallet = wallet_manager.get_wallet("miner")
            if not miner_wallet:
                miner_wallet = wallet_manager.create_wallet("miner")
            
            new_block = blockchain.mine_block(miner_wallet['address'])
            if new_block:
                print(f"🎉 New block mined: #{new_block.index}")
                p2p_network.broadcast_block(new_block)
                BlockchainVisualizer.print_block(new_block)
            else:
                print("No transactions to mine.")

        elif command == "transaction":
            try:
                sender_name = input("  Sender wallet name: ")
                receiver_name = input("  Receiver wallet name: ")
                amount = float(input("  Amount: "))

                sender_wallet = wallet_manager.get_wallet(sender_name)
                receiver_wallet = wallet_manager.get_wallet(receiver_name)

                if not sender_wallet or not receiver_wallet:
                    print("Sender or receiver wallet not found.")
                    continue

                tx = Transaction(
                    sender=sender_wallet['address'],
                    receiver=receiver_wallet['address'],
                    amount=amount,
                    private_key=sender_wallet['private_key']
                )
                
                if blockchain.add_transaction(tx):
                    print("Transaction added to mempool.")
                    p2p_network.broadcast_transaction(tx)
                else:
                    print("Failed to add transaction.")

            except ValueError:
                print("Invalid amount.")
            except Exception as e:
                print(f"Error creating transaction: {e}")

        elif command == "chain":
            BlockchainVisualizer.print_chain(blockchain)

        elif command == "status":
            BlockchainAnalyzer.print_status(blockchain)

        elif command == "wallets":
            print("Wallets:")
            for name, address in wallet_manager.list_wallets().items():
                print(f"  - {name}: {address}")

        else:
            print(f"Unknown command: '{command}'. Type 'help' for options.")

def print_help():
    """Prints help message for CLI"""
    print("\nHub Blockchain CLI Help")
    print("---------------------")
    print("  mine         - Mine a new block")
    print("  transaction  - Create a new transaction")
    print("  chain        - Display the entire blockchain")
    print("  status       - Show blockchain status")
    print("  wallets      - List all wallets")
    print("  help         - Show this help message")
    print("  exit         - Exit the application")
    print("---------------------\n")

def demo_mode():
    """
    Runs a non-interactive demo of the blockchain
    """
    print("🚀 Running Blockchain Demo Mode...")
    
    # 1. Initialize blockchain
    blockchain = Blockchain()
    print("Blockchain initialized.")
    
    # 2. Create wallets
    wallet_manager.create_wallet("miner")
    wallet_manager.create_wallet("alice")
    wallet_manager.create_wallet("bob")
    
    print("\nWallets created:")
    for name, info in wallet_manager.list_wallets().items():
        print(f"  - {name}: {info}")
    
    # 3. Create transactions
    print("\nCreating transactions...")
    alice_wallet = wallet_manager.get_wallet("alice")
    bob_wallet = wallet_manager.get_wallet("bob")
    
    tx1 = Transaction(alice_wallet['address'], bob_wallet['address'], 10, alice_wallet['private_key'])
    tx2 = Transaction(bob_wallet['address'], alice_wallet['address'], 5, bob_wallet['private_key'])
    
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    print("2 transactions added to mempool.")
    
    # 4. Mine a block
    print("\nMining a block...")
    miner_wallet = wallet_manager.get_wallet("miner")
    blockchain.mine_block(miner_wallet['address'])
    
    # 5. Visualize the chain
    BlockchainVisualizer.print_chain(blockchain)
    
    # 6. Check status
    BlockchainAnalyzer.print_status(blockchain)
    print("\n✅ Demo finished.")

def mining_mode():
    """Continuous mining mode"""
    # TODO: Implement continuous mining loop
    print("Mining mode not yet implemented.")

def main():
    """
    Main entry point for the application
    """
    if "--demo" in sys.argv:
        demo_mode()
        return
        
    if "--mine" in sys.argv:
        mining_mode()
        return

    if "--create-config" in sys.argv:
        create_sample_config()
        return

    # Initialize components
    blockchain = Blockchain()
    
    # Load data
    try:
        chain_data = FileUtils.load_json(config.get_blockchain_file_path())
        if chain_data:
            blockchain.chain = [blockchain.block_from_dict(b) for b in chain_data]
        
        wallet_data = FileUtils.load_json(config.get_wallet_file_path())
        if wallet_data:
            wallet_manager.wallets = wallet_data
            
    except Exception as e:
        print(f"Could not load data: {e}. Starting with a fresh blockchain.")

    # P2P Network
    p2p_network = P2PNetwork(blockchain)
    p2p_thread = threading.Thread(target=p2p_network.start)
    p2p_thread.daemon = True
    p2p_thread.start()

    # HTTP Server
    http_server = BlockchainHTTPServer(
        (config.network.http_host, config.network.http_port),
        blockchain,
        p2p_network
    )
    http_thread = threading.Thread(target=http_server.serve_forever)
    http_thread.daemon = True
    http_thread.start()
    
    print(f"HTTP server running on http://{config.network.http_host}:{config.network.http_port}")

    # Start interactive CLI
    try:
        interactive_cli(blockchain, p2p_network)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if config.storage.auto_save:
            FileUtils.save_json(config.get_blockchain_file_path(), [b.to_dict() for b in blockchain.chain])
            FileUtils.save_json(config.get_wallet_file_path(), wallet_manager.wallets)
        
        http_server.shutdown()
        # p2p_network.stop() # TODO: Implement graceful shutdown
        print("Shutdown complete.")

if __name__ == "__main__":
    main() 