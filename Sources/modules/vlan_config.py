import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))
    
from netmiko import ConnectHandler
from datetime import datetime
import time
from config.setting import VLAN_CONFIGS, DEVICE_DELAY, REPORTS_DIR
from modules.utils import (setup_logging, load_devices, get_device_info, 
                           save_results, print_header, print_summary)

logger = setup_logging('vlan_config')


def configure_vlan(device_info, vlan_config):
    try:
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
        print(f"\nKết nối thành công! Prompt: {prompt}")
        
        print(f"Đang cấu hình VLAN...")
        output = connection.send_config_set(vlan_config)
        
        connection.save_config()
        
        print(f"Kiểm tra cấu hình VLAN...")
        verify_output = connection.send_command('show vlan brief')
        
        connection.disconnect()
        
        print(f"Cấu hình VLAN thành công cho {device_info['hostname']}")
        print(f"\nVLAN Summary:\n{verify_output}")
        logger.info(f"Cấu hình VLAN thành công cho {device_info['hostname']}")
        
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


def configure_all_vlans():
    print_header("CẤU HÌNH VLAN TỰ ĐỘNG")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    df_switches = df_devices[df_devices['hostname'].str.contains('Switch', case=False)]
    
    if len(df_switches) == 0:
        print("Không tìm thấy Switch nào trong danh sách thiết bị")
        return []
    
    print(f"Tìm thấy {len(df_switches)} Switch")
    print(f"{'-'*60}")
    
    results = []
    
    for index, row in df_switches.iterrows():
        device = get_device_info(row)
        vlan_config = VLAN_CONFIGS.get(row['hostname'], [])
        
        if vlan_config:
            result = configure_vlan(device, vlan_config)
            results.append(result)
            time.sleep(DEVICE_DELAY)
        else:
            print(f"Không có cấu hình VLAN cho {row['hostname']}")
            logger.warning(f"Không có cấu hình VLAN cho {row['hostname']}")
    
    if results:
        output_file = save_results(results, 'vlan_config_results', REPORTS_DIR)
        print(f"\nĐã xuất kết quả ra file: {output_file}")
    
    print_summary(results)
    
    return results


if __name__ == "__main__":
    configure_all_vlans()

