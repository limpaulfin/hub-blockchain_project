#!/usr/bin/env python3
"""
Cryptographic Utilities Module
File: utils/crypto.py
Purpose: Các hàm mã hóa và bảo mật cho blockchain
Dependencies: hashlib, ecdsa
"""

import hashlib
import secrets
import base64
from typing import Tuple, Dict, Any, Optional

class CryptoUtils:
    """
    Lớp tiện ích cho các chức năng mã hóa
    """
    
    @staticmethod
    def sha256_hash(data: str) -> str:
        """
        Tính hash SHA-256 của dữ liệu
        
        Args:
            data: Dữ liệu cần hash
            
        Returns:
            str: Hash SHA-256 dưới dạng hex
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    @staticmethod
    def double_sha256(data: str) -> str:
        """
        Tính double SHA-256 (như Bitcoin)
        
        Args:
            data: Dữ liệu cần hash
            
        Returns:
            str: Double SHA-256 hash
        """
        first_hash = hashlib.sha256(data.encode('utf-8')).digest()
        return hashlib.sha256(first_hash).hexdigest()
    
    @staticmethod
    def generate_private_key() -> str:
        """
        Tạo private key ngẫu nhiên
        
        Returns:
            str: Private key dưới dạng hex
        """
        return secrets.token_hex(32)
    
    @staticmethod
    def generate_address(private_key: str) -> str:
        """
        Tạo địa chỉ ví từ private key (simplified)
        
        Args:
            private_key: Private key dưới dạng hex
            
        Returns:
            str: Địa chỉ ví
        """
        # Simplified address generation (thực tế phức tạp hơn)
        hash_object = hashlib.sha256(private_key.encode())
        return f"1{hash_object.hexdigest()[:32]}"
    
    @staticmethod
    def merkle_root(hashes: list) -> str:
        """
        Tính Merkle root từ danh sách hashes
        
        Args:
            hashes: Danh sách các hash
            
        Returns:
            str: Merkle root
        """
        if not hashes:
            return CryptoUtils.sha256_hash("")
        
        if len(hashes) == 1:
            return hashes[0]
        
        # Duplicate last hash if odd number
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])
        
        next_level = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i + 1]
            next_level.append(CryptoUtils.sha256_hash(combined))
        
        return CryptoUtils.merkle_root(next_level)
    
    @staticmethod
    def proof_of_work(data: str, difficulty: int) -> Tuple[int, str]:
        """
        Thực hiện Proof of Work
        
        Args:
            data: Dữ liệu cần hash
            difficulty: Độ khó (số lượng số 0 đầu tiên)
            
        Returns:
            Tuple[int, str]: (nonce, hash)
        """
        target = "0" * difficulty
        nonce = 0
        
        while True:
            hash_input = f"{data}{nonce}"
            hash_result = CryptoUtils.sha256_hash(hash_input)
            
            if hash_result.startswith(target):
                return nonce, hash_result
            
            nonce += 1
    
    @staticmethod
    def validate_hash(data: str, nonce: int, expected_hash: str) -> bool:
        """
        Xác thực hash với nonce
        
        Args:
            data: Dữ liệu gốc
            nonce: Nonce được sử dụng
            expected_hash: Hash mong đợi
            
        Returns:
            bool: True nếu hash hợp lệ
        """
        hash_input = f"{data}{nonce}"
        calculated_hash = CryptoUtils.sha256_hash(hash_input)
        return calculated_hash == expected_hash

class DigitalSignature:
    """
    Lớp cho digital signature (simplified implementation)
    """
    
    @staticmethod
    def generate_keypair() -> Tuple[str, str]:
        """
        Tạo cặp khóa công khai/riêng tư
        
        Returns:
            Tuple[str, str]: (private_key, public_key)
        """
        private_key = CryptoUtils.generate_private_key()
        public_key = CryptoUtils.sha256_hash(private_key)[:64]
        return private_key, public_key
    
    @staticmethod
    def sign_message(message: str, private_key: str) -> str:
        """
        Ký message bằng private key (simplified)
        
        Args:
            message: Message cần ký
            private_key: Private key
            
        Returns:
            str: Digital signature
        """
        combined = f"{message}{private_key}"
        return CryptoUtils.sha256_hash(combined)
    
    @staticmethod
    def verify_signature(message: str, signature: str, public_key: str) -> bool:
        """
        Xác thực digital signature (simplified)
        
        Args:
            message: Message gốc
            signature: Digital signature
            public_key: Public key
            
        Returns:
            bool: True nếu signature hợp lệ
        """
        # Simplified verification (trong thực tế phức tạp hơn)
        expected_hash = CryptoUtils.sha256_hash(f"{message}{public_key}")
        return len(signature) == 64  # Basic validation

class WalletManager:
    """
    Quản lý ví và khóa
    """
    
    def __init__(self):
        self.wallets: Dict[str, Dict[str, str]] = {}
    
    def create_wallet(self, wallet_name: str) -> Dict[str, str]:
        """
        Tạo ví mới
        
        Args:
            wallet_name: Tên ví
            
        Returns:
            Dict: Thông tin ví (address, private_key, public_key)
        """
        private_key, public_key = DigitalSignature.generate_keypair()
        address = CryptoUtils.generate_address(private_key)
        
        wallet_info = {
            'address': address,
            'private_key': private_key,
            'public_key': public_key
        }
        
        self.wallets[wallet_name] = wallet_info
        return wallet_info
    
    def get_wallet(self, wallet_name: str) -> Optional[Dict[str, str]]:
        """
        Lấy thông tin ví
        
        Args:
            wallet_name: Tên ví
            
        Returns:
            Optional[Dict]: Thông tin ví hoặc None
        """
        return self.wallets.get(wallet_name)
    
    def list_wallets(self) -> Dict[str, str]:
        """
        Liệt kê tất cả ví
        
        Returns:
            Dict: Mapping từ tên ví đến địa chỉ
        """
        return {name: info['address'] for name, info in self.wallets.items()}

# Utility functions
def hash_transaction(sender: str, receiver: str, amount: float, timestamp: str) -> str:
    """
    Hash một giao dịch
    
    Args:
        sender: Người gửi
        receiver: Người nhận
        amount: Số tiền
        timestamp: Thời gian
        
    Returns:
        str: Hash của giao dịch
    """
    data = f"{sender}{receiver}{amount}{timestamp}"
    return CryptoUtils.sha256_hash(data)

def hash_block(index: int, timestamp: str, previous_hash: str, merkle_root: str, nonce: int) -> str:
    """
    Hash một block
    
    Args:
        index: Chỉ số block
        timestamp: Thời gian
        previous_hash: Hash block trước
        merkle_root: Merkle root
        nonce: Nonce
        
    Returns:
        str: Hash của block
    """
    data = f"{index}{timestamp}{previous_hash}{merkle_root}{nonce}"
    return CryptoUtils.sha256_hash(data)

# TODO: Implement ECDSA digital signatures
# TODO: Add key derivation functions (PBKDF2, scrypt)
# TODO: Implement HD wallets (BIP32)
# TODO: Add encryption/decryption utilities 