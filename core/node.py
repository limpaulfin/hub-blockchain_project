#!/usr/bin/env python3
"""
Blockchain Node Module
File: core/node.py
Purpose: Quản lý node trong mạng blockchain phân tán
Dependencies: core/blockchain.py, network/p2p.py
"""

import uuid
from typing import Dict, List, Set
from .blockchain import Blockchain
from .transaction import Transaction

class Node:
    """
    Lớp Node đại diện cho một node trong mạng blockchain
    
    Attributes:
        node_id (str): ID duy nhất của node
        blockchain (Blockchain): Blockchain instance của node
        peers (Set[str]): Danh sách các peer nodes
        is_mining (bool): Trạng thái khai thác
        wallet_address (str): Địa chỉ ví của node
    """
    
    def __init__(self, wallet_address: str = None):
        """
        Khởi tạo node mới
        
        Args:
            wallet_address: Địa chỉ ví của node (optional)
        """
        self.node_id = str(uuid.uuid4())
        self.blockchain = Blockchain()
        self.peers: Set[str] = set()
        self.is_mining = False
        self.wallet_address = wallet_address or f"node_{self.node_id[:8]}"
        
        print(f"Node {self.node_id[:8]} initialized with wallet: {self.wallet_address}")
    
    def connect_peer(self, peer_address: str):
        """
        Kết nối với peer node khác
        
        Args:
            peer_address: Địa chỉ của peer node
        """
        if peer_address != self.node_id:
            self.peers.add(peer_address)
            print(f"Connected to peer: {peer_address}")
    
    def disconnect_peer(self, peer_address: str):
        """
        Ngắt kết nối với peer node
        
        Args:
            peer_address: Địa chỉ của peer node
        """
        self.peers.discard(peer_address)
        print(f"Disconnected from peer: {peer_address}")
    
    def broadcast_transaction(self, transaction: Transaction):
        """
        Phát tán giao dịch đến tất cả peers
        
        Args:
            transaction: Giao dịch cần phát tán
        """
        # Thêm vào blockchain local trước
        try:
            self.blockchain.add_transaction(transaction)
            print(f"Transaction added to local pool: {transaction.transaction_hash[:16]}...")
            
            # TODO: Implement actual network broadcasting
            print(f"Broadcasting transaction to {len(self.peers)} peers")
            
        except Exception as e:
            print(f"Failed to add transaction: {e}")
    
    def start_mining(self):
        """Bắt đầu khai thác blocks"""
        if len(self.blockchain.pending_transactions) == 0:
            print("No pending transactions to mine")
            return
        
        self.is_mining = True
        print(f"Node {self.node_id[:8]} started mining...")
        
        try:
            # Khai thác block với pending transactions
            new_block = self.blockchain.mine_pending_transactions(self.wallet_address)
            print(f"Block #{new_block.index} mined successfully!")
            print(f"Block hash: {new_block.hash}")
            
            # TODO: Broadcast new block to peers
            self.broadcast_new_block(new_block)
            
        except Exception as e:
            print(f"Mining failed: {e}")
        finally:
            self.is_mining = False
    
    def broadcast_new_block(self, block):
        """
        Phát tán block mới đến peers
        
        Args:
            block: Block vừa được khai thác
        """
        # TODO: Implement actual network broadcasting
        print(f"Broadcasting new block #{block.index} to {len(self.peers)} peers")
    
    def sync_blockchain(self, peer_blockchain_data: Dict):
        """
        Đồng bộ blockchain với peer
        
        Args:
            peer_blockchain_data: Dữ liệu blockchain từ peer
        """
        # TODO: Implement blockchain synchronization logic
        # - Compare chain lengths
        # - Validate incoming chain
        # - Replace if valid and longer
        print("Synchronizing blockchain with peers...")
    
    def get_node_status(self) -> Dict:
        """
        Lấy trạng thái hiện tại của node
        
        Returns:
            Dict: Thông tin trạng thái node
        """
        return {
            'node_id': self.node_id,
            'wallet_address': self.wallet_address,
            'is_mining': self.is_mining,
            'peers_count': len(self.peers),
            'blockchain_length': len(self.blockchain.chain),
            'pending_transactions': len(self.blockchain.pending_transactions),
            'wallet_balance': self.blockchain.get_balance(self.wallet_address)
        }
    
    def create_transaction(self, receiver: str, amount: float, data: Dict = None) -> Transaction:
        """
        Tạo giao dịch mới từ node này
        
        Args:
            receiver: Địa chỉ người nhận
            amount: Số tiền giao dịch
            data: Dữ liệu bổ sung
            
        Returns:
            Transaction: Giao dịch vừa tạo
        """
        # Kiểm tra số dư
        balance = self.blockchain.get_balance(self.wallet_address)
        if balance < amount:
            raise ValueError(f"Insufficient balance. Available: {balance}, Required: {amount}")
        
        # Tạo giao dịch
        transaction = Transaction(
            sender=self.wallet_address,
            receiver=receiver,
            amount=amount,
            data=data
        )
        
        return transaction
    
    def send_transaction(self, receiver: str, amount: float, data: Dict = None):
        """
        Tạo và gửi giao dịch
        
        Args:
            receiver: Địa chỉ người nhận
            amount: Số tiền giao dịch
            data: Dữ liệu bổ sung
        """
        try:
            transaction = self.create_transaction(receiver, amount, data)
            self.broadcast_transaction(transaction)
            print(f"Transaction sent: {amount} to {receiver}")
        except Exception as e:
            print(f"Failed to send transaction: {e}")
    
    def __str__(self) -> str:
        """String representation của node"""
        return f"Node({self.node_id[:8]}, peers: {len(self.peers)}, mining: {self.is_mining})"

# TODO: Implement digital signatures for transactions
# TODO: Add node authentication mechanisms
# TODO: Implement consensus participation
# TODO: Add transaction pool management 