#!/usr/bin/env python3
"""
Blockchain Core Module
File: core/blockchain.py
Purpose: Lớp chính quản lý toàn bộ blockchain
Dependencies: core/block.py, core/transaction.py
"""

import json
from typing import List, Dict, Any, Optional
from .block import Block
from .transaction import Transaction

class Blockchain:
    """
    Lớp Blockchain quản lý toàn bộ chuỗi khối
    
    Attributes:
        chain (List[Block]): Danh sách các block trong blockchain
        difficulty (int): Độ khó khai thác
        pending_transactions (List[Transaction]): Giao dịch chờ xử lý
        mining_reward (float): Phần thưởng khai thác
    """
    
    def __init__(self):
        """Khởi tạo blockchain với genesis block"""
        self.chain: List[Block] = []
        self.difficulty = 2  # Độ khó mặc định (số lượng số 0 đầu tiên)
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 10.0
        
        # Tạo genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Tạo block đầu tiên (Genesis Block)"""
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """
        Lấy block cuối cùng trong chain
        
        Returns:
            Block: Block cuối cùng
        """
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction):
        """
        Thêm giao dịch vào pending pool
        
        Args:
            transaction: Giao dịch cần thêm
        """
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
        else:
            raise ValueError("Giao dịch không hợp lệ")
    
    def mine_pending_transactions(self, mining_reward_address: str) -> Block:
        """
        Khai thác tất cả giao dịch pending thành một block mới
        
        Args:
            mining_reward_address: Địa chỉ nhận phần thưởng khai thác
            
        Returns:
            Block: Block vừa được khai thác
        """
        # Thêm giao dịch reward cho miner
        reward_transaction = Transaction(
            sender=None,  # System transaction
            receiver=mining_reward_address,
            amount=self.mining_reward,
            data={"type": "mining_reward"}
        )
        
        # Thêm reward transaction vào pending
        transactions_to_mine = self.pending_transactions + [reward_transaction]
        
        # Tạo block mới
        block = Block(
            index=len(self.chain),
            transactions=transactions_to_mine,
            previous_hash=self.get_latest_block().hash
        )
        
        # Khai thác block
        block.mine_block(self.difficulty)
        
        # Thêm vào chain và clear pending
        self.chain.append(block)
        self.pending_transactions = []
        
        return block
    
    def add_block(self, block: Block) -> bool:
        """
        Thêm một block nhận từ mạng vào chuỗi (sau khi xác thực)
        
        Returns:
            bool: True nếu thêm thành công
        """
        latest_block = self.get_latest_block()
        if block.is_valid(latest_block):
            self.chain.append(block)
            self.clear_transactions_from_mempool(block.transactions)
            return True
        return False

    def clear_transactions_from_mempool(self, mined_transactions: List[Transaction]):
        """Xóa các giao dịch đã được đào khỏi mempool."""
        mined_tx_hashes = {tx.transaction_hash for tx in mined_transactions}
        self.pending_transactions = [
            tx for tx in self.pending_transactions if tx.transaction_hash not in mined_tx_hashes
        ]

    def get_balance(self, address: str) -> float:
        """
        Tính số dư của một địa chỉ
        
        Args:
            address: Địa chỉ ví cần kiểm tra
            
        Returns:
            float: Số dư hiện tại
        """
        balance = 0.0
        
        # Duyệt qua tất cả block (trừ genesis)
        for block in self.chain[1:]:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """
        Kiểm tra tính hợp lệ của toàn bộ blockchain
        
        Returns:
            bool: True nếu blockchain hợp lệ
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Kiểm tra block hiện tại
            if not current_block.is_valid(previous_block):
                return False
            
            # Kiểm tra liên kết với block trước
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    @staticmethod
    def block_from_dict(block_data: Dict[str, Any]) -> Block:
        """Tạo đối tượng Block từ dictionary."""
        transactions = [Transaction.from_dict(tx) for tx in block_data.get('transactions', [])]
        block = Block(
            index=block_data['index'],
            transactions=transactions,
            previous_hash=block_data['previous_hash']
        )
        block.timestamp = block_data['timestamp']
        block.merkle_root = block_data['merkle_root']
        block.nonce = block_data['nonce']
        block.difficulty = block_data['difficulty']
        block.hash = block_data['hash']
        return block

    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi blockchain thành dictionary
        
        Returns:
            Dict: Dữ liệu blockchain
        """
        return {
            'chain': [block.to_dict() for block in self.chain],
            'difficulty': self.difficulty,
            'pending_transactions': [tx.to_dict() for tx in self.pending_transactions],
            'mining_reward': self.mining_reward
        }
    
    def save_to_file(self, filename: str):
        """Lưu blockchain vào file JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def get_transaction_history(self, address: str) -> List[Dict]:
        """
        Lấy lịch sử giao dịch của một địa chỉ
        
        Args:
            address: Địa chỉ cần tra cứu
            
        Returns:
            List[Dict]: Danh sách giao dịch liên quan
        """
        history = []
        
        for block in self.chain[1:]:  # Skip genesis block
            for transaction in block.transactions:
                if transaction.sender == address or transaction.receiver == address:
                    tx_data = transaction.to_dict()
                    tx_data['block_index'] = block.index
                    tx_data['block_timestamp'] = block.timestamp
                    history.append(tx_data)
        
        return history
    
    def __str__(self) -> str:
        """String representation của blockchain"""
        return f"Blockchain(blocks: {len(self.chain)}, pending: {len(self.pending_transactions)})"

# TODO: Implement transaction fees
# TODO: Add mempool management
# TODO: Implement different consensus algorithms
# TODO: Add blockchain state snapshots 