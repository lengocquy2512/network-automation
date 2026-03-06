import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))
    
import pandas as pd
from datetime import datetime
import logging
from config.setting import DEVICES_FILE, LOGS_DIR

def setup_logging(module_name):
    log_file = LOGS_DIR / f"{module_name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(module_name)


def load_devices():
    try:
        df = pd.read_csv(DEVICES_FILE)
        return df
    except FileNotFoundError:
        print(f" Không tìm thấy file {DEVICES_FILE}")
        return None
    except Exception as e:
        print(f" Lỗi khi đọc file devices: {str(e)}")
        return None


def get_device_info(row):
    device_info = {
        'device_type': row['device_type'],
        'host': row['ip'],
        'username': row['username'],
        'password': row['password']
    }
    
    device_info['hostname'] = row['hostname']
    
    return device_info


def save_results(results, filename_prefix, output_dir):
    df = pd.DataFrame(results)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f"{filename_prefix}_{timestamp}.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    return str(output_file)


def print_header(title):
    print("\n" + "-"*60)
    print(title)
    print("-"*60)
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)


def print_summary(results, title="TỔNG KẾT"):
    success = sum(1 for r in results if r.get('status') == 'SUCCESS')
    failed = len(results) - success
    
    print(f"\n{'-'*60}")
    print(title)
    print(f"{'-'*60}")
    print(f"Tổng số thiết bị: {len(results)}")
    print(f"Thành công: {success}")
    print(f"Thất bại: {failed}")
    print(f"Thời gian kết thúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'-'*60}\n")


def filter_devices(df, device_type=None, hostname_pattern=None):
    filtered = df.copy()
    
    if device_type:
        filtered = filtered[filtered['device_type'].str.contains(device_type, case=False)]
    
    if hostname_pattern:
        filtered = filtered[filtered['hostname'].str.contains(hostname_pattern, case=False)]
    
    return filtered


def confirm_action(message):
    response = input(f"{message} (y/n): ").strip().lower()
    return response == 'y'


def display_menu(options):
    print("\n" + "-"*60)
    print("MENU CHỨC NĂNG:")
    for key, value in options.items():
        print(f"{key}. {value}")
    print("-"*60)
    
    return input("Nhập lựa chọn: ").strip()