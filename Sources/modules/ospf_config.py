import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from netmiko import ConnectHandler
from datetime import datetime
import time
from config.setting import OSPF_CONFIGS, DEVICE_DELAY, REPORTS_DIR
from modules.utils import (setup_logging, load_devices, get_device_info, 
                           save_results, print_header, print_summary)

logger = setup_logging('ospf_config')


def configure_ospf(device_info, ospf_config):
    try:
        print(f"\n{'='*60}")
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
        
        print(f"Đang cấu hình OSPF...")
        output = connection.send_config_set(ospf_config)
        
        connection.save_config()
        
        print(f"Chờ OSPF thiết lập neighbor... (10 giây)")
        time.sleep(10)
        
        print(f"Kiểm tra cấu hình OSPF...")
        verify_ospf = connection.send_command('show ip ospf neighbor')
        verify_routes = connection.send_command('show ip route ospf')
        
        connection.disconnect()
        
        print(f"Cấu hình OSPF thành công cho {device_info['hostname']}")
        print(f"\nOSPF Neighbors:\n{verify_ospf}")
        print(f"\nOSPF Routes:\n{verify_routes[:300]}...")
        logger.info(f"Cấu hình OSPF thành công cho {device_info['hostname']}")
        
        return {
            'status': 'SUCCESS',
            'hostname': device_info['hostname'],
            'ip': device_info['host'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ospf_neighbors': verify_ospf[:200],
            'ospf_routes': verify_routes[:200]
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


def configure_all_ospf():
    print_header("CẤU HÌNH OSPF TỰ ĐỘNG")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    df_routers = df_devices[df_devices['hostname'].str.startswith('R')]
    
    if len(df_routers) == 0:
        print("Không tìm thấy Router nào trong danh sách thiết bị")
        return []
    
    print(f"\nTìm thấy {len(df_routers)} Router")
    print(f"{'-'*60}")
    
    results = []
    
    for index, row in df_routers.iterrows():
        device = get_device_info(row)
        ospf_config = OSPF_CONFIGS.get(row['hostname'], [])
        
        if ospf_config:
            result = configure_ospf(device, ospf_config)
            results.append(result)
            time.sleep(DEVICE_DELAY)
        else:
            print(f"Không có cấu hình OSPF cho {row['hostname']}")
            logger.warning(f"Không có cấu hình OSPF cho {row['hostname']}")
    
    if results:
        output_file = save_results(results, 'ospf_config_results', REPORTS_DIR)
        print(f"\nĐã xuất kết quả ra file: {output_file}")
    
    print_summary(results)
    
    return results


if __name__ == "__main__":
    configure_all_ospf()