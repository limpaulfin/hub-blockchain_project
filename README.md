# 🔗 Hub Blockchain Project

**Dự án Tiểu Luận Cá Nhân**: Blockchain trong Quản lý Chuỗi Cung Ứng

---

## 📋 Thông tin Dự án

**Tác giả**: **TS. Nguyễn Hoài Đức**  
**Trường**: Đại học Ngân Hàng TP. Hồ Chí Minh (HUB)  
**Môn học**: Chuỗi khối trong Kinh doanh (BLB 515)  
**Đề tài**: Blockchain trong quản lý chuỗi cung ứng

---

## 🎯 Mục tiêu

1. **Nghiên cứu lý thuyết**: Phân tích các khái niệm cốt lõi của công nghệ blockchain
2. **Ứng dụng thực tế**: Triển khai mô hình blockchain cho quản lý chuỗi cung ứng
3. **Đánh giá hiệu quả**: So sánh với các hệ thống truyền thống
4. **Visualization**: Mô phỏng hoạt động của blockchain network

---

## 🏗️ Kiến trúc Hệ thống

```text
blockchain_project/
├── core/                    # Blockchain core modules
│   ├── transaction.py       # Transaction management
│   ├── block.py            # Block structure & Merkle tree
│   ├── blockchain.py       # Main blockchain logic
│   ├── node.py             # Network node management
│   └── consensus.py        # Consensus algorithms (PoW, PoS)
├── network/                # Network & communication
│   ├── p2p.py              # Peer-to-peer networking
│   ├── message.py          # Message serialization
│   └── server.py           # HTTP API server
├── utils/                  # Utility modules
│   ├── crypto.py           # Cryptographic functions
│   └── tools.py            # Helper tools & visualization
├── config.py               # Configuration management
├── main.py                 # Main application entry point
└── docs/                   # Documentation & research
```

---

## 🚀 Tính năng Chính

### Core Blockchain Features

- ✅ **Transaction Management**: Tạo, xác thực và quản lý giao dịch
- ✅ **Block Mining**: Proof of Work với độ khó điều chỉnh tự động
- ✅ **Merkle Tree**: Cấu trúc dữ liệu hiệu quả cho xác thực
- ✅ **Chain Validation**: Kiểm tra tính toàn vẹn của blockchain

### Network & P2P

- ✅ **P2P Networking**: Kết nối và giao tiếp giữa các nodes
- ✅ **Message Broadcasting**: Phát tán giao dịch và blocks
- ✅ **Peer Discovery**: Tự động khám phá các nodes mới

### Consensus Mechanisms

- ✅ **Proof of Work (PoW)**: Thuật toán khai thác truyền thống
- ✅ **Proof of Stake (PoS)**: Cơ chế đồng thuận tiết kiệm năng lượng

### Visualization & Tools

- 🎨 **Blockchain Visualizer**: Hiển thị chuỗi blocks trực quan
- 📊 **Transaction Flow**: Theo dõi luồng giao dịch
- 📈 **Mining Statistics**: Thống kê hiệu suất khai thác

---

## ⚡ Quick Start

### 1. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 2. Khởi chạy Blockchain Node

```bash
python main.py
```

### 3. Truy cập Web Interface

```
http://localhost:8080
```

### 4. Sử dụng API

```bash
# Kiểm tra trạng thái node
curl http://localhost:8080/status

# Xem blockchain
curl http://localhost:8080/blockchain

# Tạo giao dịch
curl -X POST http://localhost:8080/transaction \
  -H "Content-Type: application/json" \
  -d '{"receiver": "alice", "amount": 10}'
```

---

## 🔬 Nghiên cứu & Phân tích

### Supply Chain Use Cases

1. **Traceability**: Theo dõi nguồn gốc sản phẩm
2. **Transparency**: Minh bạch thông tin cho tất cả stakeholders
3. **Security**: Bảo mật dữ liệu với cryptographic hashing
4. **Immutability**: Tính bất biến của records

### Performance Metrics

- **Transaction Throughput**: TPS (Transactions Per Second)
- **Mining Efficiency**: Hash rate và energy consumption
- **Network Latency**: Thời gian propagation giữa nodes
- **Storage Optimization**: Blockchain size management

---

## 📊 Technical Specifications

| Component   | Technology  | Purpose                        |
| ----------- | ----------- | ------------------------------ |
| Hashing     | SHA-256     | Block và transaction integrity |
| Merkle Tree | Binary tree | Efficient verification         |
| Consensus   | PoW + PoS   | Distributed agreement          |
| Networking  | TCP/JSON    | P2P communication              |
| API         | HTTP REST   | External integration           |
| Storage     | JSON files  | Persistent blockchain data     |

---

## 🎓 Đóng góp Học thuật

Bài tiểu luận cá nhân này đóng góp:

1. **Mô hình thực tế**: Implementation hoàn chỉnh của blockchain network
2. **Phân tích so sánh**: PoW vs PoS trong môi trường supply chain
3. **Case study**: Ứng dụng cụ thể cho doanh nghiệp Việt Nam
4. **Performance evaluation**: Đánh giá hiệu suất và khả năng mở rộng

---

## 📚 Tài liệu Tham khảo

---

## 📄 License & Acknowledgments

Dự án này được phát triển cho mục đích học tập và nghiên cứu tại **Trường Đại học Ngân Hàng TP. Hồ Chí Minh**.

TS. Nguyễn Hoài Đức - Giảng viên hướng dẫn môn "Chuỗi khối trong Kinh doanh"

---

_© 2025 - Hub Blockchain Project - Đại học Ngân Hàng TP.HCM_
