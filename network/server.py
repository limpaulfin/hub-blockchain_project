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
    
    def __init__(self, blockchain, p2p_network, *args, **kwargs):
        self.blockchain = blockchain
        self.p2p_network = p2p_network
        super().__init__(*args, **kwargs)

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
        status = {
            "blocks": len(self.blockchain.chain),
            "pending_transactions": len(self.blockchain.pending_transactions),
            "difficulty": self.blockchain.difficulty,
            "is_valid": self.blockchain.is_chain_valid(),
            "peers": len(self.p2p_network.peers) if self.p2p_network else 0,
        }
        self._send_json_response(status)
    
    def _handle_get_blockchain(self):
        """Xử lý get blockchain endpoint"""
        blockchain_data = [block.to_dict() for block in self.blockchain.chain]
        self._send_json_response(blockchain_data)
    
    def _handle_get_balance(self, query_params):
        """Xử lý get balance endpoint"""
        address = query_params.get('address')
        if not address or not address[0]:
            self._send_error(400, "Missing address parameter")
            return
        
        balance = self.blockchain.get_balance(address[0])
        
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
        
        transactions = self.blockchain.get_transaction_history(address[0])
        
        response = {
            "address": address[0],
            "transactions": transactions
        }
        self._send_json_response(response)
    
    def _handle_get_peers(self):
        """Xử lý get peers endpoint"""
        peers = self.p2p_network.get_peer_list() if self.p2p_network else []
        response = {
            "peers": peers,
            "peer_count": len(peers)
        }
        self._send_json_response(response)
    
    def _handle_mining_stats(self):
        """Xử lý mining stats endpoint"""
        response = {
            "blocks_mined": 0,
            "hash_rate": 0,
            "difficulty": self.blockchain.difficulty
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
            # Note: This is simplified. In reality, you'd get the sender from auth.
            # Here we assume the node owner is the sender.
            # A real app needs a wallet management system accessible here.
            tx = self.blockchain.new_transaction(
                sender="node_owner_address", # Placeholder
                receiver=data['receiver'],
                amount=data['amount']
            )
            
            # Broadcast transaction
            if self.p2p_network:
                self.p2p_network.broadcast_transaction(tx) # Assuming tx object is what's needed
            
            response = {
                "success": True,
                "transaction_hash": tx.hash, # Assuming tx object has a hash
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
            if len(self.blockchain.pending_transactions) == 0:
                self._send_error(400, "No pending transactions to mine")
                return
            
            # This should be asynchronous in a real application
            miner_address = data.get("miner_address", "network_reward_address")
            new_block = self.blockchain.mine_block(miner_address)
            
            if self.p2p_network:
                self.p2p_network.broadcast_block(new_block)

            response = {
                "success": True,
                "message": "New block mined",
                "block": new_block.to_dict()
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
            if self.p2p_network:
                self.p2p_network.connect_to_peer(data['address'], data['port'])
            
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
            if self.p2p_network:
                self.p2p_network.sync_chain() # Assuming this method exists

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
        return

class BlockchainHTTPServer:
    """
    Lớp wrapper cho HTTP server
    """
    def __init__(self, server_address, blockchain, p2p_network):
        self.server_address = server_address
        self.blockchain = blockchain
        self.p2p_network = p2p_network
        
        def handler(*args, **kwargs):
            return BlockchainHTTPHandler(self.blockchain, self.p2p_network, *args, **kwargs)
            
        self.http_server = HTTPServer(self.server_address, handler)
        self.server_thread = None
        
    def serve_forever(self):
        """Bắt đầu HTTP server"""
        print(f"HTTP Server serving forever at {self.server_address}")
        self.http_server.serve_forever()

    def shutdown(self):
        """Dừng HTTP server"""
        if self.http_server:
            print("Shutting down HTTP server...")
            self.http_server.shutdown()
            self.http_server.server_close()
            print("HTTP Server stopped.")

def create_server(host: str = "localhost", port: int = 8080, blockchain=None, p2p_network=None) -> BlockchainHTTPServer:
    """
    Tạo instance của BlockchainHTTPServer
    """
    if blockchain is None:
        raise ValueError("Blockchain instance is required")
    
    return BlockchainHTTPServer((host, port), blockchain, p2p_network)

# TODO: Add authentication for sensitive endpoints
# TODO: Implement rate limiting
# TODO: Add more detailed logging
# TODO: Improve error handling and response consistency

# TODO: Implement WebSocket support for real-time updates
# TODO: Add authentication and rate limiting
# TODO: Implement API documentation endpoint
# TODO: Add request/response logging 