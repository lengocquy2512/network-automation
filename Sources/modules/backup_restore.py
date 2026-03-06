import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from netmiko import ConnectHandler
from datetime import datetime
import time
import os
import glob
from config.setting import DEVICE_DELAY, REPORTS_DIR, BACKUPS_DIR
from modules.utils import (setup_logging, load_devices, get_device_info, 
                           save_results, print_header, print_summary, 
                           confirm_action, display_menu)

logger = setup_logging('backup')

def backup_all_devices():
    print_header("BACKUP TẤT CẢ THIẾT BỊ")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    results = []
    for index, row in df_devices.iterrows():
        device = get_device_info(row)
        result = backup_config(device)
        results.append(result)
        time.sleep(DEVICE_DELAY)
    
    if results:
        report_file = save_results(results, 'backup_report', REPORTS_DIR)
        print(f"\nHoàn tất backup {len(results)} thiết bị")
        print(f"Báo cáo: {report_file}")
    
    print_summary(results)
    return results

def restore_device():
    df_devices = load_devices()
    if df_devices is None:
        return
    
    print(f"\n{'='*60}")
    print("DANH SÁCH THIẾT BỊ:")
    for idx, row in df_devices.iterrows():
        print(f"{idx+1}. {row['hostname']} ({row['ip']})")
    
    device_idx = input("\nNhập số thứ tự thiết bị: ").strip()
    try:
        device_idx = int(device_idx) - 1
        selected_device = df_devices.iloc[device_idx]
    except:
        print("Lựa chọn không hợp lệ")
        return
    
    backup_files = glob.glob(str(BACKUPS_DIR / f"{selected_device['hostname']}_backup_*.txt"))
    
    if not backup_files:
        print(f"Không tìm thấy file backup cho {selected_device['hostname']}")
        return
    
    backup_files.sort(reverse=True)
    print(f"\nDANH SÁCH BACKUP CỦA {selected_device['hostname']}:")
    for idx, bf in enumerate(backup_files[:5]):
        file_time = os.path.getmtime(bf)
        print(f"{idx+1}. {os.path.basename(bf)} - {datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')}")
    
    backup_idx = input("\nNhập số thứ tự file backup (1 = mới nhất): ").strip()
    try:
        backup_idx = int(backup_idx) - 1
        selected_backup = backup_files[backup_idx]
    except:
        print("Lựa chọn không hợp lệ")
        return
    
    if confirm_action(f"Bạn có chắc muốn restore {selected_device['hostname']}?"):
        device = get_device_info(selected_device)
        restore_config(device, selected_backup)

def simulate_and_restore():
    print_header("MÔ PHỎNG LỖI VÀ TỰ ĐỘNG KHÔI PHỤC")
    
    df_devices = load_devices()
    if df_devices is None:
        return
    
    routers = df_devices[df_devices['hostname'].str.startswith('R')]
    if len(routers) == 0:
        print("Không tìm thấy Router nào")
        return
    
    target_router = routers.iloc[0]
    device = get_device_info(target_router)
    
    print(f"\nThiết bị được chọn: {target_router['hostname']}")
    
    print(f"\n{'='*60}")
    print("BƯỚC 1: BACKUP CẤU HÌNH HIỆN TẠI")
    backup_result = backup_config(device)
    
    if backup_result['status'] != 'SUCCESS':
        print("Backup thất bại, không thể tiếp tục")
        return
    
    backup_file = backup_result['backup_file']
    input("\nNhấn Enter để tiếp tục mô phỏng lỗi...")
    
    print(f"\n{'='*60}")
    print("BƯỚC 2: MÔ PHỎNG LỖI")
    simulate_error(device)
    
    print("\nChờ 5 giây trước khi khôi phục...")
    time.sleep(5)
    
    print(f"\n{'='*60}")
    print("BƯỚC 3: TỰ ĐỘNG KHÔI PHỤC CẤU HÌNH")
    restore_config(device, backup_file)
    
    print(f"\n{'='*60}")
    print("HOÀN TẤT QUY TRÌNH MÔ PHỎNG VÀ KHÔI PHỤC")
    print(f"{'='*60}")


def backup_config(device_info):
    try:
        print(f"\n{'='*60}")
        print(f"Đang backup {device_info['hostname']} ({device_info['host']})...")
        logger.info(f"Bắt đầu backup {device_info['hostname']}")
        
        connection_params = {
            'device_type': device_info['device_type'],
            'host': device_info['host'],
            'username': device_info['username'],
            'password': device_info['password']
        }
        
        connection = ConnectHandler(**connection_params)
        
        running_config = connection.send_command('show running-config')
        connection.disconnect()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = BACKUPS_DIR / f"{device_info['hostname']}_backup_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(running_config)
        
        file_size = os.path.getsize(filename)
        
        print(f"  Backup thành công!")
        print(f"  File: {filename}")
        print(f"  Kích thước: {file_size} bytes")
        logger.info(f"Backup thành công {device_info['hostname']} - {file_size} bytes")
        
        return {
            'status': 'SUCCESS',
            'hostname': device_info['hostname'],
            'ip': device_info['host'],
            'backup_file': str(filename),
            'file_size': file_size,
            'timestamp': timestamp
        }
        
    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        print(f"Lỗi khi backup {device_info['hostname']}: {error_msg}")
        logger.error(f"Lỗi khi backup {device_info['hostname']}: {error_msg}")
        
        return {
            'status': 'ERROR',
            'hostname': device_info['hostname'],
            'ip': device_info['host'],
            'error': error_msg
        }


