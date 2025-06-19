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
    print("\n🚀 Hub Blockchain Interactive CLI (Giao diện dòng lệnh tương tác)")
    print("===================================================================")
    print("Commands (Lệnh): mine, transaction, chain, status, wallets, help, exit")

    while True:
        command = input("> ").strip().lower()

        if command == "exit":
            print("Exiting... / Đang thoát...")
            # TODO: Graceful shutdown
            sys.exit(0)
        
        elif command == "help":
            print_help()

        elif command == "mine":
            miner_wallet = wallet_manager.get_wallet("miner")
            if not miner_wallet:
                print("Creating miner wallet... / Đang tạo ví cho thợ đào...")
                miner_wallet = wallet_manager.create_wallet("miner")
            
            print("Mining a new block... / Đang đào khối mới...")
            new_block = blockchain.mine_pending_transactions(miner_wallet['address'])
            if new_block:
                print(f"🎉 New block mined: #{new_block.index} / Đã đào xong khối mới: #{new_block.index}")
                p2p_network.broadcast_block(new_block)
                BlockchainVisualizer.print_block(new_block)
            else:
                print("No transactions to mine. / Không có giao dịch để đào.")

        elif command == "transaction":
            try:
                sender_name = input("  Sender wallet name / Tên ví người gửi: ")
                receiver_name = input("  Receiver wallet name / Tên ví người nhận: ")
                amount = float(input("  Amount / Số lượng: "))

                sender_wallet = wallet_manager.get_wallet(sender_name)
                receiver_wallet = wallet_manager.get_wallet(receiver_name)

                if not sender_wallet or not receiver_wallet:
                    print("Sender or receiver wallet not found. / Không tìm thấy ví người gửi hoặc người nhận.")
                    continue

                tx = Transaction(
                    sender=sender_wallet['address'],
                    receiver=receiver_wallet['address'],
                    amount=amount,
                    private_key=sender_wallet['private_key']
                )
                
                if blockchain.add_transaction(tx):
                    print("Transaction added to mempool. / Đã thêm giao dịch vào vùng chờ.")
                    p2p_network.broadcast_transaction(tx)
                else:
                    print("Failed to add transaction. / Thêm giao dịch thất bại.")

            except ValueError:
                print("Invalid amount. / Số lượng không hợp lệ.")
            except Exception as e:
                print(f"Error creating transaction: {e} / Lỗi khi tạo giao dịch: {e}")

        elif command == "chain":
            BlockchainVisualizer.print_chain(blockchain)

        elif command == "status":
            BlockchainAnalyzer.print_status(blockchain)

        elif command == "wallets":
            print("Wallets / Các ví:")
            for name, address in wallet_manager.list_wallets().items():
                print(f"  - {name}: {address}")

        else:
            print(f"Unknown command: '{command}'. Type 'help' for options. / Lệnh không xác định: '{command}'. Gõ 'help' để xem các tùy chọn.")

def print_help():
    """Prints help message for CLI"""
    print("\nHub Blockchain CLI Help / Trợ giúp")
    print("---------------------------------")
    print("  mine         - Mine a new block / Đào một khối mới")
    print("  transaction  - Create a new transaction / Tạo giao dịch mới")
    print("  chain        - Display the entire blockchain / Hiển thị toàn bộ chuỗi khối")
    print("  status       - Show blockchain status / Hiển thị trạng thái chuỗi khối")
    print("  wallets      - List all wallets / Liệt kê các ví")
    print("  help         - Show this help message / Hiển thị thông báo này")
    print("  exit         - Exit the application / Thoát ứng dụng")
    print("---------------------------------\n")

def demo_mode():
    """
    Runs a non-interactive demo of the blockchain
    """
    print("🚀 Running Blockchain Demo Mode... / Chạy chế độ demo...")
    
    # 1. Initialize blockchain
    blockchain = Blockchain()
    print("Blockchain initialized. / Đã khởi tạo chuỗi khối.")
    
    # 2. Create wallets
    wallet_manager.create_wallet("miner")
    wallet_manager.create_wallet("alice")
    wallet_manager.create_wallet("bob")
    
    print("\nWallets created: / Các ví đã tạo:")
    for name, info in wallet_manager.list_wallets().items():
        print(f"  - {name}: {info}")
    
    # 3. Create transactions
    print("\nCreating transactions... / Đang tạo giao dịch...")
    alice_wallet = wallet_manager.get_wallet("alice")
    bob_wallet = wallet_manager.get_wallet("bob")
    
    tx1 = Transaction(alice_wallet['address'], bob_wallet['address'], 10, alice_wallet['private_key'])
    tx2 = Transaction(bob_wallet['address'], alice_wallet['address'], 5, bob_wallet['private_key'])
    
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    print("2 transactions added to mempool. / 2 giao dịch đã được thêm vào vùng chờ.")
    
    # 4. Mine a block
    print("\nMining a block... / Đang đào khối...")
    miner_wallet = wallet_manager.get_wallet("miner")
    blockchain.mine_pending_transactions(miner_wallet['address'])
    
    # 5. Visualize the chain
    BlockchainVisualizer.print_chain(blockchain)
    
    # 6. Check status
    BlockchainAnalyzer.print_status(blockchain)
    print("\n✅ Demo finished. / Hoàn thành demo.")

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
        chain_data = FileUtils.load_json(config.storage.blockchain_file)
        if chain_data:
            blockchain.chain = [Blockchain.block_from_dict(b) for b in chain_data]
        
        wallet_data = FileUtils.load_json(config.storage.wallets_file)
        if wallet_data:
            wallet_manager.wallets = wallet_data
            
    except Exception as e:
        print(f"Could not load data: {e}. Starting with a fresh blockchain. / Không thể tải dữ liệu. Bắt đầu với chuỗi khối mới.")

    # P2P Network
    p2p_network = P2PNetwork(blockchain, host=config.network.p2p_host, port=config.network.p2p_port)
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
        print("\nShutting down... / Đang tắt...")
    finally:
        if config.storage.auto_save:
            FileUtils.save_json(config.storage.blockchain_file, [b.to_dict() for b in blockchain.chain])
            FileUtils.save_json(config.storage.wallets_file, wallet_manager.wallets)
        
        http_server.shutdown()
        p2p_network.stop()
        print("Shutdown complete. / Tắt hoàn tất.")

if __name__ == "__main__":
    main() 