import socket
import struct
import json

download_dir='D:\python3.7\chengxu\luffy\ch-5\小型FTP\服务端\download'


def get(phone):
    # 拿到文件内容，以写的方式打开一个新文件，写入客户端
    # 1.收报头
    header = phone.recv(4)
    header_size = struct.unpack('i', header)[0]

    header_bytes = phone.recv(header_size)
    header_json = header_bytes.decode('utf-8')
    header_dic = json.loads(header_json)
    total_size = header_dic['file_size']
    # 2.从报头解析数据
    filename = header_dic['filename']
    f = open('%s/%s' % (download_dir, filename), 'wb')
    recv_size = 0
    while recv_size < total_size:
        data = phone.recv(1024)
        f.write(data)
        recv_size += len(data)

def client():
    phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    phone.connect(('127.0.0.1',8081))

    while 1:
        #发命令
        msg=input('--')
        if not msg:continue
        phone.send(msg.encode('utf-8'))
        cmds=msg.split()
        if cmds[0] == 'get':
            get(phone)
    phone.close()

if __name__ == '__main__':
    client()