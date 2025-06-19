#!/usr/bin/env python3
"""
Blockchain Consensus Module
File: core/consensus.py
Purpose: Triển khai các cơ chế đồng thuận (Proof of Work, Proof of Stake)
Dependencies: core/block.py, core/blockchain.py
"""

import hashlib
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from .block import Block

class ConsensusAlgorithm(ABC):
    """
    Abstract base class cho các thuật toán đồng thuận
    """
    
    @abstractmethod
    def mine_block(self, block: Block, **kwargs) -> Block:
        """
        Khai thác block theo thuật toán đồng thuận
        
        Args:
            block: Block cần khai thác
            **kwargs: Tham số bổ sung
            
        Returns:
            Block: Block đã được khai thác
        """
        pass
    
    @abstractmethod
    def validate_block(self, block: Block, **kwargs) -> bool:
        """
        Xác thực block theo thuật toán đồng thuận
        
        Args:
            block: Block cần xác thực
            **kwargs: Tham số bổ sung
            
        Returns:
            bool: True nếu block hợp lệ
        """
        pass

class ProofOfWork(ConsensusAlgorithm):
    """
    Thuật toán đồng thuận Proof of Work (PoW)
    
    Attributes:
        difficulty (int): Độ khó khai thác (số lượng số 0 đầu tiên)
        target_time (int): Thời gian mục tiêu cho mỗi block (giây)
    """
    
    def __init__(self, difficulty: int = 4, target_time: int = 10):
        """
        Khởi tạo PoW consensus
        
        Args:
            difficulty: Độ khó ban đầu
            target_time: Thời gian mục tiêu giữa các block (giây)
        """
        self.difficulty = difficulty
        self.target_time = target_time
        self.mining_stats = {
            'blocks_mined': 0,
            'total_hash_attempts': 0,
            'average_mining_time': 0
        }
    
    def mine_block(self, block: Block, **kwargs) -> Block:
        """
        Khai thác block bằng Proof of Work
        
        Args:
            block: Block cần khai thác
            **kwargs: Có thể chứa 'difficulty' để override
            
        Returns:
            Block: Block đã được khai thác
        """
        difficulty = kwargs.get('difficulty', self.difficulty)
        target = "0" * difficulty
        
        start_time = time.time()
        hash_attempts = 0
        
        print(f"Mining block #{block.index} with difficulty {difficulty}...")
        
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.calculate_hash()
            hash_attempts += 1
            
            # Hiển thị progress mỗi 100,000 attempts
            if hash_attempts % 100000 == 0:
                print(f"Mining... {hash_attempts} attempts")
        
        mining_time = time.time() - start_time
        
        # Cập nhật stats
        self.mining_stats['blocks_mined'] += 1
        self.mining_stats['total_hash_attempts'] += hash_attempts
        self.mining_stats['average_mining_time'] = (
            (self.mining_stats['average_mining_time'] * (self.mining_stats['blocks_mined'] - 1) + mining_time) 
            / self.mining_stats['blocks_mined']
        )
        
        print(f"Block #{block.index} mined!")
        print(f"Hash: {block.hash}")
        print(f"Nonce: {block.nonce}")
        print(f"Mining time: {mining_time:.2f} seconds")
        print(f"Hash attempts: {hash_attempts}")
        
        return block
    
    def validate_block(self, block: Block, **kwargs) -> bool:
        """
        Xác thực block PoW
        
        Args:
            block: Block cần xác thực
            **kwargs: Có thể chứa 'difficulty'
            
        Returns:
            bool: True nếu block hợp lệ
        """
        difficulty = kwargs.get('difficulty', self.difficulty)
        target = "0" * difficulty
        
        # Kiểm tra hash có đúng format không
        if not block.hash.startswith(target):
            return False
        
        # Kiểm tra hash có được tính đúng không
        calculated_hash = block.calculate_hash()
        if calculated_hash != block.hash:
            return False
        
        return True
    
    def adjust_difficulty(self, last_blocks: List[Block]) -> int:
        """
        Điều chỉnh độ khó dựa trên thời gian khai thác gần đây
        
        Args:
            last_blocks: Danh sách blocks gần đây
            
        Returns:
            int: Độ khó mới
        """
        if len(last_blocks) < 2:
            return self.difficulty
        
        # Tính thời gian trung bình giữa các blocks
        time_diffs = []
        for i in range(1, len(last_blocks)):
            current_time = time.fromisoformat(last_blocks[i].timestamp)
            prev_time = time.fromisoformat(last_blocks[i-1].timestamp)
            time_diffs.append((current_time - prev_time).total_seconds())
        
        avg_time = sum(time_diffs) / len(time_diffs)
        
        # Điều chỉnh difficulty
        if avg_time < self.target_time * 0.8:  # Quá nhanh
            new_difficulty = self.difficulty + 1
        elif avg_time > self.target_time * 1.2:  # Quá chậm
            new_difficulty = max(1, self.difficulty - 1)
        else:
            new_difficulty = self.difficulty
        
        if new_difficulty != self.difficulty:
            print(f"Difficulty adjusted: {self.difficulty} -> {new_difficulty}")
            print(f"Average mining time: {avg_time:.2f}s, Target: {self.target_time}s")
        
        return new_difficulty
    
    def get_mining_stats(self) -> Dict[str, Any]:
        """Lấy thống kê khai thác"""
        return self.mining_stats.copy()

