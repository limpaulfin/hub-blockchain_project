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
import argparse
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

def main():
    """
    Main entry point for the application
    """
    parser = argparse.ArgumentParser(
        description="Hub Blockchain - A simple blockchain implementation.",
        epilog="""
    Ví dụ / Examples:
      python3 main.py mine --wallet my_miner
      python3 main.py transaction alice bob 10.5
      python3 main.py chain
      python3 main.py server
    """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Các lệnh có sẵn / Available commands')
    subparsers.required = True

    # --- Command: demo ---
    parser_demo = subparsers.add_parser('demo', help='Chạy demo blockchain không tương tác.')
    
    # --- Command: mine ---
    parser_mine = subparsers.add_parser('mine', help='Đào khối mới cho các giao dịch đang chờ.')
    parser_mine.add_argument('--wallet', default='miner', help='Chỉ định ví nhận thưởng (mặc định: miner).')

    # --- Command: transaction ---
    parser_tx = subparsers.add_parser('transaction', help='Tạo và phát đi một giao dịch mới.')
    parser_tx.add_argument('sender', metavar='SENDER_WALLET', help='Tên ví người gửi.')
    parser_tx.add_argument('receiver', metavar='RECEIVER_WALLET', help='Tên ví người nhận.')
    parser_tx.add_argument('amount', metavar='AMOUNT', type=float, help='Số lượng giao dịch.')

    # --- Command: chain ---
    parser_chain = subparsers.add_parser('chain', help='Hiển thị toàn bộ chuỗi khối.')

    # --- Command: status ---
    parser_status = subparsers.add_parser('status', help='Hiển thị trạng thái của chuỗi khối.')

    # --- Command: wallets ---
    parser_wallets = subparsers.add_parser('wallets', help='Liệt kê tất cả các ví đã tạo.')
    
    # --- Command: create-wallet ---
    parser_create_wallet = subparsers.add_parser('create-wallet', help='Tạo một ví mới.')
    parser_create_wallet.add_argument('name', metavar='WALLET_NAME', help='Tên của ví mới.')

    # --- Command: server ---
    parser_server = subparsers.add_parser('server', help='Chạy node như một máy chủ (P2P và HTTP).')
    
    # --- Command: create-config ---
    parser_create_config = subparsers.add_parser('create-config', help='Tạo file config.py mẫu.')

    args = parser.parse_args()

    if args.command == 'create-config':
        create_sample_config()
        return

    if args.command == 'demo':
        demo_mode()
        return

    # Initialize components
    blockchain = Blockchain()
    
    # Load data from files
    try:
        chain_data = FileUtils.load_json(config.storage.blockchain_file)
        if chain_data and 'chain' in chain_data:
            blockchain.chain = [Blockchain.block_from_dict(b) for b in chain_data['chain']]
            blockchain.pending_transactions = [Transaction.from_dict(tx) for tx in chain_data.get('pending_transactions', [])]
            print("Blockchain data loaded from file. / Đã tải dữ liệu chuỗi khối từ file.")
        
        wallet_data = FileUtils.load_json(config.storage.wallets_file)
        if wallet_data:
            wallet_manager.wallets = wallet_data
            print("Wallet data loaded from file. / Đã tải dữ liệu ví từ file.")
            
    except FileNotFoundError:
        print("No saved data found. Starting with a fresh blockchain. / Không tìm thấy dữ liệu đã lưu. Bắt đầu với chuỗi khối mới.")
    except Exception as e:
        print(f"Could not load data: {e}. Starting fresh. / Không thể tải dữ liệu: {e}. Bắt đầu mới.")

    p2p_network = P2PNetwork(blockchain, host=config.network.p2p_host, port=config.network.p2p_port)

    # --- Execute Commands ---
    action_taken = False
    
    if args.command == 'create-wallet':
        action_taken = True
        wallet = wallet_manager.create_wallet(args.name)
        print(f"✅ Wallet '{args.name}' created / Đã tạo ví '{args.name}': {wallet['address']}")
    
    elif args.command == 'wallets':
        action_taken = True
        print("Wallets / Các ví:")
        wallets_list = wallet_manager.list_wallets()
        if not wallets_list:
            print("  No wallets found. / Không tìm thấy ví nào.")
        for name, address in wallets_list.items():
            print(f"  - {name}: {address}")

    elif args.command == 'chain':
        action_taken = True
        BlockchainVisualizer.print_chain(blockchain)

    elif args.command == 'status':
        action_taken = True
        BlockchainAnalyzer.print_status(blockchain)

    elif args.command == 'transaction':
        action_taken = True
        try:
            sender_wallet = wallet_manager.get_wallet(args.sender)
            receiver_wallet = wallet_manager.get_wallet(args.receiver)

            if not sender_wallet:
                raise ValueError(f"Sender wallet '{args.sender}' not found. / Không tìm thấy ví người gửi '{args.sender}'.")
            if not receiver_wallet:
                raise ValueError(f"Receiver wallet '{args.receiver}' not found. / Không tìm thấy ví người nhận '{args.receiver}'.")

            tx = Transaction(sender_wallet['address'], receiver_wallet['address'], args.amount, sender_wallet['private_key'])
            blockchain.add_transaction(tx)
            print("✅ Transaction added to local mempool. / Đã thêm giao dịch vào mempool cục bộ.")
            # p2p_network.broadcast_transaction(tx)
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e} / Lỗi không mong đợi: {e}")

    elif args.command == 'mine':
        action_taken = True
        miner_wallet_name = args.wallet
        miner_wallet = wallet_manager.get_wallet(miner_wallet_name)
        if not miner_wallet:
            print(f"Miner wallet '{miner_wallet_name}' not found, creating it... / Không tìm thấy ví '{miner_wallet_name}', đang tạo...")
            miner_wallet = wallet_manager.create_wallet(miner_wallet_name)

        print(f"⛏️  Mining a new block... (reward to: {miner_wallet_name}) / Đang đào khối mới... (thưởng cho: {miner_wallet_name})")
        if not blockchain.pending_transactions:
            print("ℹ️ No pending transactions to mine. A block will be created with only the reward. / Không có giao dịch chờ xử lý. Khối mới sẽ chỉ có giao dịch thưởng.")
        
        new_block = blockchain.mine_pending_transactions(miner_wallet['address'])
        print(f"🎉 New block #{new_block.index} mined successfully! / Đã đào xong khối mới #{new_block.index}!")
        BlockchainVisualizer.print_block(new_block)
        # p2p_network.broadcast_block(new_block)

    elif args.command == 'server':
        action_taken = True
        p2p_thread = threading.Thread(target=p2p_network.start)
        p2p_thread.daemon = True
        p2p_thread.start()

        http_server = BlockchainHTTPServer(
            (config.network.http_host, config.network.http_port),
            blockchain,
            p2p_network
        )
        http_thread = threading.Thread(target=http_server.serve_forever)
        http_thread.daemon = True
        http_thread.start()
        
        print(f"HTTP server running on http://{config.network.http_host}:{config.network.http_port}")
        print("Press Ctrl+C to shut down. / Nhấn Ctrl+C để tắt.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down... / Đang tắt...")

    # Save data if changed and not in server mode
    if action_taken and args.command != 'server':
        if args.command in ['transaction', 'mine', 'create-wallet']:
             if config.storage.auto_save:
                blockchain.save_to_file(config.storage.blockchain_file)
                FileUtils.save_json(config.storage.wallets_file, wallet_manager.wallets)
                print(f"💾 Blockchain and wallets saved. / Đã lưu chuỗi khối và ví.")

    if not action_taken:
        print("No action specified. Use 'python3 main.py --help' for options. / Không có hành động nào được chỉ định. Sử dụng 'python3 main.py --help' để xem các tùy chọn.")

if __name__ == "__main__":
    main() 