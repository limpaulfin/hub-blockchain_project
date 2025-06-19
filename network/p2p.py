#!/usr/bin/env python3
"""
Peer-to-Peer Network Module
File: network/p2p.py
Purpose: Quản lý kết nối P2P và giao tiếp giữa các nodes
Dependencies: network/message.py, core/node.py
"""

import socket
import threading
import json
import time
from typing import Dict, List, Set, Optional, Callable
from dataclasses import dataclass

@dataclass
class PeerInfo:
    """
    Thông tin về một peer node
    
    Attributes:
        address (str): Địa chỉ IP
        port (int): Port kết nối
        node_id (str): ID của node
        last_seen (float): Timestamp lần cuối gặp
        is_connected (bool): Trạng thái kết nối
    """
    address: str
    port: int
    node_id: str = ""
    last_seen: float = 0.0
    is_connected: bool = False
    
    @property
    def endpoint(self) -> str:
        """Địa chỉ endpoint đầy đủ"""
        return f"{self.address}:{self.port}"

class P2PNetwork:
    """
    Lớp quản lý mạng P2P cho blockchain
    
    Attributes:
        host (str): Địa chỉ host của node này
        port (int): Port lắng nghe
        node_id (str): ID của node này
        peers (Dict[str, PeerInfo]): Danh sách peers
        message_handlers (Dict[str, Callable]): Handlers cho các loại message
    """
    
    def __init__(self, host: str = "localhost", port: int = 8000, node_id: str = ""):
        """
        Khởi tạo P2P network
        
        Args:
            host: Địa chỉ IP để bind
            port: Port để lắng nghe
            node_id: ID của node này
        """
        self.host = host
        self.port = port
        self.node_id = node_id
        self.peers: Dict[str, PeerInfo] = {}
        self.message_handlers: Dict[str, Callable] = {}
        
        # Network components
        self.server_socket: Optional[socket.socket] = None
        self.is_running = False
        self.server_thread: Optional[threading.Thread] = None
        
        # Default message handlers
        self._register_default_handlers()
        
        print(f"P2P Network initialized on {host}:{port}")
    
    def _register_default_handlers(self):
        """Đăng ký các message handlers mặc định"""
        self.register_handler("ping", self._handle_ping)
        self.register_handler("pong", self._handle_pong)
        self.register_handler("peer_discovery", self._handle_peer_discovery)
        self.register_handler("peer_list", self._handle_peer_list)
    
    def register_handler(self, message_type: str, handler: Callable):
        """
        Đăng ký handler cho loại message
        
        Args:
            message_type: Loại message
            handler: Function để xử lý message
        """
        self.message_handlers[message_type] = handler
        print(f"Registered handler for message type: {message_type}")
    
    def start_server(self):
        """Bắt đầu server P2P"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            
            self.is_running = True
            self.server_thread = threading.Thread(target=self._accept_connections)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            print(f"P2P Server started on {self.host}:{self.port}")
            
        except Exception as e:
            print(f"Failed to start P2P server: {e}")
    
    def stop_server(self):
        """Dừng server P2P"""
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        print("P2P Server stopped")
    
    def _accept_connections(self):
        """Accept incoming connections (chạy trong thread riêng)"""
        while self.is_running:
            try:
                client_socket, address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
                print(f"New connection from {address}")
                
            except Exception as e:
                if self.is_running:
                    print(f"Error accepting connection: {e}")
    
    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """
        Xử lý client connection
        
        Args:
            client_socket: Socket của client
            address: Địa chỉ của client
        """
        try:
            while self.is_running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # Parse message
                try:
                    message = json.loads(data.decode('utf-8'))
                    self._process_message(message, client_socket)
                except json.JSONDecodeError:
                    print(f"Invalid JSON from {address}")
                
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
    
    def _process_message(self, message: Dict, sender_socket: socket.socket):
        """
        Xử lý message nhận được
        
        Args:
            message: Message data
            sender_socket: Socket của người gửi
        """
        message_type = message.get('type')
        if message_type in self.message_handlers:
            try:
                self.message_handlers[message_type](message, sender_socket)
            except Exception as e:
                print(f"Error processing message type {message_type}: {e}")
        else:
            print(f"Unknown message type: {message_type}")
    
    def connect_to_peer(self, address: str, port: int) -> bool:
        """
        Kết nối đến một peer
        
        Args:
            address: Địa chỉ IP của peer
            port: Port của peer
            
        Returns:
            bool: True nếu kết nối thành công
        """
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((address, port))
            
            # Gửi ping để xác nhận kết nối
            ping_message = {
                'type': 'ping',
                'from': self.node_id,
                'timestamp': time.time()
            }
            self._send_message(peer_socket, ping_message)
            
            # Thêm vào danh sách peers
            endpoint = f"{address}:{port}"
            self.peers[endpoint] = PeerInfo(
                address=address,
                port=port,
                last_seen=time.time(),
                is_connected=True
            )
            
            print(f"Connected to peer {endpoint}")
            return True
            
        except Exception as e:
            print(f"Failed to connect to peer {address}:{port}: {e}")
            return False
    
    def broadcast_message(self, message: Dict):
        """
        Phát tán message đến tất cả peers
        
        Args:
            message: Message cần phát tán
        """
        message['from'] = self.node_id
        message['timestamp'] = time.time()
        
        for endpoint, peer in self.peers.items():
            if peer.is_connected:
                try:
                    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    peer_socket.connect((peer.address, peer.port))
                    self._send_message(peer_socket, message)
                    peer_socket.close()
                except Exception as e:
                    print(f"Failed to send message to {endpoint}: {e}")
                    peer.is_connected = False
    
    def _send_message(self, sock: socket.socket, message: Dict):
        """
        Gửi message qua socket
        
        Args:
            sock: Socket để gửi
            message: Message data
        """
        data = json.dumps(message).encode('utf-8')
        sock.send(data)
    
    def discover_peers(self):
        """Khám phá peers mới từ các peers hiện có"""
        discovery_message = {
            'type': 'peer_discovery',
            'requesting_peers': True
        }
        self.broadcast_message(discovery_message)
    
    # Default message handlers
    def _handle_ping(self, message: Dict, sender_socket: socket.socket):
        """Xử lý ping message"""
        pong_response = {
            'type': 'pong',
            'from': self.node_id,
            'timestamp': time.time(),
            'original_timestamp': message.get('timestamp')
        }
        self._send_message(sender_socket, pong_response)
    
    def _handle_pong(self, message: Dict, sender_socket: socket.socket):
        """Xử lý pong message"""
        from_node = message.get('from')
        print(f"Received pong from {from_node}")
    
    def _handle_peer_discovery(self, message: Dict, sender_socket: socket.socket):
        """Xử lý peer discovery request"""
        if message.get('requesting_peers'):
            peer_list = {
                'type': 'peer_list',
                'peers': [
                    {'address': peer.address, 'port': peer.port}
                    for peer in self.peers.values()
                    if peer.is_connected
                ]
            }
            self._send_message(sender_socket, peer_list)
    
    def _handle_peer_list(self, message: Dict, sender_socket: socket.socket):
        """Xử lý peer list response"""
        peers_data = message.get('peers', [])
        for peer_data in peers_data:
            address = peer_data.get('address')
            port = peer_data.get('port')
            endpoint = f"{address}:{port}"
            
            if endpoint not in self.peers:
                print(f"Discovered new peer: {endpoint}")
                # Có thể tự động kết nối hoặc chỉ thêm vào danh sách
    
    def get_peer_count(self) -> int:
        """Lấy số lượng peers đang kết nối"""
        return sum(1 for peer in self.peers.values() if peer.is_connected)
    
    def get_peer_list(self) -> List[Dict]:
        """Lấy danh sách peers"""
        return [
            {
                'endpoint': endpoint,
                'address': peer.address,
                'port': peer.port,
                'node_id': peer.node_id,
                'last_seen': peer.last_seen,
                'is_connected': peer.is_connected
            }
            for endpoint, peer in self.peers.items()
        ]
    
    def cleanup_disconnected_peers(self):
        """Dọn dẹp các peers đã ngắt kết nối"""
        current_time = time.time()
        timeout = 300  # 5 phút
        
        disconnected = []
        for endpoint, peer in self.peers.items():
            if current_time - peer.last_seen > timeout:
                disconnected.append(endpoint)
        
        for endpoint in disconnected:
            del self.peers[endpoint]
            print(f"Removed disconnected peer: {endpoint}")

# TODO: Implement NAT traversal
# TODO: Add encryption for messages
# TODO: Implement peer reputation system
# TODO: Add bandwidth monitoring 