def restore_config(device_info, backup_file):
    try:
        print(f"\n{'='*60}")
        print(f"Đang restore {device_info['hostname']} từ {backup_file}...")
        logger.info(f"Bắt đầu restore {device_info['hostname']} từ {backup_file}")
        
        with open(backup_file, 'r') as f:
            config_lines = f.readlines()
        
        clean_config = []
        skip_lines = ['!', 'Building configuration', 'Current configuration', 
                     'version', 'boot-start-marker', 'boot-end-marker']
        
        for line in config_lines:
            line = line.strip()
            if line and not any(skip in line for skip in skip_lines):
                clean_config.append(line)
        
        connection_params = {
            'device_type': device_info['device_type'],
            'host': device_info['host'],
            'username': device_info['username'],
            'password': device_info['password']
        }
        
        connection = ConnectHandler(**connection_params)
        
        print(f"Đang áp dụng cấu hình...")
        batch_size = 20
        for i in range(0, len(clean_config), batch_size):
            batch = clean_config[i:i+batch_size]
            try:
                connection.send_config_set(batch)
            except:
                pass  
        
        connection.save_config()
        connection.disconnect()
        
        print(f"Restore thành công!")
        logger.info(f"Restore thành công {device_info['hostname']}")
        return {
            'status': 'SUCCESS',
            'hostname': device_info['hostname'],
            'ip': device_info['host'],
            'restored_from': backup_file
        }
        
    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        print(f"Lỗi khi restore {device_info['hostname']}: {error_msg}")
        logger.error(f"Lỗi khi restore {device_info['hostname']}: {error_msg}")
        
        return {
            'status': 'ERROR',
            'hostname': device_info['hostname'],
            'ip': device_info['host'],
            'error': error_msg
        }

def list_backups():
    print_header("DANH SÁCH FILE BACKUP")
    
    backup_files = glob.glob(str(BACKUPS_DIR / "*_backup_*.txt"))
    backup_files.sort(reverse=True)
    
    if not backup_files:
        print("Không có file backup nào")
    else:
        print(f"\nTổng số file backup: {len(backup_files)}\n")
        for bf in backup_files[:20]:
            file_size = os.path.getsize(bf)
            file_time = os.path.getmtime(bf)
            print(f"📄 {os.path.basename(bf)}")
            print(f"   Kích thước: {file_size} bytes")
            print(f"   Thời gian: {datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')}\n")

def simulate_error(device_info):
    try:
        print(f"\n{'='*60}")
        print(f"MÔ PHỎNG LỖI: Xóa cấu hình subinterface trên {device_info['hostname']}...")
        logger.warning(f"Mô phỏng lỗi trên {device_info['hostname']}")
        
        connection_params = {
            'device_type': device_info['device_type'],
            'host': device_info['host'],
            'username': device_info['username'],
            'password': device_info['password']
        }
        
        connection = ConnectHandler(**connection_params)
        connection.send_config_set(['interface g0/0.20',
                                    'no ip address 192.168.20.1 255.255.255.0'
                                    ])
        connection.save_config()
        
        int_table = connection.send_command('show ip interface brief')
        connection.disconnect()
        
        print(f"Đã mô phỏng lỗi (xóa subinterface g0/0.20)")
        print(f"Interface table sau khi xóa:")
        print(int_table[:1000] + "...")
        
        return True
        
    except Exception as e:
        print(f"Lỗi khi mô phỏng: {str(e)}")
        return False

def backup_restore_menu():
    print_header("CHƯƠNG TRÌNH BACKUP VÀ RESTORE CẤU HÌNH")
    
    menu_options = {
        '1': 'Backup cấu hình tất cả thiết bị',
        '2': 'Restore cấu hình từ file backup',
        '3': 'Mô phỏng lỗi và tự động khôi phục',
        '4': 'Xem danh sách file backup',
        '0': 'Thoát'
    }
    
    while True:
        choice = display_menu(menu_options)
        
        if choice == '1':
            backup_all_devices()
        elif choice == '2':
            restore_device()
        elif choice == '3':
            simulate_and_restore()
        elif choice == '4':
            list_backups()
        elif choice == '0':
            print("\nTạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ")


if __name__ == "__main__":
    backup_restore_menu()