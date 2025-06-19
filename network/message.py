#!/usr/bin/env python3
"""
Network Message Module
File: network/message.py
Purpose: Định nghĩa các loại message và serialization
Dependencies: core/transaction.py, core/block.py
"""

import json
import time
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

class MessageType(Enum):
    """Enum cho các loại message"""
    PING = "ping"
    PONG = "pong"
    PEER_DISCOVERY = "peer_discovery"
    PEER_LIST = "peer_list"
    NEW_TRANSACTION = "new_transaction"
    NEW_BLOCK = "new_block"
    REQUEST_BLOCKCHAIN = "request_blockchain"
    BLOCKCHAIN_DATA = "blockchain_data"
    SYNC_REQUEST = "sync_request"
    SYNC_RESPONSE = "sync_response"
    CONSENSUS_VOTE = "consensus_vote"
    NODE_STATUS = "node_status"

@dataclass
class BaseMessage:
    """
    Base class cho tất cả messages
    
    Attributes:
        type (str): Loại message
        from_node (str): ID của node gửi
        to_node (str): ID của node nhận (optional)
        timestamp (float): Timestamp tạo message
        message_id (str): ID duy nhất của message
    """
    type: str
    from_node: str
    timestamp: float
    to_node: Optional[str] = None
    message_id: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()
        if not self.message_id:
            self.message_id = f"{self.from_node}_{self.timestamp}"

@dataclass
class PingMessage(BaseMessage):
    """Message ping để kiểm tra kết nối"""
    type: str = MessageType.PING.value

@dataclass
class PongMessage(BaseMessage):
    """Message pong phản hồi ping"""
    type: str = MessageType.PONG.value
    original_timestamp: Optional[float] = None

@dataclass
class PeerDiscoveryMessage(BaseMessage):
    """Message yêu cầu danh sách peers"""
    type: str = MessageType.PEER_DISCOVERY.value
    requesting_peers: bool = True

@dataclass
class PeerListMessage(BaseMessage):
    """Message chứa danh sách peers"""
    type: str = MessageType.PEER_LIST.value
    peers: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.peers is None:
            self.peers = []

@dataclass
class NewTransactionMessage(BaseMessage):
    """Message thông báo giao dịch mới"""
    type: str = MessageType.NEW_TRANSACTION.value
    transaction_data: Dict[str, Any] = None

@dataclass
class NewBlockMessage(BaseMessage):
    """Message thông báo block mới"""
    type: str = MessageType.NEW_BLOCK.value
    block_data: Dict[str, Any] = None

@dataclass
class RequestBlockchainMessage(BaseMessage):
    """Message yêu cầu dữ liệu blockchain"""
    type: str = MessageType.REQUEST_BLOCKCHAIN.value
    from_index: int = 0
    to_index: Optional[int] = None

@dataclass
class BlockchainDataMessage(BaseMessage):
    """Message chứa dữ liệu blockchain"""
    type: str = MessageType.BLOCKCHAIN_DATA.value
    blockchain_data: Dict[str, Any] = None
    blocks: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.blocks is None:
            self.blocks = []

@dataclass
class SyncRequestMessage(BaseMessage):
    """Message yêu cầu đồng bộ"""
    type: str = MessageType.SYNC_REQUEST.value
    current_height: int = 0
    last_block_hash: str = ""

@dataclass
class SyncResponseMessage(BaseMessage):
    """Message phản hồi đồng bộ"""
    type: str = MessageType.SYNC_RESPONSE.value
    height: int = 0
    blocks_data: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.blocks_data is None:
            self.blocks_data = []

@dataclass
class ConsensusVoteMessage(BaseMessage):
    """Message voting cho consensus"""
    type: str = MessageType.CONSENSUS_VOTE.value
    block_hash: str = ""
    vote: str = ""  # "approve" hoặc "reject"
    round_number: int = 0

@dataclass
class NodeStatusMessage(BaseMessage):
    """Message trạng thái node"""
    type: str = MessageType.NODE_STATUS.value
    node_info: Dict[str, Any] = None

