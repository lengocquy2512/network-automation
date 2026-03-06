import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from modules.utils import print_header, display_menu, confirm_action
from datetime import datetime

try:
    from modules.backup_restore import (
        backup_all_devices, 
        restore_device, 
        simulate_and_restore, 
        list_backups
    )
    BACKUP_MODULE = True
except ImportError as e:
    print(f"Cảnh báo: Không thể import backup_restore module: {e}")
    BACKUP_MODULE = False

try:
    from modules.vlan_config import configure_all_vlans
    VLAN_MODULE = True
except ImportError as e:
    print(f"Cảnh báo: Không thể import vlan_config module: {e}")
    VLAN_MODULE = False

try:
    from modules.ip_config import configure_all_ip_interfaces
    IP_MODULE = True
except ImportError as e:
    print(f"Cảnh báo: Không thể import ip_config module: {e}")
    IP_MODULE = False

try:
    from modules.ospf_config import configure_all_ospf
    OSPF_MODULE = True
except ImportError as e:
    print(f"Cảnh báo: Không thể import ospf_config module: {e}")
    OSPF_MODULE = False

try:
    from modules.static_route_config import configure_all_static_routes
    STATIC_ROUTE_MODULE = True
except ImportError as e:
    print(f"Cảnh báo: Không thể import static_route_config module: {e}")
    STATIC_ROUTE_MODULE = False

try:
    from modules.monitoring import (
        check_device_connectivity,
        show_interface_status,
        show_routing_table,
        show_vlan_info,
        show_ospf_status,
        monitor_all_devices
    )
    MONITORING_MODULE = True
except ImportError as e:
    print(f"Cảnh báo: Không thể import monitoring module: {e}")
    MONITORING_MODULE = False
