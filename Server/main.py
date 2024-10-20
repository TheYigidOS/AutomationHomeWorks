import socket
import json
from zeroconf import ServiceInfo, Zeroconf


HOST = '0.0.0.0'  
PORT = 12345      

DeviceIP = "127.0.0.1"


def MdnsService():
    zeroconf = Zeroconf()

    
    ip_bytes = socket.inet_aton(DeviceIP)

    
    service_info = ServiceInfo(
        "_http._tcp.local.",            
        "yigitServer._http._tcp.local.",  
        addresses=[ip_bytes],           
        port=PORT,                      
        properties={},                  
        server="yigitServer.local."     
    )

    
    zeroconf.register_service(service_info)
    print("mDNS service registered as 'yigitServer.local'")
    return zeroconf

def handle_command(command, nums):
    
    num1, num2 = map(int, nums.split('#'))

    
    if command == "ADD":
        return num1 + num2
    elif command == "SUBTRACT":
        return num1 - num2
    else:
        return "Unknown Command"

def start_server():
    
    zeroconf = MdnsService()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening on {HOST}:{PORT}")
            
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024).decode('utf-8')
                    message = json.loads(data)
                    command = message.get("Command")
                    nums = message.get("Nums")
                    result = handle_command(command, nums)

                    
                    response = json.dumps({"Result": result})
                    conn.sendall(response.encode('utf-8'))
    finally:
        zeroconf.close()

if __name__ == "__main__":
    start_server()
