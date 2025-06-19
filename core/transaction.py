#!/usr/bin/env python3
"""
Blockchain Transaction Module
File: core/transaction.py
Purpose: Quản lý cấu trúc và xử lý giao dịch trong blockchain
Dependencies: utils/crypto.py
"""

import hashlib
import json
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
    
    def __init__(self, sender: str, receiver: str, amount: float, data: Optional[Dict] = None):
        """
        Khởi tạo giao dịch mới
        
        Args:
            sender: Địa chỉ ví người gửi
            receiver: Địa chỉ ví người nhận
            amount: Số tiền giao dịch
            data: Dữ liệu bổ sung (metadata)
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now().isoformat()
        self.data = data or {}
        self.transaction_hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Tính toán hash SHA-256 của giao dịch
        
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
            'hash': self.transaction_hash
        }
    
    def is_valid(self) -> bool:
        """
        Kiểm tra tính hợp lệ của giao dịch
        
        Returns:
            bool: True nếu giao dịch hợp lệ
        """
        # Kiểm tra các trường bắt buộc
        if not self.sender or not self.receiver:
            return False
        
        # Kiểm tra số tiền phải dương
        if self.amount <= 0:
            return False
        
        # Xác minh hash
        calculated_hash = self.calculate_hash()
        return calculated_hash == self.transaction_hash
    
    def __str__(self) -> str:
        """String representation của giao dịch"""
        return f"Transaction({self.sender} -> {self.receiver}: {self.amount})"

# TODO: Implement digital signature verification
# TODO: Add transaction fee calculation
# TODO: Implement multi-signature support 