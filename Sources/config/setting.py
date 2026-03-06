from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

REPORTS_DIR = BASE_DIR / 'reports'
LOGS_DIR = BASE_DIR / 'logs'
BACKUPS_DIR = REPORTS_DIR / 'backups'
CONFIG_DIR = BASE_DIR / 'config'

DEVICES_FILE = CONFIG_DIR / 'devices.csv'

CONNECTION_TIMEOUT = 30
DEVICE_DELAY = 1  

VLAN_CONFIGS = {
    'Switch1': [
        'vlan 10',
        'name VLAN_10',
        'exit',
        'vlan 20',
        'name VLAN_20',
        'exit',
        'interface e0/0',
        'switchport trunk encapsulation dot1q',
        'switchport mode trunk',
        'switchport trunk allowed vlan 10,20,99',
        'exit',
        'interface e0/2',
        'switchport mode access',
        'switchport access vlan 10',
        'exit',
        'interface e0/3',
        'switchport mode access',
        'switchport access vlan 20',
        'exit'
    ],
    'Switch2': [
        'vlan 10',
        'name VLAN_10',
        'exit',
        'vlan 20',
        'name VLAN_20',
        'exit',
        'interface e0/0',
        'switchport trunk encapsulation dot1q',
        'switchport mode trunk',
        'switchport trunk allowed vlan 10,20,99',
        'exit',
        'interface e0/1',
        'switchport mode access',
        'switchport access vlan 10',
        'exit',
        'interface e0/2',
        'switchport mode access',
        'switchport access vlan 20',
        'exit'
    ],
    'Switch3': [
        'vlan 10',
        'name VLAN_10',
        'exit',
        'vlan 20',
        'name VLAN_20',
        'exit',
        'interface e0/0',
        'switchport trunk encapsulation dot1q',
        'switchport mode trunk',
        'switchport trunk allowed vlan 10,20,99',
        'exit',
        'interface e0/1',
        'switchport mode access',
        'switchport access vlan 10',
        'exit',
        'interface e0/2',
        'switchport mode access',
        'switchport access vlan 20',
        'exit'
    ]
}

IP_CONFIGS = {
    'R1': [
        'interface g0/0',
        'no shutdown',
        'exit',
        'interface g0/0.10',
        'encapsulation dot1q 10',
        'ip address 192.168.10.1 255.255.255.0',
        'exit',
        'interface g0/0.20',
        'encapsulation dot1q 20',
        'ip address 192.168.20.1 255.255.255.0',
        'exit',
        'interface g1/0',
        'ip address 10.0.1.1 255.255.255.252',
        'no shutdown',
        'exit',
        'interface g2/0',
        'ip address 10.0.2.1 255.255.255.252',
        'no shutdown',
        'exit'
    ],
    'R2': [
        'interface g1/0',
        'ip address 10.0.1.2 255.255.255.252',
        'no shutdown',
        'exit',
        'interface g0/0',
        'no shutdown',
        'exit',
        'interface g0/0.10',
        'encapsulation dot1q 10',
        'ip address 10.10.10.1 255.255.255.0',
        'exit',
        'interface g0/0.20',
        'encapsulation dot1q 20',
        'ip address 10.10.20.1 255.255.255.0',
        'exit'
    ],
    'R3': [
        'interface g2/0',
        'ip address 10.0.2.2 255.255.255.252',
        'no shutdown',
        'exit',
        'interface g0/0',
        'no shutdown',
        'exit',
        'interface g0/0.10',
        'encapsulation dot1q 10',
        'ip address 10.20.10.1 255.255.255.0',
        'exit',
        'interface g0/0.20',
        'encapsulation dot1q 20',
        'ip address 10.20.20.1 255.255.255.0',
        'exit'
    ]
}

OSPF_CONFIGS = {
    'R1': [
        'router ospf 1',
        'router-id 1.1.1.1',
        'network 192.168.1.0 0.0.0.255 area 0',
        'network 192.168.10.0 0.0.0.255 area 0',
        'network 192.168.20.0 0.0.0.255 area 0',
        'network 10.0.1.0 0.0.0.3 area 0',
        'network 10.0.2.0 0.0.0.3 area 0',
        'exit'
    ],
    'R2': [
        'router ospf 1',
        'router-id 2.2.2.2',
        'network 192.168.2.0 0.0.0.255 area 0',
        'network 10.10.10.0 0.0.0.255 area 0',
        'network 10.10.20.0 0.0.0.255 area 0',
        'network 10.0.1.0 0.0.0.3 area 0',
        'exit'
    ],
    'R3': [
        'router ospf 1',
        'router-id 3.3.3.3',
        'network 192.168.3.0 0.0.0.255 area 0',
        'network 10.20.10.0 0.0.0.255 area 0',
        'network 10.20.20.0 0.0.0.255 area 0',
        'network 10.0.2.0 0.0.0.3 area 0',
        'exit'
    ]
}

STATIC_ROUTE_CONFIGS = {
    'R1': [
        'ip route 192.168.2.0 255.255.255.0 10.0.1.2',
        'ip route 10.10.10.0 255.255.255.0 10.0.1.2',
        'ip route 10.10.20.0 255.255.255.0 10.0.1.2',
        'ip route 192.168.3.0 255.255.255.0 10.0.2.2',
        'ip route 10.20.10.0 255.255.255.0 10.0.2.2',
        'ip route 10.20.20.0 255.255.255.0 10.0.2.2'
    ],
    'R2': [
        'ip route 192.168.1.0 255.255.255.0 10.0.1.1',
        'ip route 192.168.10.0 255.255.255.0 10.0.1.1',
        'ip route 192.168.20.0 255.255.255.0 10.0.1.1',
        'ip route 192.168.3.0 255.255.255.0 10.0.1.1',
        'ip route 10.20.10.0 255.255.255.0 10.0.1.1',
        'ip route 10.20.20.0 255.255.255.0 10.0.1.1',
        'ip route 10.0.2.0 255.255.255.252 10.0.1.1'
    ],
    'R3': [
        'ip route 192.168.1.0 255.255.255.0 10.0.2.1',
        'ip route 192.168.10.0 255.255.255.0 10.0.2.1',
        'ip route 192.168.20.0 255.255.255.0 10.0.2.1',
        'ip route 192.168.2.0 255.255.255.0 10.0.2.1',
        'ip route 10.10.10.0 255.255.255.0 10.0.2.1',
        'ip route 10.10.20.0 255.255.255.0 10.0.2.1',
        'ip route 10.0.1.0 255.255.255.252 10.0.2.1'
    ]
}

def create_directories():
    for directory in [REPORTS_DIR, LOGS_DIR, BACKUPS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

create_directories()