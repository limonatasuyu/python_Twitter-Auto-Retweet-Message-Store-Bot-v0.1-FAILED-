import subprocess
import socket
import os

proxy_index = 3
auth_index = 4

PROXIES = [
    # PROXY_IP_ADDRESSES
]

PROXY_AUTHS = [
 # PROXY PASSWORD AND USERNAMES
]

PROXY_HOST = PROXIES[proxy_index]["IP"]
PROXY_PORT = PROXIES[proxy_index]["PORT"]

PROXY_USER = PROXY_AUTHS[auth_index][0]
PROXY_PASS = PROXY_AUTHS[auth_index][1]


class MITMProxy:
    def __init__(self):
        self.proxy_process = None
        self.proxy_port = self.find_available_port()

    def find_available_port(self):
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.bind(('127.0.0.1', 0))
        _, port = temp_socket.getsockname()
        temp_socket.close()
        return port

    def start_proxy(self):
        base_command = "mitmdump"
        proxy_port_option = f"-p {self.proxy_port}"
        upstream_options = f"--mode upstream:http://{PROXY_HOST}:{PROXY_PORT} --upstream-auth {PROXY_USER}:{PROXY_PASS}"
        connection_strategy_option = "--set connection_strategy=lazy"

        module_path = os.path.abspath(__file__)
        module_directory = os.path.dirname(module_path)

        script_option = f"-s {module_directory}/interceptor.py"

        command = f"{base_command} {proxy_port_option} {upstream_options} {connection_strategy_option} {script_option}"
        self.proxy_process = subprocess.Popen(command, shell=True)

    def stop_proxy(self):
        if self.proxy_process and self.proxy_process.poll() is None:
            self.proxy_process.terminate()
            self.proxy_process.wait()
