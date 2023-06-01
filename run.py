import requests
import socket
from urllib.parse import urlparse
import concurrent.futures

def validate_server(server):
    server = server.strip()  # 去除首尾的空格和换行符
    server = server.encode('idna').decode()  # 使用idna进行编码解码

    if server.startswith('udp://'):
        return validate_udp_server(server)
    elif server.startswith('http://') or server.startswith('https://'):
        return validate_http_server(server)
    else:
        print(f"无法解析的服务器地址：{server}")
        return None

def validate_http_server(server):
    try:
        response = requests.get(server)
        if response.status_code == 200:
            print(f"HTTP服务器 {server} 连接成功")
            return server
    except requests.exceptions.RequestException:
        print(f"HTTP服务器 {server} 连接失败")
    return None

def validate_udp_server(server):
    server_url = urlparse(server)
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.settimeout(5)  # 设置超时时间为5秒
        udp_socket.connect((server_url.hostname, server_url.port))
        udp_socket.close()
        print(f"UDP服务器 {server} 连接成功")
        return server
    except (socket.error, socket.timeout):
        print(f"UDP服务器 {server} 连接失败")
    return None

# 读取bt.txt文件，获取服务器清单并去除空行和重复项
with open('C:\\Workspace\\py\\bt\\bt.txt', 'r', encoding='utf-8') as file:
    servers_list = file.read().replace(',', '\n').splitlines()
    servers_list = [server.strip() for server in servers_list if server.strip()]  # 去除空行

# 验证服务器有效性并实时返回连接结果
alive_servers_list = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(validate_server, servers_list)
    for result in results:
        if result is not None:
            alive_servers_list.append(result)

str = ','.join(alive_servers_list)
print(str)

# 将有效服务器写入bt_alive.txt文件
with open('bt_alive.txt', 'w', encoding='utf-8') as file:
    file.write(str)

print(f"操作完成")