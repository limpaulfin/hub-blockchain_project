#!/usr/bin/env python3
"""
Blockchain HTTP Server Module
File: network/server.py
Purpose: HTTP REST API server cho blockchain node
Dependencies: core/node.py, network/p2p.py
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, Optional

class BlockchainHTTPHandler(BaseHTTPRequestHandler):
    """
    HTTP Request Handler cho blockchain API
    """
    
    def do_GET(self):
        """Xử lý GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        try:
            if path == "/":
                self._handle_root()
            elif path == "/status":
                self._handle_status()
            elif path == "/blockchain":
                self._handle_get_blockchain()
            elif path == "/balance":
                self._handle_get_balance(query_params)
            elif path == "/transactions":
                self._handle_get_transactions(query_params)
            elif path == "/peers":
                self._handle_get_peers()
            elif path == "/mining/stats":
                self._handle_mining_stats()
            else:
                self._send_error(404, "Endpoint not found")
                
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def do_POST(self):
        """Xử lý POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            # Đọc request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            if path == "/transaction":
                self._handle_create_transaction(data)
            elif path == "/mine":
                self._handle_mine_block(data)
            elif path == "/connect":
                self._handle_connect_peer(data)
            elif path == "/sync":
                self._handle_sync_blockchain()
            else:
                self._send_error(404, "Endpoint not found")
                
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def _handle_root(self):
        """Xử lý root endpoint"""
        response = {
            "message": "Blockchain Node API",
            "version": "1.0.0",
            "endpoints": [
                "GET /status - Node status",
                "GET /blockchain - Full blockchain",
                "GET /balance?address=<addr> - Get balance",
                "GET /transactions?address=<addr> - Get transactions",
                "GET /peers - Connected peers",
                "GET /mining/stats - Mining statistics",
                "POST /transaction - Create transaction",
                "POST /mine - Mine pending transactions",
                "POST /connect - Connect to peer",
                "POST /sync - Sync blockchain"
            ]
        }
        self._send_json_response(response)
    
    def _handle_status(self):
        """Xử lý status endpoint"""
        node = self.server.blockchain_node
        status = node.get_node_status()
        
        # Thêm thông tin server
        status.update({
            "server_host": self.server.server_address[0],
            "server_port": self.server.server_address[1],
            "api_version": "1.0.0"
        })
        
        self._send_json_response(status)
    
    def _handle_get_blockchain(self):
        """Xử lý get blockchain endpoint"""
        node = self.server.blockchain_node
        blockchain_data = node.blockchain.to_dict()
        self._send_json_response(blockchain_data)
    
    def _handle_get_balance(self, query_params):
        """Xử lý get balance endpoint"""
        address = query_params.get('address')
        if not address or not address[0]:
            self._send_error(400, "Missing address parameter")
            return
        
        node = self.server.blockchain_node
        balance = node.blockchain.get_balance(address[0])
        
        response = {
            "address": address[0],
            "balance": balance
        }
        self._send_json_response(response)
    
    def _handle_get_transactions(self, query_params):
        """Xử lý get transactions endpoint"""
        address = query_params.get('address')
        if not address or not address[0]:
            self._send_error(400, "Missing address parameter")
            return
        
        node = self.server.blockchain_node
        transactions = node.blockchain.get_transaction_history(address[0])
        
        response = {
            "address": address[0],
            "transactions": transactions
        }
        self._send_json_response(response)
    
    def _handle_get_peers(self):
        """Xử lý get peers endpoint"""
        # TODO: Implement peer management
        response = {
            "peers": [],
            "peer_count": 0
        }
        self._send_json_response(response)
    
    def _handle_mining_stats(self):
        """Xử lý mining stats endpoint"""
        # TODO: Implement mining statistics
        response = {
            "blocks_mined": 0,
            "hash_rate": 0,
            "difficulty": 2
        }
        self._send_json_response(response)
    
    def _handle_create_transaction(self, data):
        """Xử lý create transaction endpoint"""
        required_fields = ['receiver', 'amount']
        for field in required_fields:
            if field not in data:
                self._send_error(400, f"Missing required field: {field}")
                return
        
        try:
            node = self.server.blockchain_node
            transaction = node.create_transaction(
                receiver=data['receiver'],
                amount=data['amount'],
                data=data.get('data')
            )
            
            # Broadcast transaction
            node.broadcast_transaction(transaction)
            
            response = {
                "success": True,
                "transaction_hash": transaction.transaction_hash,
                "message": "Transaction created and broadcasted"
            }
            self._send_json_response(response)
            
        except ValueError as e:
            self._send_error(400, str(e))
        except Exception as e:
            self._send_error(500, f"Failed to create transaction: {str(e)}")
    
    def _handle_mine_block(self, data):
        """Xử lý mine block endpoint"""
        try:
            node = self.server.blockchain_node
            
            if len(node.blockchain.pending_transactions) == 0:
                self._send_error(400, "No pending transactions to mine")
                return
            
            # Mine block trong thread riêng để không block HTTP response
            mining_thread = threading.Thread(target=node.start_mining)
            mining_thread.daemon = True
            mining_thread.start()
            
            response = {
                "success": True,
                "message": "Mining started",
                "pending_transactions": len(node.blockchain.pending_transactions)
            }
            self._send_json_response(response)
            
        except Exception as e:
            self._send_error(500, f"Failed to start mining: {str(e)}")
    
    def _handle_connect_peer(self, data):
        """Xử lý connect peer endpoint"""
        if 'address' not in data or 'port' not in data:
            self._send_error(400, "Missing address or port")
            return
        
        try:
            # TODO: Implement peer connection via P2P network
            response = {
                "success": True,
                "message": f"Connected to peer {data['address']}:{data['port']}"
            }
            self._send_json_response(response)
            
        except Exception as e:
            self._send_error(500, f"Failed to connect to peer: {str(e)}")
    
    def _handle_sync_blockchain(self):
        """Xử lý sync blockchain endpoint"""
        try:
            # TODO: Implement blockchain synchronization
            response = {
                "success": True,
                "message": "Blockchain sync initiated"
            }
            self._send_json_response(response)
            
        except Exception as e:
            self._send_error(500, f"Failed to sync blockchain: {str(e)}")
    
    def _send_json_response(self, data: Dict[str, Any], status_code: int = 200):
        """
        Gửi JSON response
        
        Args:
            data: Dữ liệu để gửi
            status_code: HTTP status code
        """
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def _send_error(self, status_code: int, message: str):
        """
        Gửi error response
        
        Args:
            status_code: HTTP status code
            message: Error message
        """
        error_data = {
            "error": True,
            "status_code": status_code,
            "message": message
        }
        self._send_json_response(error_data, status_code)
    
    def log_message(self, format, *args):
        """Override để custom logging"""
        print(f"[HTTP] {format % args}")

class BlockchainHTTPServer:
    """
    HTTP Server cho blockchain node
    """
    
    def __init__(self, host: str = "localhost", port: int = 8080, blockchain_node=None):
        """
        Khởi tạo HTTP server
        
        Args:
            host: Host address
            port: Port number
            blockchain_node: Blockchain node instance
        """
        self.host = host
        self.port = port
        self.blockchain_node = blockchain_node
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
    
    def start(self):
        """Bắt đầu HTTP server"""
        try:
            self.server = HTTPServer((self.host, self.port), BlockchainHTTPHandler)
            self.server.blockchain_node = self.blockchain_node
            
            self.is_running = True
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            print(f"HTTP API Server started on http://{self.host}:{self.port}")
            print("Available endpoints:")
            print(f"  - Status: http://{self.host}:{self.port}/status")
            print(f"  - Blockchain: http://{self.host}:{self.port}/blockchain")
            
        except Exception as e:
            print(f"Failed to start HTTP server: {e}")
    
    def stop(self):
        """Dừng HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.is_running = False
            print("HTTP API Server stopped")
    
    def get_server_info(self) -> Dict[str, Any]:
        """Lấy thông tin server"""
        return {
            "host": self.host,
            "port": self.port,
            "is_running": self.is_running,
            "base_url": f"http://{self.host}:{self.port}"
        }

# TODO: Implement WebSocket support for real-time updates
# TODO: Add authentication and rate limiting
# TODO: Implement API documentation endpoint
# TODO: Add request/response logging 