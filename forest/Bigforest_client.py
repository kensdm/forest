#encoding:utf-8

import socket
import pickle
import time

class Bigforest_client:
    def __init__(self,ip,port):
        self.client = socket.socket()
        self.client.connect((ip, int(port)))

    def add_master(self,data):
        message=('1',data)
        self.client.send(pickle.dumps(message))
        re_data = self.client.recv(1024)
        re_data = pickle.loads(re_data)
        print("server>>", re_data)
    def add_split(self,data):
        message = ('2', data)
        self.client.send(pickle.dumps(message))
        re_data = self.client.recv(1024)
        re_data = pickle.loads(re_data)
        print("server>>", re_data)
    def add_slave(self,data):
        message = ('3', data)
        self.client.send(pickle.dumps(message))
        re_data = self.client.recv(1024)
        re_data = pickle.loads(re_data)
        print("server>>", re_data)
    def add_super_node(self,data):
        message = ('4', data)
        self.client.send(pickle.dumps(message))
        re_data = self.client.recv(1024)
        re_data=pickle.loads(re_data)
        print("server>>", re_data)
    def bing(self,data,):
        message = ('5', data)
        self.client.send(pickle.dumps(message))
        re_data = self.client.recv(1024)
        re_data = pickle.loads(re_data)
        print("server>>", re_data)
    def put_dict(self,data):
        message = ('6', data)
        self.client.send(pickle.dumps(message))
        re_data = self.client.recv(1024)
        re_data = pickle.loads(re_data)
        print("server>>", re_data)
    def get_sql(self):
        message = ('7', ' ')
        self.client.send(pickle.dumps(message))
        re_data = self.client.recv(1024)
        re_data = pickle.loads(re_data)
        print("server>>", re_data)

        # '1': self.__t.Add_master_node,
        # '2': self.__t.Add_split_node,
        # '3': self.__t.Add_slave_node,
        # '4': self.__t.Add_super_node,
        # '5': self.__t.bing_table,
        # '6': self.__t.put_dict,
        # '7': self.__t.get_sql
if __name__ == '__main__':
    ip='127.0.0.1'
    port=1234
    a=Bigforest_client(ip,port)
    uid = 15
    uid1 = 20
    uid2 = 40
    sql = 'insert'
    table = 'go'
    database = 'test'
    database1 = 'testtest'

    ip1 = '127.0.0.1:3306'
    ip2 = '127.0.0.1:3307'
    ip3 = '127.0.0.1:3309'
    admin = {'user': 'root', 'passwd': 'root'}
    admin1 = {'user': 'root11', 'passwd': 'root'}
    jiqun1 = '用户'
    jiqun2 = '商品'
    data=(jiqun1,sql, database, uid, ip1, admin)
    data1 = (jiqun2, sql, database, uid, ip2, admin)
    data2=(jiqun1,sql, database, uid, ip3, admin)
    datadict={'用户uid':{'uid':14},'事件':'支付','商品id':{'spid':3},'数量':4,'价格':10,'事件对象uid':{'uid':12}}

    a.add_super_node(jiqun1)
    a.add_master(data)
    a.add_super_node(jiqun2)
    a.add_master(data1)
    a.add_split(data2)
    a.bing(jiqun1)
    a.bing(jiqun2)
    start = time.time()
    a.put_dict(datadict)
    a.get_sql()
    print(time.time()-start)