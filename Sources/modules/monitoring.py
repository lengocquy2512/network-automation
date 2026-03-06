import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from netmiko import ConnectHandler
from datetime import datetime
import time
from config.setting import DEVICE_DELAY, REPORTS_DIR
from modules.utils import (setup_logging, load_devices, get_device_info, 
                           save_results, print_header, print_summary,
                           display_menu, confirm_action)

logger = setup_logging('monitoring')


def check_device_connectivity():
    print_header("KIỂM TRA KẾT NỐI THIẾT BỊ")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    print(f"\nĐang kiểm tra kết nối tới {len(df_devices)} thiết bị...\n")
    
    results = []
    
    for index, row in df_devices.iterrows():
        device = get_device_info(row)
        hostname = row['hostname']
        ip = row['ip']
        
        try:
            print(f"{'='*70}")
            print(f" Đang kiểm tra {hostname} ({ip})...")
            
            start_time = time.time()
            
            connection_params = {
                'device_type': device['device_type'],
                'host': device['host'],
                'username': device['username'],
                'password': device['password']
            }
            
            connection = ConnectHandler(**connection_params)
            prompt = connection.find_prompt()
            
            version_output = connection.send_command('show version | include IOS')
            uptime_output = connection.send_command('show version | include uptime')
            
            connection.disconnect()
            
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            print(f" Kết nối THÀNH CÔNG!")
            print(f"  Prompt: {prompt}")
            print(f"  IOS Version: {version_output.strip()}")
            print(f"  Uptime: {uptime_output.strip()}")
            print(f"  Response Time: {response_time}s")
            
            logger.info(f"Kết nối thành công tới {hostname}")
            
            results.append({
                'status': 'SUCCESS',
                'hostname': hostname,
                'ip': ip,
                'prompt': prompt,
                'response_time': response_time,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            error_msg = str(e)
            print(f" Kết nối THẤT BẠI!")
            print(f"  Lỗi: {error_msg}")
            
            logger.error(f"Không thể kết nối tới {hostname}: {error_msg}")
            
            results.append({
                'status': 'ERROR',
                'hostname': hostname,
                'ip': ip,
                'error': error_msg,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        time.sleep(DEVICE_DELAY)
    
    if results:
        output_file = save_results(results, 'connectivity_check', REPORTS_DIR)
        print(f"\n Đã lưu báo cáo: {output_file}")
    
    print_summary(results, "KẾT QUẢ KIỂM TRA KẾT NỐI")
    
    return results


def show_interface_status():
    print_header("TRẠNG THÁI INTERFACE")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    results = []
    
    for index, row in df_devices.iterrows():
        device = get_device_info(row)
        hostname = row['hostname']
        
        try:
            print(f"\n{'='*70}")
            print(f" {hostname} - INTERFACE STATUS")
            print(f"{'='*70}")
            
            connection_params = {
                'device_type': device['device_type'],
                'host': device['host'],
                'username': device['username'],
                'password': device['password']
            }
            
            connection = ConnectHandler(**connection_params)
            
            if 'Switch' in hostname:
                int_status = connection.send_command('show interfaces status')
                int_brief = connection.send_command('show ip interface brief')
            else:
                int_brief = connection.send_command('show ip interface brief')
                int_status = connection.send_command('show interfaces description')
            
            connection.disconnect()
            
            print(f"\n IP Interface Brief:")
            print(int_brief)
            
            print(f"\n Interface Status/Description:")
            print(int_status)
            
            up_count = int_brief.count('up')
            down_count = int_brief.count('down')
            
            print(f"\n Thống kê:")
            print(f"   UP: {up_count}")
            print(f"   DOWN: {down_count}")
            
            logger.info(f"Đã kiểm tra interface của {hostname}")
            
            results.append({
                'status': 'SUCCESS',
                'hostname': hostname,
                'ip': device['host'],
                'up_interfaces': up_count,
                'down_interfaces': down_count,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            error_msg = str(e)
            print(f" Lỗi khi kiểm tra {hostname}: {error_msg}")
            logger.error(f"Lỗi khi kiểm tra interface {hostname}: {error_msg}")
            
            results.append({
                'status': 'ERROR',
                'hostname': hostname,
                'ip': device['host'],
                'error': error_msg,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        time.sleep(DEVICE_DELAY)
    
    if results:
        output_file = save_results(results, 'interface_status', REPORTS_DIR)
        print(f"\n Đã lưu báo cáo: {output_file}")
    
    print_summary(results, "KẾT QUẢ KIỂM TRA INTERFACE")
    
    return results


def show_routing_table():
    print_header("BẢNG ĐỊNH TUYẾN")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    df_routers = df_devices[df_devices['hostname'].str.startswith('R')]
    
    if len(df_routers) == 0:
        print("Không tìm thấy Router nào")
        return []
    
    results = []
    
    for index, row in df_routers.iterrows():
        device = get_device_info(row)
        hostname = row['hostname']
        
        try:
            print(f"\n{'='*70}")
            print(f"  {hostname} - ROUTING TABLE")
            print(f"{'='*70}")
            
            connection_params = {
                'device_type': device['device_type'],
                'host': device['host'],
                'username': device['username'],
                'password': device['password']
            }
            
            connection = ConnectHandler(**connection_params)
            
            routing_table = connection.send_command('show ip route')
            
            route_summary = connection.send_command('show ip route summary')
            
            connection.disconnect()
            
            print(f"\n Routing Table:")
            print(routing_table)
            
            print(f"\n Route Summary:")
            print(route_summary)
            
            logger.info(f"Đã kiểm tra routing table của {hostname}")
            
            results.append({
                'status': 'SUCCESS',
                'hostname': hostname,
                'ip': device['host'],
                'routes': routing_table[:500],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            error_msg = str(e)
            print(f" Lỗi khi kiểm tra {hostname}: {error_msg}")
            logger.error(f"Lỗi khi kiểm tra routing table {hostname}: {error_msg}")
            
            results.append({
                'status': 'ERROR',
                'hostname': hostname,
                'ip': device['host'],
                'error': error_msg,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        time.sleep(DEVICE_DELAY)
    
    if results:
        output_file = save_results(results, 'routing_table', REPORTS_DIR)
        print(f"\n Đã lưu báo cáo: {output_file}")
    
    print_summary(results, "KẾT QUẢ KIỂM TRA ROUTING TABLE")
    
    return results


def show_vlan_info():
    print_header("THÔNG TIN VLAN")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    df_switches = df_devices[df_devices['hostname'].str.contains('Switch', case=False)]
    
    if len(df_switches) == 0:
        print("Không tìm thấy Switch nào")
        return []
    
    results = []
    
    for index, row in df_switches.iterrows():
        device = get_device_info(row)
        hostname = row['hostname']
        
        try:
            print(f"\n{'='*70}")
            print(f"  {hostname} - VLAN INFORMATION")
            print(f"{'='*70}")
            
            connection_params = {
                'device_type': device['device_type'],
                'host': device['host'],
                'username': device['username'],
                'password': device['password']
            }
            
            connection = ConnectHandler(**connection_params)
            
            vlan_brief = connection.send_command('show vlan brief')
            vlan_summary = connection.send_command('show vlan summary')
            trunk_info = connection.send_command('show interfaces trunk')
            
            connection.disconnect()
            
            print(f"\n VLAN Brief:")
            print(vlan_brief)
            
            print(f"\n VLAN Summary:")
            print(vlan_summary)
            
            print(f"\n Trunk Interfaces:")
            print(trunk_info)
            
            logger.info(f"Đã kiểm tra VLAN của {hostname}")
            
            results.append({
                'status': 'SUCCESS',
                'hostname': hostname,
                'ip': device['host'],
                'vlan_info': vlan_brief[:300],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            error_msg = str(e)
            print(f" Lỗi khi kiểm tra {hostname}: {error_msg}")
            logger.error(f"Lỗi khi kiểm tra VLAN {hostname}: {error_msg}")
            
            results.append({
                'status': 'ERROR',
                'hostname': hostname,
                'ip': device['host'],
                'error': error_msg,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        time.sleep(DEVICE_DELAY)
    
    if results:
        output_file = save_results(results, 'vlan_info', REPORTS_DIR)
        print(f"\n Đã lưu báo cáo: {output_file}")
    
    print_summary(results, "KẾT QUẢ KIỂM TRA VLAN")
    
    return results


def show_ospf_status():
    print_header("TRẠNG THÁI OSPF")
    
    df_devices = load_devices()
    if df_devices is None:
        return []
    
    df_routers = df_devices[df_devices['hostname'].str.startswith('R')]
    
    if len(df_routers) == 0:
        print("Không tìm thấy Router nào")
        return []
    
    results = []
    
    for index, row in df_routers.iterrows():
        device = get_device_info(row)
        hostname = row['hostname']
        
        try:
            print(f"\n{'='*70}")
            print(f" {hostname} - OSPF STATUS")
            print(f"{'='*70}")
            
            connection_params = {
                'device_type': device['device_type'],
                'host': device['host'],
                'username': device['username'],
                'password': device['password']
            }
            
            connection = ConnectHandler(**connection_params)
            
            ospf_neighbor = connection.send_command('show ip ospf neighbor')
            ospf_interface = connection.send_command('show ip ospf interface brief')
            ospf_database = connection.send_command('show ip ospf database')
            
            connection.disconnect()
            
            print(f"\n OSPF Neighbors:")
            print(ospf_neighbor)
            
            print(f"\n OSPF Interfaces:")
            print(ospf_interface)
            
            print(f"\n OSPF Database Summary:")

            database_lines = ospf_database.split('\n')[:20]
            print('\n'.join(database_lines))
            
            neighbor_count = ospf_neighbor.count('FULL')
            
            print(f"\n Thống kê:")
            print(f"   OSPF Neighbors (FULL): {neighbor_count}")
            
            logger.info(f"Đã kiểm tra OSPF của {hostname}")
            
            results.append({
                'status': 'SUCCESS',
                'hostname': hostname,
                'ip': device['host'],
                'neighbor_count': neighbor_count,
                'neighbors': ospf_neighbor[:300],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            error_msg = str(e)
            print(f" Lỗi khi kiểm tra {hostname}: {error_msg}")
            logger.error(f"Lỗi khi kiểm tra OSPF {hostname}: {error_msg}")
            
            results.append({
                'status': 'ERROR',
                'hostname': hostname,
                'ip': device['host'],
                'error': error_msg,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        time.sleep(DEVICE_DELAY)
    
    if results:
        output_file = save_results(results, 'ospf_status', REPORTS_DIR)
        print(f"\n Đã lưu báo cáo: {output_file}")
    
    print_summary(results, "KẾT QUẢ KIỂM TRA OSPF")
    
    return results


def monitor_all_devices():
    print_header("GIÁM SÁT TOÀN DIỆN HỆ THỐNG")
    
    print("\n Bắt đầu quá trình giám sát toàn diện...")
    print("Quá trình này sẽ kiểm tra:")
    print("  1. Kết nối thiết bị")
    print("  2. Trạng thái Interface")
    print("  3. Bảng định tuyến (Router)")
    print("  4. Thông tin VLAN (Switch)")
    print("  5. Trạng thái OSPF (Router)")
    
    if not confirm_action("\nBạn có muốn tiếp tục?"):
        print(" Đã hủy")
        return
    
    print(f"\n{'='*70}")
    print("BƯỚC 1/5: Kiểm tra kết nối thiết bị")
    print(f"{'='*70}")
    conn_results = check_device_connectivity()
    input("\nNhấn Enter để tiếp tục bước tiếp theo...")
    
    print(f"\n{'='*70}")
    print("BƯỚC 2/5: Kiểm tra trạng thái Interface")
    print(f"{'='*70}")
    int_results = show_interface_status()
    input("\nNhấn Enter để tiếp tục bước tiếp theo...")
    
    print(f"\n{'='*70}")
    print("BƯỚC 3/5: Kiểm tra bảng định tuyến")
    print(f"{'='*70}")
    route_results = show_routing_table()
    input("\nNhấn Enter để tiếp tục bước tiếp theo...")
    
    print(f"\n{'='*70}")
    print("BƯỚC 4/5: Kiểm tra cấu hình VLAN")
    print(f"{'='*70}")
    vlan_results = show_vlan_info()
    input("\nNhấn Enter để tiếp tục bước cuối...")
    
    print(f"\n{'='*70}")
    print("BƯỚC 5/5: Kiểm tra trạng thái OSPF")
    print(f"{'='*70}")
    ospf_results = show_ospf_status()
    
    print(f"\n{'='*70}")
    print("  HOÀN TẤT QUÁ TRÌNH GIÁM SÁT TOÀN DIỆN")
    print(f"{'='*70}")
    print(f"\nTổng kết:")
    print(f"   Kiểm tra kết nối: {len(conn_results)} thiết bị")
    print(f"   Kiểm tra interface: {len(int_results)} thiết bị")
    print(f"   Kiểm tra routing: {len(route_results)} router")
    print(f"   Kiểm tra VLAN: {len(vlan_results)} switch")
    print(f"   Kiểm tra OSPF: {len(ospf_results)} router")
    print(f"\nTất cả báo cáo đã được lưu trong thư mục: {REPORTS_DIR}")
    print(f"{'='*70}")


def monitoring_menu():
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


if __name__ == "__main__":
    monitoring_menu()