def show_welcome():
    print("\n" + "="*70)
    print(" "*20 + "NETWORK AUTOMATION SYSTEM")
    print(" "*15 + "Hệ thống tự động hóa cấu hình mạng")
    print("="*70)
    print(f"Thời gian khởi động: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

def configuration_menu():
    while True:
        print_header("MENU CẤU HÌNH THIẾT BỊ")
        
        menu_options = {}
        option_num = 1
        
        if VLAN_MODULE:
            menu_options[str(option_num)] = "   Cấu hình VLAN (Switch)"
            option_num += 1
        
        if IP_MODULE:
            menu_options[str(option_num)] = "   Cấu hình IP Interface (Router)"
            option_num += 1
        
        if OSPF_MODULE:
            menu_options[str(option_num)] = "   Cấu hình OSPF Routing"
            option_num += 1
        
        if STATIC_ROUTE_MODULE:
            menu_options[str(option_num)] = "   Cấu hình Static Route"
            option_num += 1
        
        menu_options['9'] = "   Cấu hình tất cả (Full Configuration)"
        menu_options['0'] = "   Quay lại menu chính"
        
        choice = display_menu(menu_options)
        
        if choice == '0':
            break
        elif choice == '1' and VLAN_MODULE:
            configure_all_vlans()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '2' and IP_MODULE:
            configure_all_ip_interfaces()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '3' and OSPF_MODULE:
            configure_all_ospf()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '4' and STATIC_ROUTE_MODULE:
            configure_all_static_routes()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '9':
            full_configuration()
            input("\nNhấn Enter để tiếp tục...")
        else:
            print("Lựa chọn không hợp lệ hoặc module chưa được cài đặt")
            input("\nNhấn Enter để tiếp tục...")


def backup_restore_menu():
    if not BACKUP_MODULE:
        print("\nModule Backup & Restore chưa được cài đặt")
        input("\nNhấn Enter để tiếp tục...")
        return
        
    while True:
        print_header("MENU BACKUP & RESTORE")
        
        menu_options = {
            '1': 'Backup cấu hình tất cả thiết bị',
            '2': 'Restore cấu hình từ file backup',
            '3': 'Mô phỏng lỗi và tự động khôi phục',
            '4': 'Xem danh sách file backup',
            '0': 'Quay lại menu chính'
        }
        
        choice = display_menu(menu_options)
        
        if choice == '0':
            break
        elif choice == '1':
            backup_all_devices()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '2':
            restore_device()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '3':
            simulate_and_restore()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '4':
            list_backups()
            input("\nNhấn Enter để tiếp tục...")
        else:
            print("Lựa chọn không hợp lệ")
            input("\nNhấn Enter để tiếp tục...")


def monitoring_menu():
    if not MONITORING_MODULE:
        print("\n Module Monitoring chưa được cài đặt")
        print("Vui lòng đảm bảo file monitoring.py đã được tạo trong thư mục modules/")
        input("\nNhấn Enter để tiếp tục...")
        return
        
    while True:
        print_header("MENU GIÁM SÁT THIẾT BỊ")
        
        menu_options = {
            '1': ' Kiểm tra kết nối thiết bị',
            '2': ' Xem trạng thái Interface',
            '3': ' Xem bảng định tuyến (Router)',
            '4': ' Xem cấu hình VLAN (Switch)',
            '5': ' Xem trạng thái OSPF (Router)',
            '6': ' Giám sát toàn diện (All-in-One)',
            '0': ' Quay lại menu chính'
        }
        
        choice = display_menu(menu_options)
        
        if choice == '0':
            break
        elif choice == '1':
            check_device_connectivity()
            input("\n Nhấn Enter để tiếp tục...")
        elif choice == '2':
            show_interface_status()
            input("\n Nhấn Enter để tiếp tục...")
        elif choice == '3':
            show_routing_table()
            input("\n Nhấn Enter để tiếp tục...")
        elif choice == '4':
            show_vlan_info()
            input("\n Nhấn Enter để tiếp tục...")
        elif choice == '5':
            show_ospf_status()
            input("\n Nhấn Enter để tiếp tục...")
        elif choice == '6':
            monitor_all_devices()
            input("\n Nhấn Enter để tiếp tục...")
        else:
            print(" Lựa chọn không hợp lệ")
            input("\nNhấn Enter để tiếp tục...")


def full_configuration():
    print_header("CẤU HÌNH ĐẦY ĐỦ TOÀN BỘ HỆ THỐNG")
    
    print("\n  CẢNH BÁO:")
    print("Chức năng này sẽ thực hiện:")
    print("  1  Cấu hình VLAN trên tất cả Switch")
    print("  2  Cấu hình IP Interface trên tất cả Router")
    print("  3  Cấu hình OSPF Routing Protocol")
    print("  4  Backup cấu hình sau khi hoàn tất")
    print("\n   Thời gian dự kiến: 5-10 phút")
    
    if not confirm_action("\n  Bạn có chắc muốn tiếp tục?"):
        print(" Đã hủy thao tác")
        return
    
    print("\n" + "="*70)
    print(" BẮT ĐẦU QUY TRÌNH CẤU HÌNH TỰ ĐỘNG")
    print("="*70)
    
    if VLAN_MODULE:
        print("\n BƯỚC 1/4: Cấu hình VLAN trên Switch")
        print("-"*70)
        configure_all_vlans()
        print("\n Hoàn tất bước 1")
        input("\nNhấn Enter để tiếp tục bước tiếp theo...")
    else:
        print("\n  Bỏ qua: Module VLAN chưa cài đặt")
    
    if IP_MODULE:
        print("\n BƯỚC 2/4: Cấu hình IP Interface trên Router")
        print("-"*70)
        configure_all_ip_interfaces()
        print("\n Hoàn tất bước 2")
        input("\nNhấn Enter để tiếp tục bước tiếp theo...")
    else:
        print("\n  Bỏ qua: Module IP Config chưa cài đặt")
    
    if OSPF_MODULE:
        print("\n BƯỚC 3/4: Cấu hình OSPF Routing Protocol")
        print("-"*70)
        configure_all_ospf()
        print("\n Hoàn tất bước 3")
        input("\nNhấn Enter để tiếp tục bước cuối...")
    else:
        print("\n  Bỏ qua: Module OSPF chưa cài đặt")
    
    if BACKUP_MODULE:
        print("\n BƯỚC 4/4: Backup cấu hình toàn bộ hệ thống")
        print("-"*70)
        backup_all_devices()
        print("\n Hoàn tất bước 4")
    else:
        print("\n  Bỏ qua: Module Backup chưa cài đặt")
    
    print("\n" + "="*70)
    print(" HOÀN TẤT QUY TRÌNH CẤU HÌNH ĐẦY ĐỦ")
    print(" Hệ thống đã được cấu hình thành công!")
    print("="*70)


def system_info():
    print_header("THÔNG TIN HỆ THỐNG")
    
    print("\n Modules đã cài đặt:")
    print(f"   VLAN Configuration: {' Sẵn sàng' if VLAN_MODULE else ' Chưa cài đặt'}")
    print(f"   IP Interface Configuration: {' Sẵn sàng' if IP_MODULE else ' Chưa cài đặt'}")
    print(f"   OSPF Configuration: {' Sẵn sàng' if OSPF_MODULE else ' Chưa cài đặt'}")
    print(f"   Static Route Configuration: {' Sẵn sàng' if STATIC_ROUTE_MODULE else ' Chưa cài đặt'}")
    print(f"   Backup & Restore: {' Sẵn sàng' if BACKUP_MODULE else ' Chưa cài đặt'}")
    
    print("\n Cấu trúc thư mục dự án:")
    print(f"   Base Directory: {BASE_DIR}")
    print(f"   Reports: {BASE_DIR / 'reports'}")
    print(f"   Logs: {BASE_DIR / 'logs'}")
    print(f"   Backups: {BASE_DIR / 'reports' / 'backups'}")
    print(f"   Config: {BASE_DIR / 'config'}")
    
    print("\n Thông tin phiên bản:")
    print("   Version: 1.0.0")
    print("   Release Date: 2025")
    print("   Python Version: 3.x")
    
    print("\n Thông tin người phát triển:")
    print("   Tác giả:Lê Ngọc Quy")
    
    print(f"\n Thời gian hiện tại: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main_menu():
    show_welcome()
    
    while True:
        print_header("MENU CHÍNH")
        
        menu_options = {
            '1': ' Cấu hình thiết bị',
            '2': ' Backup & Restore',
            '3': ' Giám sát thiết bị',
            '4': ' Thông tin hệ thống',
            '0': ' Thoát chương trình'
        }
        
        choice = display_menu(menu_options)
        
        if choice == '1':
            configuration_menu()
        elif choice == '2':
            backup_restore_menu()
        elif choice == '3':
            monitoring_menu()
        elif choice == '4':
            system_info()
            input("\n Nhấn Enter để tiếp tục...")
        elif choice == '0':
            print("\n" + "="*70)
            if confirm_action("  Bạn có chắc muốn thoát không?"):
                print("\n Cảm ơn bạn đã sử dụng Network Automation System!")
                print(" Thời gian kết thúc: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print(" Hẹn gặp lại!")
                print("="*70 + "\n")
                break
        else:
            print("\n Lựa chọn không hợp lệ")
            input("\nNhấn Enter để tiếp tục...")


def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n  Chương trình bị gián đoạn bởi người dùng (Ctrl+C)")
        print(" Tạm biệt!")
    except Exception as e:
        print(f"\n Lỗi nghiêm trọng: {str(e)}")
        print("Vui lòng kiểm tra lại cấu hình và thử lại")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()