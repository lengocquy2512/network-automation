import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from netmiko import ConnectHandler
from datetime import datetime
import time
from config.setting import IP_CONFIGS, DEVICE_DELAY, REPORTS_DIR
from modules.utils import (setup_logging, load_devices, get_device_info, 
                           save_results, print_header, print_summary)

logger = setup_logging('ip_config')


def configure_ip_interface(device_info, ip_config):
    try:
        print(f"\n{'-'*60}")
        print(f"Đang kết nối tới {device_info['hostname']} ({device_info['host']})...")
        logger.info(f"Kết nối tới {device_info['hostname']}")
        
        connection_params = {
            'device_type': device_info['device_type'],
            'host': device_info['host'],
            'username': device_info['username'],
            'password': device_info['password']
        }
        
        connection = ConnectHandler(**connection_params)
        prompt = connection.find_prompt()
        print(f"Kết nối thành công! Prompt: {prompt}")
        
        print(f"Đang cấu hình IP Interface...")
        output = connection.send_config_set(ip_config)
        
        connection.save_config()
        
        print(f"Kiểm tra cấu hình IP...")
        verify_output = connection.send_command('show ip interface brief')
        
        connection.disconnect()
        
        print(f"Cấu hình IP thành công cho {device_info['hostname']}")
        print(f"\nTrạng thái Interface:\n{verify_output}")
        logger.info(f"Cấu hình IP thành công cho {device_info['hostname']}")
        
        return {
            'status': 'SUCCESS',
            'hostname': device_info['hostname'],
            'ip': device_info['host'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'verification': verify_output[:300]
        }
        
    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        print(f"Lỗi khi cấu hình {device_info['hostname']}: {error_msg}")
        logger.error(f"Lỗi khi cấu hình {device_info['hostname']}: {error_msg}")
        
        return {
            'status': 'ERROR',
            'hostname': device_info['hostname'],
            'ip': device_info['host'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': error_msg
        }


def configure_all_ip_interfaces():
    print_header("CẤU HÌNH IP INTERFACE TỰ ĐỘNG")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    print(f"\nTìm thấy {len(df_devices)} thiết bị")
    print(f"{'-'*60}")
    
    results = []
    
    for index, row in df_devices.iterrows():
        device = get_device_info(row)
        ip_config = IP_CONFIGS.get(row['hostname'], [])
        
        if ip_config:
            result = configure_ip_interface(device, ip_config)
            results.append(result)
            time.sleep(DEVICE_DELAY)
        else:
            print(f"Không có cấu hình IP cho {row['hostname']}")
            logger.warning(f"Không có cấu hình IP cho {row['hostname']}")
    
    if results:
        output_file = save_results(results, 'ip_config_results', REPORTS_DIR)
        print(f"\nĐã xuất kết quả ra file: {output_file}")
    
    print_summary(results)
    
    return results


if __name__ == "__main__":
    configure_all_ip_interfaces()