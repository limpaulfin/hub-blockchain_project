#!/usr/bin/env python3
"""
Blockchain Transaction Module
File: core/transaction.py
Purpose: Quản lý cấu trúc và xử lý giao dịch trong blockchain
Dependencies: utils/crypto.py
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class Transaction:
    """
    Lớp Transaction đại diện cho một giao dịch trong blockchain
    
    Attributes:
        sender (str): Địa chỉ người gửi
        receiver (str): Địa chỉ người nhận  
        amount (float): Số tiền giao dịch
        timestamp (str): Thời gian giao dịch
        transaction_hash (str): Hash của giao dịch
    """
    
    def __init__(self, sender: Optional[str], receiver: str, amount: float, private_key: Optional[str] = None, data: Optional[Dict] = None):
        """
        Khởi tạo giao dịch mới
        
        Args:
            sender: Địa chỉ ví người gửi (None cho giao dịch hệ thống)
            receiver: Địa chỉ ví người nhận
            amount: Số tiền giao dịch
            private_key: Khóa riêng của người gửi để ký
            data: Dữ liệu bổ sung (metadata)
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
        self.data = data or {}
        
        # Hash và signature được tính sau
        self.transaction_hash = self.calculate_hash()
        self.signature = None # Sẽ được thêm sau khi ký
        
        if sender and private_key:
            self.sign(private_key)

    def calculate_hash(self) -> str:
        """
        Tính toán hash SHA-256 của giao dịch (không bao gồm signature)
        
        Returns:
            str: Hash của giao dịch dưới dạng hex
        """
        transaction_string = json.dumps({
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'data': self.data
        }, sort_keys=True)
        
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def sign(self, private_key: str):
        """Ký giao dịch bằng private key"""
        # Đây là một ví dụ đơn giản, thực tế cần dùng ecdsa
        # self.signature = CryptoUtils.sign(self.transaction_hash, private_key)
        self.signature = f"signed_with_{private_key}" # Placeholder
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi giao dịch thành dictionary
        
        Returns:
            Dict: Dữ liệu giao dịch dưới dạng dictionary
        """
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'data': self.data,
            'transaction_hash': self.transaction_hash,
            'signature': self.signature
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """
        Tạo đối tượng Transaction từ dictionary
        """
        tx = cls(
            sender=data.get('sender'),
            receiver=data.get('receiver'),
            amount=data.get('amount'),
            data=data.get('data')
        )
        tx.timestamp = data.get('timestamp', time.time())
        tx.transaction_hash = data.get('transaction_hash', tx.calculate_hash())
        tx.signature = data.get('signature')
        return tx
    
    def is_valid(self) -> bool:
        """
        Kiểm tra tính hợp lệ của giao dịch
        
        Returns:
            bool: True nếu giao dịch hợp lệ
        """
        # Giao dịch hệ thống (thưởng) luôn hợp lệ
        if self.sender is None:
            return True
            
        if not self.sender or not self.receiver or not self.signature:
            return False
        
        if self.amount <= 0:
            return False
        
        # Xác minh hash
        if self.transaction_hash != self.calculate_hash():
            return False
        
        # Xác minh signature
        # valid_sig = CryptoUtils.verify(self.transaction_hash, self.signature, self.sender_public_key)
        # return valid_sig
        return True # Placeholder
    
    def __str__(self) -> str:
        """String representation của giao dịch"""
        if self.sender:
            return f"Transaction({self.sender[:10]}... -> {self.receiver[:10]}...: {self.amount})"
        return f"Transaction(System -> {self.receiver[:10]}...: {self.amount})"

# TODO: Implement digital signature verification
# TODO: Add transaction fee calculation
# TODO: Implement multi-signature support 