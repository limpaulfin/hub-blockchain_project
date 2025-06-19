#!/usr/bin/env python3
"""
Blockchain Block Module
File: core/block.py
Purpose: Định nghĩa cấu trúc Block và Merkle Tree
Dependencies: core/transaction.py, utils/crypto.py
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .transaction import Transaction

class Block:
    """
    Lớp Block đại diện cho một khối trong blockchain
    
    Attributes:
        index (int): Chỉ số của block trong chain
        transactions (List[Transaction]): Danh sách giao dịch
        timestamp (str): Thời gian tạo block
        previous_hash (str): Hash của block trước đó
        merkle_root (str): Root của Merkle tree
        nonce (int): Số dùng trong proof of work
        hash (str): Hash của block hiện tại
    """
    
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str):
        """
        Khởi tạo block mới
        
        Args:
            index: Vị trí của block trong blockchain
            transactions: Danh sách các giao dịch
            previous_hash: Hash của block trước đó
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = datetime.now().isoformat()
        self.previous_hash = previous_hash
        self.merkle_root = self.calculate_merkle_root()
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Tính toán hash SHA-256 của block
        
        Returns:
            str: Hash của block dưới dạng hex
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'nonce': self.nonce,
            'transactions_count': len(self.transactions)
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def calculate_merkle_root(self) -> str:
        """
        Tính toán Merkle root từ danh sách giao dịch
        
        Returns:
            str: Merkle root hash
        """
        if not self.transactions:
            return hashlib.sha256("".encode()).hexdigest()
        
        # Lấy hash của tất cả giao dịch
        transaction_hashes = [tx.transaction_hash for tx in self.transactions]
        
        # Tính Merkle tree
        while len(transaction_hashes) > 1:
            next_level = []
            
            # Nếu số lẻ, duplicate hash cuối
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
            
            # Tính hash cho từng cặp
            for i in range(0, len(transaction_hashes), 2):
                combined = transaction_hashes[i] + transaction_hashes[i + 1]
                next_level.append(hashlib.sha256(combined.encode()).hexdigest())
            
            transaction_hashes = next_level
        
        return transaction_hashes[0]
    
    def mine_block(self, difficulty: int):
        """
        Khai thác block với độ khó được chỉ định (Proof of Work)
        
        Args:
            difficulty: Số lượng số 0 đầu tiên trong hash
        """
        target = "0" * difficulty
        
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi block thành dictionary
        
        Returns:
            Dict: Dữ liệu block dưới dạng dictionary
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'nonce': self.nonce,
            'hash': self.hash,
            'transactions': [tx.to_dict() for tx in self.transactions]
        }
    
    def is_valid(self, previous_block: Optional['Block'] = None) -> bool:
        """
        Kiểm tra tính hợp lệ của block
        
        Args:
            previous_block: Block trước đó để kiểm tra liên kết
            
        Returns:
            bool: True nếu block hợp lệ
        """
        # Kiểm tra hash của block
        if self.hash != self.calculate_hash():
            return False
        
        # Kiểm tra merkle root
        if self.merkle_root != self.calculate_merkle_root():
            return False
        
        # Kiểm tra liên kết với block trước
        if previous_block and self.previous_hash != previous_block.hash:
            return False
        
        # Kiểm tra tính hợp lệ của tất cả giao dịch
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        
        return True
    
    def __str__(self) -> str:
        """String representation của block"""
        return f"Block #{self.index} (Hash: {self.hash[:16]}...)"

# TODO: Implement advanced Merkle tree operations
# TODO: Add block size validation
# TODO: Implement different consensus mechanisms 