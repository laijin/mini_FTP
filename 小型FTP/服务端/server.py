import socket
import os
import subprocess
import struct
import json

share_dir=r'D:\python3.7\chengxu\luffy\ch-5\小型FTP\客户端\share'

def get(cmds,conn):
    filename = cmds[1]
    # 以读的方式打开文件，读取文件内容，发送给客户端

    header_dic = {
        'filename': filename,
        'md5': 'graga',
        'file_size': os.path.getsize(r'%s/%s' % (share_dir, filename))
    }
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode('utf-8')

    header_len = struct.pack('i', len(header_bytes))
    # 2、把报头发送给客户端
    conn.send(header_len)
    conn.send(header_bytes)
    # 3、发送数据
    f = open('%s/%s' % (share_dir, filename), 'rb')
    for line in f:
        conn.send(line)




def server():
    phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    phone.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    phone.bind(('127.0.0.1',8081))

    phone.listen(5)

    while True:
        conn,client_addr=phone.accept()

        while True:
            try:
                data=conn.recv(1024)
                if not data:break
                print('客户端的数据为',data)
                # 1、conn.send(data.upper())

                #解析命令，提取相应的命令参数
                cmds=data.decode('utf-8').split()
                if cmds[0] == 'get':
                    get(cmds,conn)
            except ConnectionResetError:
                break

        conn.close()

    phone.close()
if __name__ == '__main__':
    server()

