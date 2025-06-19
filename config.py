#!/usr/bin/env python3
"""
Blockchain Configuration Module
File: config.py
Purpose: Quản lý cấu hình toàn bộ hệ thống blockchain
Dependencies: None
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class NetworkConfig:
    """Cấu hình mạng"""
    p2p_host: str = "localhost"
    p2p_port: int = 8000
    http_host: str = "localhost"
    http_port: int = 8080
    max_peers: int = 10
    connection_timeout: int = 30
    message_timeout: int = 60

@dataclass
class BlockchainConfig:
    """Cấu hình blockchain"""
    difficulty: int = 2
    target_block_time: int = 10  # seconds
    max_transactions_per_block: int = 100
    mining_reward: float = 10.0
    min_transaction_amount: float = 0.01
    max_transaction_amount: float = 1000000.0

@dataclass
class ConsensusConfig:
    """Cấu hình consensus"""
    algorithm: str = "pow"  # "pow" or "pos"
    pos_minimum_stake: float = 100.0
    difficulty_adjustment_blocks: int = 10
    max_mining_threads: int = 1

@dataclass
class StorageConfig:
    """Cấu hình lưu trữ"""
    data_directory: str = "./data"
    blockchain_file: str = "blockchain.json"
    wallet_file: str = "wallets.json"
    auto_save: bool = True
    backup_interval: int = 3600  # seconds

@dataclass
class LoggingConfig:
    """Cấu hình logging"""
    level: str = "INFO"
    file_path: str = "./logs/blockchain.log"
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5
    enable_console: bool = True

class Config:
    """
    Lớp quản lý cấu hình chính
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Khởi tạo config
        
        Args:
            config_file: Đường dẫn file config (optional)
        """
        # Default configurations
        self.network = NetworkConfig()
        self.blockchain = BlockchainConfig()
        self.consensus = ConsensusConfig()
        self.storage = StorageConfig()
        self.logging = LoggingConfig()
        
        # Development vs Production
        self.environment = os.getenv("BLOCKCHAIN_ENV", "development")
        
        # Load from file if provided
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        
        # Override with environment variables
        self._load_from_environment()
        
        # Validate configuration
        self._validate_config()
    
    def _load_from_environment(self):
        """Load configuration từ environment variables"""
        
        # Network config
        self.network.p2p_host = os.getenv("P2P_HOST", self.network.p2p_host)
        self.network.p2p_port = int(os.getenv("P2P_PORT", str(self.network.p2p_port)))
        self.network.http_host = os.getenv("HTTP_HOST", self.network.http_host)
        self.network.http_port = int(os.getenv("HTTP_PORT", str(self.network.http_port)))
        
        # Blockchain config
        self.blockchain.difficulty = int(os.getenv("MINING_DIFFICULTY", str(self.blockchain.difficulty)))
        self.blockchain.mining_reward = float(os.getenv("MINING_REWARD", str(self.blockchain.mining_reward)))
        
        # Consensus config
        self.consensus.algorithm = os.getenv("CONSENSUS_ALGORITHM", self.consensus.algorithm)
        
        # Storage config
        self.storage.data_directory = os.getenv("DATA_DIRECTORY", self.storage.data_directory)
    
    def _validate_config(self):
        """Validate cấu hình"""
        
        # Validate ports
        if not (1024 <= self.network.p2p_port <= 65535):
            raise ValueError(f"Invalid P2P port: {self.network.p2p_port}")
        
        if not (1024 <= self.network.http_port <= 65535):
            raise ValueError(f"Invalid HTTP port: {self.network.http_port}")
        
        # Validate difficulty
        if not (1 <= self.blockchain.difficulty <= 10):
            raise ValueError(f"Invalid difficulty: {self.blockchain.difficulty}")
        
        # Validate consensus algorithm
        if self.consensus.algorithm not in ["pow", "pos"]:
            raise ValueError(f"Invalid consensus algorithm: {self.consensus.algorithm}")
        
        # Create directories if needed
        os.makedirs(self.storage.data_directory, exist_ok=True)
        os.makedirs(os.path.dirname(self.logging.file_path), exist_ok=True)
    
    def load_from_file(self, config_file: str):
        """
        Load configuration từ file JSON
        
        Args:
            config_file: Đường dẫn file config
        """
        import json
        
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
            
            # Update configurations
            if 'network' in data:
                for key, value in data['network'].items():
                    if hasattr(self.network, key):
                        setattr(self.network, key, value)
            
            if 'blockchain' in data:
                for key, value in data['blockchain'].items():
                    if hasattr(self.blockchain, key):
                        setattr(self.blockchain, key, value)
            
            if 'consensus' in data:
                for key, value in data['consensus'].items():
                    if hasattr(self.consensus, key):
                        setattr(self.consensus, key, value)
            
            if 'storage' in data:
                for key, value in data['storage'].items():
                    if hasattr(self.storage, key):
                        setattr(self.storage, key, value)
            
            if 'logging' in data:
                for key, value in data['logging'].items():
                    if hasattr(self.logging, key):
                        setattr(self.logging, key, value)
        
        except Exception as e:
            print(f"Failed to load config from {config_file}: {e}")
    
    def save_to_file(self, config_file: str):
        """
        Lưu configuration ra file JSON
        
        Args:
            config_file: Đường dẫn file config
        """
        import json
        
        data = {
            'network': self.network.__dict__,
            'blockchain': self.blockchain.__dict__,
            'consensus': self.consensus.__dict__,
            'storage': self.storage.__dict__,
            'logging': self.logging.__dict__
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Configuration saved to {config_file}")
        except Exception as e:
            print(f"Failed to save config to {config_file}: {e}")
    
    def get_blockchain_file_path(self) -> str:
        """Lấy đường dẫn file blockchain"""
        return os.path.join(self.storage.data_directory, self.storage.blockchain_file)
    
    def get_wallet_file_path(self) -> str:
        """Lấy đường dẫn file wallet"""
        return os.path.join(self.storage.data_directory, self.storage.wallet_file)
    
    def is_development(self) -> bool:
        """Kiểm tra có phải development environment"""
        return self.environment == "development"
    
    def is_production(self) -> bool:
        """Kiểm tra có phải production environment"""
        return self.environment == "production"
    
    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi config thành dictionary"""
        return {
            'environment': self.environment,
            'network': self.network.__dict__,
            'blockchain': self.blockchain.__dict__,
            'consensus': self.consensus.__dict__,
            'storage': self.storage.__dict__,
            'logging': self.logging.__dict__
        }
    
    def print_config(self):
        """In cấu hình hiện tại"""
        print("\n🔧 BLOCKCHAIN CONFIGURATION")
        print("="*60)
        print(f"Environment: {self.environment}")
        print("\nNetwork:")
        print(f"  P2P:  {self.network.p2p_host}:{self.network.p2p_port}")
        print(f"  HTTP: {self.network.http_host}:{self.network.http_port}")
        print(f"  Max Peers: {self.network.max_peers}")
        
        print("\nBlockchain:")
        print(f"  Difficulty: {self.blockchain.difficulty}")
        print(f"  Target Block Time: {self.blockchain.target_block_time}s")
        print(f"  Mining Reward: {self.blockchain.mining_reward}")
        print(f"  Max Transactions/Block: {self.blockchain.max_transactions_per_block}")
        
        print("\nConsensus:")
        print(f"  Algorithm: {self.consensus.algorithm.upper()}")
        if self.consensus.algorithm == "pos":
            print(f"  Minimum Stake: {self.consensus.pos_minimum_stake}")
        
        print("\nStorage:")
        print(f"  Data Directory: {self.storage.data_directory}")
        print(f"  Auto Save: {self.storage.auto_save}")
        
        print("="*60)

