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
