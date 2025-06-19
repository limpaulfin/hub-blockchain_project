#!/usr/bin/env python3
"""
Blockchain Tools & Visualization Module
File: utils/tools.py
Purpose: Các công cụ hỗ trợ và visualization cho blockchain
Dependencies: core modules
"""

import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

class BlockchainVisualizer:
    """
    Lớp visualization cho blockchain
    """
    
    @staticmethod
    def print_chain(blockchain) -> None:
        """
        In ra chuỗi blockchain dưới dạng ASCII art
        
        Args:
            blockchain: Blockchain object
        """
        print("\n" + "="*80)
        print("🔗 BLOCKCHAIN VISUALIZATION")
        print("="*80)
        
        for i, block in enumerate(blockchain.chain):
            BlockchainVisualizer.print_block(block, i)
            if i < len(blockchain.chain) - 1:
                print(" " * 38 + "⬆️")
                print(" " * 38 + "🔗")
                print(" " * 38 + "⬇️")

        print("="*80)
        print(f"Total Blocks: {len(blockchain.chain)}")
        print("="*80)

    @staticmethod
    def print_block(block, index: Optional[int] = None) -> None:
        """
        In ra một block dưới dạng ASCII art
        
        Args:
            block: Block object
            index: Vị trí block (optional)
        """
        block_index = index if index is not None else block.index
        
        print("." + "-"*78 + ".")
        print(f"| {'Block #' + str(block_index):<76} |")
        print("+" + "="*78 + "+")
        print(f"| {'Timestamp / Dấu thời gian:':<30} {datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S'):<46} |")
        print(f"| {'Difficulty / Độ khó:':<30} {block.difficulty:<46} |")
        print(f"| {'Nonce:':<30} {block.nonce:<46} |")
        print("+" + "-"*78 + "+")
        print(f"| {'Merkle Root:':<30} {block.merkle_root:<46} |")
        print(f"| {'Previous Hash / Hash Trước:':<30} {block.previous_hash:<46} |")
        print(f"| {'Block Hash / Hash Khối:':<30} {block.hash:<46} |")
        print("+" + "-"*78 + "+")
        print(f"| {'Transactions / Giao dịch:':<76} |")
        
        if block.transactions:
            for i, tx in enumerate(block.transactions):
                if tx.sender is None: # Mining Reward
                    tx_info = f"  {i+1}. From: System Reward / To: {tx.receiver[:10]}... / Amount: {tx.amount}"
                else:
                    tx_info = f"  {i+1}. From: {tx.sender[:10]}... / To: {tx.receiver[:10]}... / Amount: {tx.amount}"
                print(f"| {tx_info:<76} |")
        else:
            print(f"| {'  (No transactions in this block / Không có giao dịch)':<76} |")
            
        print("'" + "-"*78 + "'")

class BlockchainAnalyzer:
    """
    Lớp phân tích blockchain
    """
    
    @staticmethod
    def print_status(blockchain) -> None:
        """
        In ra trạng thái hiện tại của blockchain
        
        Args:
            blockchain: Blockchain object
        """
        print("\n" + "="*60)
        print("📊 BLOCKCHAIN STATUS / TRẠNG THÁI CHUỖI KHỐI")
        print("="*60)
        print(f"  - Total Blocks / Tổng số khối:         {len(blockchain.chain)}")
        print(f"  - Current Difficulty / Độ khó hiện tại:   {blockchain.difficulty}")
        print(f"  - Pending Transactions / Giao dịch chờ: {len(blockchain.pending_transactions)}")
        print(f"  - Chain valid / Chuỗi hợp lệ:          {blockchain.is_chain_valid()}")
        print("="*60)

class PerformanceMonitor:
    """
    Lớp theo dõi hiệu suất
    """
    
    @staticmethod
    def measure_mining_time(blockchain, miner_address: str) -> float:
        """
        Đo thời gian khai thác một block
        
        Args:
            blockchain: Blockchain object
            miner_address: Địa chỉ miner
            
        Returns:
            float: Thời gian khai thác (seconds)
        """
        start_time = time.time()
        blockchain.mine_block(miner_address)
        end_time = time.time()
        return end_time - start_time

class FileUtils:
    """
    Lớp tiện ích cho file operations
    """
    
    @staticmethod
    def save_json(filepath: str, data: Any) -> None:
        """
        Lưu dữ liệu vào file JSON
        
        Args:
            filepath: Đường dẫn file
            data: Dữ liệu cần lưu
        """

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data successfully saved to {filepath} / Dữ liệu đã được lưu vào {filepath}")
        except Exception as e:
            print(f"Error saving data to {filepath}: {e} / Lỗi khi lưu dữ liệu vào {filepath}: {e}")
    
    @staticmethod
    def load_json(filepath: str) -> Optional[Any]:
        """
        Load dữ liệu từ file JSON
        
        Args:
            filepath: Đường dẫn file
            
        Returns:
            Optional[Any]: Dữ liệu hoặc None nếu lỗi
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {filepath} / Không tìm thấy file: {filepath}")
            return None
        except Exception as e:
            print(f"Error loading data from {filepath}: {e} / Lỗi khi tải dữ liệu từ {filepath}: {e}")
            return None

# TODO: Add transaction analysis tools
# TODO: Implement network latency visualization
# TODO: Add block explorer utility
# TODO: Implement Merkle tree visualizer 