class MessageSerializer:
    """
    Lớp serialize/deserialize messages
    """
    
    # Mapping từ message type đến class
    MESSAGE_CLASSES = {
        MessageType.PING.value: PingMessage,
        MessageType.PONG.value: PongMessage,
        MessageType.PEER_DISCOVERY.value: PeerDiscoveryMessage,
        MessageType.PEER_LIST.value: PeerListMessage,
        MessageType.NEW_TRANSACTION.value: NewTransactionMessage,
        MessageType.NEW_BLOCK.value: NewBlockMessage,
        MessageType.REQUEST_BLOCKCHAIN.value: RequestBlockchainMessage,
        MessageType.BLOCKCHAIN_DATA.value: BlockchainDataMessage,
        MessageType.SYNC_REQUEST.value: SyncRequestMessage,
        MessageType.SYNC_RESPONSE.value: SyncResponseMessage,
        MessageType.CONSENSUS_VOTE.value: ConsensusVoteMessage,
        MessageType.NODE_STATUS.value: NodeStatusMessage,
    }
    
    @staticmethod
    def serialize(message: BaseMessage) -> str:
        """
        Serialize message thành JSON string
        
        Args:
            message: Message object
            
        Returns:
            str: JSON string
        """
        try:
            message_dict = asdict(message)
            return json.dumps(message_dict)
        except Exception as e:
            raise ValueError(f"Failed to serialize message: {e}")
    
    @staticmethod
    def deserialize(data: str) -> BaseMessage:
        """
        Deserialize JSON string thành message object
        
        Args:
            data: JSON string
            
        Returns:
            BaseMessage: Message object
        """
        try:
            message_dict = json.loads(data)
            message_type = message_dict.get('type')
            
            if message_type in MessageSerializer.MESSAGE_CLASSES:
                message_class = MessageSerializer.MESSAGE_CLASSES[message_type]
                # Loại bỏ các fields không cần thiết
                filtered_dict = {
                    k: v for k, v in message_dict.items()
                    if k in message_class.__dataclass_fields__
                }
                return message_class(**filtered_dict)
            else:
                # Fallback về BaseMessage
                return BaseMessage(**message_dict)
                
        except Exception as e:
            raise ValueError(f"Failed to deserialize message: {e}")
    
    @staticmethod
    def validate_message(message: BaseMessage) -> bool:
        """
        Kiểm tra tính hợp lệ của message
        
        Args:
            message: Message cần kiểm tra
            
        Returns:
            bool: True nếu message hợp lệ
        """
        # Kiểm tra các fields bắt buộc
        if not message.type or not message.from_node:
            return False
        
        # Kiểm tra timestamp hợp lý
        current_time = time.time()
        if message.timestamp > current_time + 300:  # Không quá 5 phút trong tương lai
            return False
        
        if message.timestamp < current_time - 3600:  # Không quá 1 giờ trong quá khứ
            return False
        
        return True

class MessageQueue:
    """
    Queue để quản lý messages
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Khởi tạo message queue
        
        Args:
            max_size: Kích thước tối đa của queue
        """
        self.messages: List[BaseMessage] = []
        self.max_size = max_size
        self.processed_ids: set = set()
    
    def add_message(self, message: BaseMessage) -> bool:
        """
        Thêm message vào queue
        
        Args:
            message: Message cần thêm
            
        Returns:
            bool: True nếu thêm thành công
        """
        # Kiểm tra duplicate
        if message.message_id in self.processed_ids:
            return False
        
        # Validate message
        if not MessageSerializer.validate_message(message):
            return False
        
        # Thêm vào queue
        self.messages.append(message)
        self.processed_ids.add(message.message_id)
        
        # Cleanup nếu vượt quá max_size
        if len(self.messages) > self.max_size:
            removed = self.messages.pop(0)
            self.processed_ids.discard(removed.message_id)
        
        return True
    
    def get_messages(self, message_type: Optional[str] = None) -> List[BaseMessage]:
        """
        Lấy messages theo type
        
        Args:
            message_type: Loại message cần lấy (None = tất cả)
            
        Returns:
            List[BaseMessage]: Danh sách messages
        """
        if message_type is None:
            return self.messages.copy()
        
        return [msg for msg in self.messages if msg.type == message_type]
    
    def clear_old_messages(self, max_age: float = 3600):
        """
        Xóa các messages cũ
        
        Args:
            max_age: Tuổi tối đa của message (giây)
        """
        current_time = time.time()
        threshold = current_time - max_age
        
        old_messages = []
        for i, message in enumerate(self.messages):
            if message.timestamp < threshold:
                old_messages.append(i)
                self.processed_ids.discard(message.message_id)
        
        # Xóa theo thứ tự ngược
        for i in reversed(old_messages):
            del self.messages[i]
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Lấy thống kê queue"""
        type_counts = {}
        for message in self.messages:
            type_counts[message.type] = type_counts.get(message.type, 0) + 1
        
        return {
            'total_messages': len(self.messages),
            'processed_ids_count': len(self.processed_ids),
            'message_types': type_counts
        }

# Utility functions
def create_ping_message(from_node: str, to_node: Optional[str] = None) -> PingMessage:
    """Tạo ping message"""
    return PingMessage(
        type=MessageType.PING.value,
        from_node=from_node,
        to_node=to_node,
        timestamp=time.time()
    )

def create_transaction_message(from_node: str, transaction_data: Dict) -> NewTransactionMessage:
    """Tạo new transaction message"""
    return NewTransactionMessage(
        type=MessageType.NEW_TRANSACTION.value,
        from_node=from_node,
        timestamp=time.time(),
        transaction_data=transaction_data
    )

def create_block_message(from_node: str, block_data: Dict) -> NewBlockMessage:
    """Tạo new block message"""
    return NewBlockMessage(
        type=MessageType.NEW_BLOCK.value,
        from_node=from_node,
        timestamp=time.time(),
        block_data=block_data
    )

# TODO: Implement message encryption
# TODO: Add message compression
# TODO: Implement message priority system
# TODO: Add rate limiting for message types 