class ProofOfStake(ConsensusAlgorithm):
    """
    Thuật toán đồng thuận Proof of Stake (PoS) - Placeholder
    
    Note: Đây là implementation cơ bản cho mục đích học tập
    """
    
    def __init__(self, minimum_stake: float = 100.0):
        """
        Khởi tạo PoS consensus
        
        Args:
            minimum_stake: Số tiền tối thiểu để tham gia staking
        """
        self.minimum_stake = minimum_stake
        self.validators = {}  # address -> stake amount
    
    def mine_block(self, block: Block, **kwargs) -> Block:
        """
        Tạo block bằng PoS (simplified)
        
        Args:
            block: Block cần tạo
            **kwargs: Có thể chứa 'validator_address'
            
        Returns:
            Block: Block đã được tạo
        """
        validator_address = kwargs.get('validator_address')
        
        if not validator_address or validator_address not in self.validators:
            raise ValueError("Invalid validator address")
        
        if self.validators[validator_address] < self.minimum_stake:
            raise ValueError("Insufficient stake to validate")
        
        # Trong PoS, không cần nonce mà chỉ cần timestamp và validator signature
        block.nonce = 0
        block.hash = block.calculate_hash()
        
        print(f"Block #{block.index} validated by {validator_address}")
        print(f"Stake amount: {self.validators[validator_address]}")
        
        return block
    
    def validate_block(self, block: Block, **kwargs) -> bool:
        """
        Xác thực block PoS
        
        Args:
            block: Block cần xác thực
            **kwargs: Có thể chứa 'validator_address'
            
        Returns:
            bool: True nếu block hợp lệ
        """
        # Kiểm tra hash
        calculated_hash = block.calculate_hash()
        if calculated_hash != block.hash:
            return False
        
        # TODO: Implement signature verification
        # TODO: Implement slashing conditions
        
        return True
    
    def add_validator(self, address: str, stake_amount: float):
        """
        Thêm validator mới
        
        Args:
            address: Địa chỉ của validator
            stake_amount: Số tiền stake
        """
        if stake_amount >= self.minimum_stake:
            self.validators[address] = stake_amount
            print(f"Validator {address} added with stake {stake_amount}")
        else:
            raise ValueError(f"Stake amount {stake_amount} below minimum {self.minimum_stake}")
    
    def select_validator(self) -> str:
        """
        Chọn validator dựa trên stake weight (simplified random selection)
        
        Returns:
            str: Địa chỉ của validator được chọn
        """
        if not self.validators:
            raise ValueError("No validators available")
        
        # Simplified: chọn validator có stake cao nhất
        return max(self.validators.items(), key=lambda x: x[1])[0]

# Factory function để tạo consensus algorithm
def create_consensus(algorithm: str, **kwargs) -> ConsensusAlgorithm:
    """
    Factory function tạo consensus algorithm
    
    Args:
        algorithm: Tên thuật toán ('pow' hoặc 'pos')
        **kwargs: Tham số cho thuật toán
        
    Returns:
        ConsensusAlgorithm: Instance của thuật toán đồng thuận
    """
    if algorithm.lower() == 'pow':
        return ProofOfWork(**kwargs)
    elif algorithm.lower() == 'pos':
        return ProofOfStake(**kwargs)
    else:
        raise ValueError(f"Unknown consensus algorithm: {algorithm}")

# TODO: Implement Delegated Proof of Stake (DPoS)
# TODO: Add validator slashing mechanisms
# TODO: Implement stake delegation
# TODO: Add reward distribution logic 