import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))
    
from netmiko import ConnectHandler
from datetime import datetime
import time
from config.setting import STATIC_ROUTE_CONFIGS, DEVICE_DELAY, REPORTS_DIR
from modules.utils import (setup_logging, load_devices, get_device_info, 
                           save_results, print_header, print_summary)

logger = setup_logging('static_route_config')


def configure_static_route(device_info, route_config):
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
        
        print(f"Đang cấu hình Static Route...")
        output = connection.send_config_set(route_config)
        
        connection.save_config()
        
        print(f"Kiểm tra bảng định tuyến...")
        verify_routes = connection.send_command('show ip route static')
        routing_table = connection.send_command('show ip route')
        
        connection.disconnect()
        
        print(f"Cấu hình Static Route thành công cho {device_info['hostname']}")
        print(f"\nStatic Routes:\n{verify_routes}")
        logger.info(f"Cấu hình Static Route thành công cho {device_info['hostname']}")
        
        return {
            'status': 'SUCCESS',
            'hostname': device_info['hostname'],
            'ip': device_info['host'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'static_routes': verify_routes[:300],
            'routing_table': routing_table[:300]
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


def configure_all_static_routes():
    print_header("CẤU HÌNH STATIC ROUTE TỰ ĐỘNG")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    df_routers = df_devices[df_devices['hostname'].str.startswith('R')]
    
    if len(df_routers) == 0:
        print("Không tìm thấy Router nào trong danh sách thiết bị")
        return []
    
    print(f"\nTìm thấy {len(df_routers)} Router")
    print(f"LƯU Ý: Static Route thường được dùng thay thế cho OSPF")
    print(f"{'='*60}")
    
    results = []
    
    for index, row in df_routers.iterrows():
        device = get_device_info(row)
        route_config = STATIC_ROUTE_CONFIGS.get(row['hostname'], [])
        
        if route_config:
            result = configure_static_route(device, route_config)
            results.append(result)
            time.sleep(DEVICE_DELAY)
        else:
            print(f"Không có cấu hình Static Route cho {row['hostname']}")
            logger.warning(f"Không có cấu hình Static Route cho {row['hostname']}")
    
    if results:
        output_file = save_results(results, 'static_route_results', REPORTS_DIR)
        print(f"\nĐã xuất kết quả ra file: {output_file}")
    
    print_summary(results)
    
    return results


if __name__ == "__main__":
    configure_all_static_routes()