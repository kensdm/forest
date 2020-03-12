#encoding:utf-8

from Bigforest.Bf import gorun
import time
import socket
import threading
import pickle

class Bigforest_server:
    def __init__(self,ip,port,listen_num):
        self.__t = gorun(20)
        self.__runfunc = {
            '1': self.__t.Add_master_node,
            '2': self.__t.Add_split_node,
            '3': self.__t.Add_slave_node,
            '4': self.__t.Add_super_node,
            '5': self.__t.bing_table,
            '6': self.__t.put_dict,
            '7': self.__t.get_sql,
            '8': self.__t.prin,
        }

        self.address = (ip, int(port))  # 服务端地址和端口
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.address)  # 绑定服务端地址和端口
        self.s.listen(listen_num)
        self.run()

    def accept_client(self):
        while True:
            conn, addr = self.s.accept()
            print('Client %s connected!' % str(addr))
            t1=threading.Thread(target=self.recv_message,args=(conn,))
            t1.start()

    def recv_message(self,conn):
        while True:
            try:
                re_data=conn.recv(1024)
                if re_data ==b'':
                    continue
            except:
                self.close_conn(conn)
                break
            else:
                re_data=pickle.loads(re_data)
                if re_data[1]==' ':
                    data=self.__runfunc[re_data[0]]()
                    message = f"已处理完成：{data}"
                    self.send_message(pickle.dumps(message), conn)
                else:
                    data=self.__runfunc[re_data[0]](re_data[1])
                    message = f"已处理完成：{data}"
                    self.send_message(pickle.dumps(message), conn)
                
    def send_message(self,message,conn):
        conn.send(message)

    def close_conn(self,conn):
        conn.close()
        print(conn, '断开连接')

    def run(self):
        t2=threading.Thread(target=self.accept_client)
        t2.start()

if __name__ == '__main__':
    ip='127.0.0.1'
    port=1234
    listen_num=5
    Bigforest_server(ip,port,listen_num)