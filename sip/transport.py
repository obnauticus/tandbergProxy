import socket

def open_socket(params):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((params['lh'], 0))
    s.connect((params['rh'], params['rp']))
    params['socket'] = s
    
def close_socket(params):
    s = params['socket']
    s.close()
    params['socket'] = None
    
def send_tcp(params, message):
    s= params['socket']
    s.sendall(message.encode())

def recv_tcp(params):
    s= params['socket']
    data = s.recv(4096)
    if data == '':
        raise RuntimeError("socket connection broken")
    return data.decode('utf-8')

def server(params, handle):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((params['lh'], 5060))
    print('listen {} 5060'.format(params['lh']))
    s.listen(1)
    conn, addr = s.accept()
    print ('Connected by', addr)
    params['conn'] = conn
    while 1:
        data = conn.recv(4096)
        if not data: 
            print ("no data")
            break
        res = handle(params, data.decode('utf-8'))
        if res != '':
            conn.sendall(res.encode())
    conn.close()