import paramiko
import logging
from .fake_infra import FakeEnterprise
from datetime import datetime
import socket
import threading
from app.web_api.mongodb import MongoDB

class DecoySSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.env = FakeEnterprise()  # Fake company environment
        self.mongo = MongoDB()
        self.logger = logging.getLogger("ssh_honeypot")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.start_time = datetime.now()
        self.authenticated = False  # Track login status
        self.fake_users = {user["username"]: user["password"] for user in self.env.users}

    def check_auth_password(self, username, password):
        """Allow attackers to log in if they use any fake credentials."""
        if username in self.fake_users:
            self.authenticated = True
            status = "success" if password == self.fake_users[username] else "wrong password"
        else:
            status = "failed"

        log_entry = {
            "timestamp": datetime.now(),
            "client_ip": self.client_ip,
            "username": username,
            "password": password,
            "status": status,
            "environment": self.env.__dict__
        }

        try:
            with self.mongo.session() as sessions:
                sessions.insert_one(log_entry)
            self.logger.info(f"SSH Login Attempt: {log_entry}")
        except Exception as e:
            self.logger.error(f"Error logging SSH login attempt: {str(e)}")

        return paramiko.AUTH_SUCCESSFUL if self.authenticated else paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        """Accept channel requests to allow interaction."""
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

class SSHServer:
    def __init__(self, host='0.0.0.0', port=2222):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        
    def run(self):
        self.sock.listen(100)
        print(f"SSH honeypot running on {self.host}:{self.port}")
        
        while True:
            client, addr = self.sock.accept()
            threading.Thread(target=self.handle_client, args=(client, addr)).start()
    
    def handle_client(self, client, addr):
        """Handles incoming SSH connections."""
        transport = paramiko.Transport(client)
        transport.add_server_key(self.load_host_key())
        server = DecoySSHServer(addr[0])
        transport.start_server(server=server)
        
        channel = transport.accept(20)
        if channel:
            channel.send("Welcome to Enterprise Jumpbox v2.4\r\n")
            self.handle_shell(channel, addr[0])
    
    def handle_shell(self, channel, client_ip):
        """Simulates an interactive shell for the attacker."""
        self.logger.info(f"[+] Attacker {client_ip} accessed shell.")
        channel.send("$ ")  # Fake shell prompt
        
        try:
            while True:
                command = channel.recv(1024).decode().strip()
                if not command:
                    continue

                log_entry = {
                    "timestamp": datetime.now(),
                    "client_ip": client_ip,
                    "command": command
                }

                try:
                    with self.mongo.commands() as command_logs:
                        command_logs.insert_one(log_entry)
                    self.logger.info(f"[!] {client_ip} executed: {command}")
                except Exception as e:
                    self.logger.error(f"Error logging command: {str(e)}")

                # Respond with fake output
                response = self.fake_command_response(command)
                channel.send(response.encode() + b"\n$ ")
                
                if command in ["exit", "logout"]:
                    break
        except Exception as e:
            self.logger.error(f"Shell session error: {str(e)}")

        channel.close()

def fake_command_response(self, command):
    """Generates fake command responses to make the honeypot believable."""
    fake_responses = {
        "whoami": "admin",
        "id": "uid=0(root) gid=0(root) groups=0(root)",
        "uname -a": "Linux jumpbox 5.15.0-67-generic #74-Ubuntu SMP x86_64",
        "ls": "config.txt  logs/  scripts/  tmp/",
        "pwd": "/home/admin",
        "cat /etc/passwd": "root:x:0:0:root:/root:/bin/bash\nadmin:x:1000:1000::/home/admin:/bin/bash"
    }
    return fake_responses.get(command, "command not found")