# Predefined configurations
DEVELOPMENT_CONFIG = {
    'network': {
        'p2p_port': 8000,
        'http_port': 8080,
        'max_peers': 5
    },
    'blockchain': {
        'difficulty': 2,
        'mining_reward': 10.0
    },
    'logging': {
        'level': 'DEBUG',
        'enable_console': True
    }
}

PRODUCTION_CONFIG = {
    'network': {
        'p2p_port': 9000,
        'http_port': 9080,
        'max_peers': 20
    },
    'blockchain': {
        'difficulty': 4,
        'mining_reward': 5.0
    },
    'logging': {
        'level': 'INFO',
        'enable_console': False
    }
}

# Global config instance
config = Config()

# Helper functions
def get_config() -> Config:
    """Lấy global config instance"""
    return config

def load_config(config_file: str) -> Config:
    """Load config từ file"""
    global config
    config = Config(config_file)
    return config

def create_sample_config(filename: str = "blockchain_config.json"):
    """Tạo file config mẫu"""
    sample_config = Config()
    sample_config.save_to_file(filename)
    print(f"Sample configuration created: {filename}")

# TODO: Add configuration validation rules
# TODO: Implement hot-reload configuration
# TODO: Add configuration templates for different use cases
# TODO: Implement configuration encryption for sensitive data 