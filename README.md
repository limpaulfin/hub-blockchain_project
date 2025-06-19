# 🔗 Hub Blockchain Project

**Dự án**: Blockchain

---

## 📋 Thông tin Dự án

**Tác giả**: **TS. Nguyễn Hoài Đức**  
**Trường**: Đại học Ngân Hàng TP. Hồ Chí Minh (HUB)  
**Môn học**: Chuỗi khối trong Kinh doanh (BLB 515)

---

## 🎯 Mục tiêu

1. **Nghiên cứu lý thuyết**: Phân tích các khái niệm cốt lõi của công nghệ blockchain
2. **Visualization**: Mô phỏng hoạt động của blockchain network

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

### 1. Cài đặt môi trường ảo và Dependencies

```bash
# Tạo môi trường ảo (chỉ lần đầu)
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

Ứng dụng hoạt động thông qua giao diện dòng lệnh (CLI). Xem chi tiết các lệnh bên dưới.

---

## ⌨️ Giao diện Dòng lệnh (Command-Line Interface)

### 1. Tổng quan

Hệ thống được điều khiển bằng các lệnh trực tiếp qua terminal, thay vì menu tương tác. Cú pháp chung là:
`python3 main.py [LỆNH] [THAM SỐ]...`

### 2. Sơ đồ quy trình làm việc (Workflow Diagram)

Sơ đồ sau minh họa quy trình làm việc phổ biến khi sử dụng CLI:

```text
(Bắt đầu)
    |
    v
+---------------------+      +---------------------+      +---------------------+
| 1. Tạo Ví           |----->| 2. Thực hiện        |----->| 3. Đào khối         |
| `create-wallet`     |      |    Giao dịch        |      | `mine`              |
|                     |      | `transaction`       |      |                     |
+---------------------+      +---------------------+      +---------------------+
    |         ^                        |                             |
    |         |                        v                             |
    |         |        +------------------------------+              |
    |         |        |   Giao dịch được thêm vào    |              |
    |         |        |   Mempool (Vùng chờ)         |              |
    |         |        +------------------------------+              |
    v         |                                                      v
+---------------------+      +---------------------+      +---------------------+
| 4. Kiểm tra Ví      |----->| 5. Kiểm tra Chuỗi   |----->| 6. Kiểm tra Trạng   |
| `wallets`           |      | `chain`             |      |  thái `status`      |
|                     |      |                     |      |                     |
+---------------------+      +---------------------+      +---------------------+
    ^                                                            |
    |                                                            v
    +-------------------------------------------------------(Kết thúc)

```

### 3. Danh sách các lệnh và Ví dụ

#### a. Tạo ví mới

Tạo một ví điện tử mới để gửi và nhận coin.

- **Lệnh**: `create-wallet <tên_ví>`
- **Ví dụ**:
  ```bash
  python3 main.py create-wallet alice
  ```
- **Output minh họa**:
  ```text
  ✅ Wallet 'alice' created / Đã tạo ví 'alice': 1ff885687389fe196c7f755d423672b4a
  💾 Blockchain and wallets saved. / Đã lưu chuỗi khối và ví.
  ```

#### b. Liệt kê các ví

Hiển thị danh sách tất cả các ví đã được tạo.

- **Lệnh**: `wallets`
- **Ví dụ**:
  ```bash
  python3 main.py wallets
  ```
- **Output minh họa**:
  ```text
  Wallets / Các ví:
    - alice: 1ff885687389fe196c7f755d423672b4a
    - bob: 13442883b3911b72764e137a51a0d7d9c
  ```

#### c. Tạo giao dịch

Tạo một giao dịch mới và đưa vào vùng chờ (mempool) để được đào.

- **Lệnh**: `transaction <ví_gửi> <ví_nhận> <số_lượng>`
- **Ví dụ**:
  ```bash
  python3 main.py transaction alice bob 50
  ```
- **Output minh họa**:
  ```text
  ✅ Transaction added to local mempool. / Đã thêm giao dịch vào mempool cục bộ.
  💾 Blockchain and wallets saved. / Đã lưu chuỗi khối và ví.
  ```

#### d. Đào khối mới

Gom tất cả các giao dịch đang chờ trong mempool vào một khối mới và đào khối đó (Proof of Work).

- **Lệnh**: `mine`
- **Tùy chọn**: `--wallet <tên_ví>` (Chỉ định ví nhận phần thưởng, mặc định là `miner`)
- **Ví dụ**:
  ```bash
  python3 main.py mine --wallet my_miner_wallet
  ```
- **Output minh họa**:
  ```text
  ⛏️  Mining a new block... (reward to: my_miner_wallet) / Đang đào khối mới... (thưởng cho: my_miner_wallet)
  🎉 New block #1 mined successfully! / Đã đào xong khối mới #1!
  .------------------------------------------------------------------------------.
  | Block #1                                                                     |
  ...
  | Transactions / Giao dịch:                                                    |
  |   1. From: 1ff8856873... / To: 13442883b3... / Amount: 50.0                  |
  |   2. From: System Reward / To: 1062226db9... / Amount: 10.0                  |
  '------------------------------------------------------------------------------'
  ```

#### e. Hiển thị chuỗi khối

In ra toàn bộ các khối trong blockchain một cách trực quan.

- **Lệnh**: `chain`
- **Ví dụ**:
  ```bash
  python3 main.py chain
  ```

#### f. Hiển thị trạng thái

Cung cấp thông tin tổng quan về blockchain tại thời điểm hiện tại.

- **Lệnh**: `status`
- **Ví dụ**:
  ```bash
  python3 main.py status
  ```
- **Output minh họa**:
  ```text
  ============================================================
  📊 BLOCKCHAIN STATUS / TRẠNG THÁI CHUỖI KHỐI
  ============================================================
    - Total Blocks / Tổng số khối:         2
    - Current Difficulty / Độ khó hiện tại:   2
    - Pending Transactions / Giao dịch chờ: 0
    - Chain valid / Chuỗi hợp lệ:          True
  ============================================================
  ```

#### g. Chạy Node Server

Khởi động node ở chế độ máy chủ, lắng nghe kết nối từ các node khác (P2P) và cung cấp API (HTTP).

- **Lệnh**: `server`
- **Ví dụ**:
  ```bash
  python3 main.py server
  ```
- **Output minh họa**:
  ```text
  P2P Server started on localhost:8000
  HTTP server running on http://localhost:8080
  Press Ctrl+C to shut down. / Nhấn Ctrl+C để tắt.
  ```

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
2. **Phân tích so sánh**: So sánh hiệu quả giữa PoW và PoS
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
