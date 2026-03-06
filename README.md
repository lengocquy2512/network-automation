# Network Automation

Dự án này xây dựng hệ thống **tự động hóa cấu hình và giám sát mạng**
bằng Python. Chương trình hỗ trợ cấu hình nhiều thiết bị mạng Cisco
thông qua **Netmiko** và cung cấp các chức năng:

-   Cấu hình VLAN cho switch
-   Cấu hình IP interface cho router
-   Cấu hình OSPF
-   Cấu hình static route
-   Backup và restore cấu hình thiết bị
-   Giám sát trạng thái thiết bị và mạng
-   Xuất log và báo cáo tự động

------------------------------------------------------------------------

# 1. Mục tiêu dự án

Dự án nhằm:

-   Giảm thao tác cấu hình thủ công
-   Tăng tính nhất quán trong cấu hình thiết bị
-   Hỗ trợ backup và khôi phục khi có sự cố
-   Giám sát trạng thái mạng
-   Phục vụ học tập và thực hành mạng Cisco / GNS3

------------------------------------------------------------------------

# 2. Chức năng chính

## 2.1 Cấu hình thiết bị

Hệ thống hỗ trợ cấu hình tự động:

-   VLAN trên switch
-   IP interface trên router
-   OSPF routing
-   Static route

Ngoài ra có chế độ:

**Full Configuration** -- chạy toàn bộ quy trình cấu hình.

------------------------------------------------------------------------

## 2.2 Backup và Restore

Hệ thống hỗ trợ:

-   Backup cấu hình thiết bị
-   Restore cấu hình từ file backup
-   Mô phỏng lỗi cấu hình
-   Tự động khôi phục cấu hình
-   Xem danh sách file backup

------------------------------------------------------------------------

## 2.3 Giám sát thiết bị

Các chức năng giám sát gồm:

-   Kiểm tra kết nối thiết bị
-   Trạng thái interface
-   Bảng định tuyến
-   Thông tin VLAN
-   Trạng thái OSPF
-   Giám sát toàn hệ thống

------------------------------------------------------------------------

# 3. Công nghệ sử dụng

-   Python
-   Netmiko
-   Pandas
-   Logging
-   CSV
-   Pathlib

------------------------------------------------------------------------

# 4. Cấu trúc thư mục

    network-automation/
    │
    ├── config/
    │   ├── devices.csv
    │   └── setting.py
    │
    ├── logs/
    │
    ├── main/
    │   └── main.py
    │
    ├── modules/
    │   ├── backup_restore.py
    │   ├── ip_config.py
    │   ├── monitoring.py
    │   ├── ospf_config.py
    │   ├── static_route_config.py
    │   ├── utils.py
    │   └── vlan_config.py
    │
    ├── reports/
    │   └── backups/
    │
    └── Mohinhmang.gns3

------------------------------------------------------------------------

# 5. Ý nghĩa các module

### main/main.py

File điều khiển trung tâm của hệ thống. Chứa menu chính để chọn các chức
năng:

-   cấu hình thiết bị
-   backup / restore
-   monitoring
-   thông tin hệ thống

### config/setting.py

Chứa các cấu hình hệ thống:

-   đường dẫn thư mục logs / reports / backups
-   file danh sách thiết bị
-   các lệnh cấu hình VLAN
-   các lệnh cấu hình IP
-   các lệnh OSPF
-   các lệnh static route

### modules/

Các module chức năng:

-   **vlan_config.py** -- cấu hình VLAN
-   **ip_config.py** -- cấu hình IP router
-   **ospf_config.py** -- cấu hình OSPF
-   **static_route_config.py** -- cấu hình static route
-   **backup_restore.py** -- backup và restore cấu hình
-   **monitoring.py** -- giám sát thiết bị
-   **utils.py** -- các hàm tiện ích chung

------------------------------------------------------------------------

# 6. Danh sách thiết bị

Danh sách thiết bị được lưu trong:

    config/devices.csv

File này chứa:

-   hostname
-   ip
-   device_type
-   username
-   password

------------------------------------------------------------------------

# 7. Mô hình mạng

File mô hình:

    Mohinhmang.gns3

Hệ thống gồm:

-   3 Router (R1, R2, R3)
-   3 Switch (Switch1, Switch2, Switch3)

### VLAN

Các VLAN được cấu hình:

-   VLAN 10
-   VLAN 20
-   VLAN 99

### IP Network

Một số dải mạng sử dụng:

-   192.168.10.0/24
-   192.168.20.0/24
-   10.10.10.0/24
-   10.10.20.0/24
-   10.20.10.0/24
-   10.20.20.0/24
-   10.0.1.0/30
-   10.0.2.0/30

------------------------------------------------------------------------

# 8. Cài đặt môi trường

### Tạo môi trường ảo

    python -m venv venv

### Kích hoạt môi trường

Windows:

    venv\Scripts\Activate.ps1

Linux / MacOS:

    source venv/bin/activate

### Cài thư viện

    pip install netmiko pandas

------------------------------------------------------------------------

# 9. Chạy chương trình

Chạy file:

    python main/main.py

Sau đó hệ thống sẽ hiển thị menu chức năng.

------------------------------------------------------------------------

# 10. Kết quả đầu ra

Chương trình tạo:

-   log trong thư mục `logs/`
-   báo cáo trong `reports/`
-   backup cấu hình trong `reports/backups/`

------------------------------------------------------------------------

# 11. Điểm nổi bật

-   Tự động hóa cấu hình mạng
-   Thiết kế module rõ ràng
-   Có backup và restore
-   Có hệ thống monitoring
-   Dễ mở rộng thêm chức năng

------------------------------------------------------------------------

# 12. Hướng phát triển

Có thể mở rộng:

-   giao diện web
-   hỗ trợ nhiều vendor
-   đọc cấu hình từ YAML / JSON
-   gửi cảnh báo email / telegram
-   dashboard giám sát mạng

------------------------------------------------------------------------

# 13. Tác giả

**Le Ngoc Quy**
