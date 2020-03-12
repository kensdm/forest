# Bigforest
Bigforest是一个分布式节点路由管理器，可随时添加扩展节点信息
主要应用
1、mysql负载均衡，水平/垂直集群管理，跨部门节点管理
2、跨部门集群分布式节点路由，比如：在处理订单信息时，往往会出现跨多个节点的sql操作，
   Bigforest可以根据订单信息直接生成对应节点的sql语句、对应节点的数据库信息，
   结果返回多个元组元素的列表，用户只需实现map功能就可执行分布式事务
3、Bigforest管理器是根据水平/垂直分割逻辑来定义的，所以在使用Bigforest时，需要设计好自己的水平分割逻辑与垂直分割逻辑
## 功能介绍
- 1、Bigforest_server有4个参数，分别为ip,port,listen_num,Level，通讯方式为TCP
     参数说明：ip为服务地址，port为自定义端口号，listen_num为连接数，Lever为水平分表设置的最大范围值
     
         from Bigforest.Bigforest_server import Bigforest_server
         ip = '127.0.0.1'
         port = 1234
         listen_num = 5
         Level=20
         Bigforest_server(ip, port, listen_num,Level) #运行直接启动服务

- 2、Bigforest_client目前有7个可用模块
- - 1) 分别是：
- - - 1) add_super_node:添加跨服务集群管理器
- - - 2) add_master：添加主节点信息
- - - 3) add_split：添加垂直节点信息
- - - 4) add_slave：添加从节点信息
- - - 5) bing：绑定当前节点信息
- - - 6) put_dict：订单队列，用于添加订单信息 
           数据结构为:{'用户uid':{'uid':14},'事件':'支付','商品id':{'spid':3},'数量':4,'价格':10,'事件对象uid':{'uid':12}}
- - - 7) get_sql：根据订单信息匹配对应mysql信息与生成sql语句，返回列表，列表元素结构为：(sql语句,(dbname,ip:port,admin))
        
- - 2)Bigforest_client初始化有2个参数,分别是绑定服务器的ip,port

               from Bigforest.Bigforest_client import Bigforest_client
               ip = '127.0.0.1'
               port = 1234
               Bf=Bigforest_client(ip, port)

- - 3)添加集群管理器add_super_node，有1个参数：Cluster_name（集群名称），在添加服务节点时，需要先注册集群管理器，否则无法添加服务节点，

               Bf=Bigforest_client(ip, port)
               Cluster_name='用户'
               Cluster_name1='商品'
               Bf.add_super_node(Cluster_name)
               Bf.add_super_node(Cluster_name1)
               ----------------------------------------------------
               由服务端返回结果：
               server>> 已处理完成：用户集群管理器添加成功
               server>> 已处理完成：商品集群管理器添加成功
         
- - 4)各个集群添加主节点add_master，有6个参数，分别是:Cluster_nam,'insert', dbname, Level, ip, admin
- - - 1) Cluster_nam：添加主节点时需要传入对应的Cluster_nam，比如上面我们创建了2个集群管理器，一个是用户，一个是商品，如果这次我们添加的主节点是                         属于用户集群的，那么这个Cluster_nam的值就需要定义为'用户'
- - - 2) 'insert'：第二个参数需要传入'insert',这个参数可无视但是传参时不能漏掉，写代码的时候乱加的，到时会去掉
- - - 3) dbname：传入对应ip的数据库名称
- - - 4) Level：传入水平分表设置的最大范围值
- - - 5) ip ： 传入对应数据库的ip地址需带上端口号，格式为:'127.0.0.1:3306' 
- - - 6) admin ：mysql的账号密码，格式为：{'user': 'root', 'passwd': 'root'}

               Cluster_name='用户'
               qt='insert'
               dbname = 'test'
               Level = 20
               ip = '127.0.0.1:3306'
               admin={'user': 'root', 'passwd': 'root'}

               #打包成元组
               data=(Cluster_name,qt,dbname,Level,ip,admin)
               Bf.add_master(data)#注意:参数需要以元组方式传入
               ----------------------------------------------------
               由服务端返回结果：
               server>> 已处理完成：master节点已经添加完成

- - 5) 添加垂直节点信息add_split,add_split和add_master函数操作一样，有6个参数，分别是:Cluster_nam,'insert', dbname, Level, ip, admin
- - - 1) Cluster_nam：添加主节点时需要传入对应的Cluster_nam，比如上面我们创建了2个集群管理器，一个是用户，一个是商品，如果这次我们添加的主节点是                         属于用户集群的，那么这个Cluster_nam的值就需要定义为'用户'
- - - 2) 'insert'：第二个参数需要传入'insert',这个参数可无视但是传参时不能漏掉，写代码的时候乱加的，到时会去掉
- - - 3) dbname：传入对应ip的数据库名称
- - - 4) Level：传入水平分表设置的最大范围值
- - - 5) ip ： 传入对应数据库的ip地址需带上端口号，格式为:'127.0.0.1:3306' 
- - - 6) admin ：mysql的账号密码，格式为：{'user': 'root', 'passwd': 'root'}
- - - 7) 注意：如果没有添加主节点的情况下，添加垂直节点是不成功的，系统会红字提示：先添加主节点再添加垂直节点

               Cluster_name='用户'
               qt='insert'
               dbname = 'test'
               Level = 20
               ip = '127.0.0.1:3306'
               admin={'user': 'root', 'passwd': 'root'}

               #打包成元组
               data=(Cluster_name,qt,dbname,Level,ip,admin)
               Bf.add_split(data)#注意:参数需要以元组方式传入
               ----------------------------------------------------
               由服务端返回结果：
               server>> 已处理完成：垂直节点已添加完成

- - 6) 添加垂直节点信息add_split



、动态节点扩展 动态添加节点不用重新修改配置，整个节点管理器分为两层：
- - - 1)、'insert'层：主要来管理所有节点，每个节点列表的第一个ip为主节点，后面的为从节点
- - - 2)、'select'层：负载均衡管理器，在匹配范围sql语句对应的server_ip时,
                     会根据这层的结果中匹配出server_ip因为考虑到节点之间负载均衡的问题，所以添加主节点时，会自动添加到负载均衡管理器中
- - 2.1 添加主节点
            
            t.Add_master_node('insert', '191.168.1.0')
            t.Add_master_node('insert','191.168.1.1')
            t.Add_master_node('insert','191.168.1.2')
            t.Add_master_node('insert','191.168.1.3')
            print(t.all_DB_ip)
            --------------------------------------------------------------------------------
            结果：{
            'insert':
            {0: ['191.168.1.0'], 1: ['191.168.1.1'], 2: ['191.168.1.2'], 3: ['191.168.1.3']},
            'select': 
            {0: ['191.168.1.0'], 1: ['191.168.1.1'], 2: ['191.168.1.2'], 3: ['191.168.1.3']}
            }
- - 2.2 添加从节点
            
            给某个主节点添加从节点时需要知道指定key，
            比如想给191.168.1.0主节点添加从节点'191.168.1.4',而191.168.1.0对应的管理器key为0
            想给'191.168.1.2'添加从节点'191.168.1.5'，而191.168.1.2对应的管理器key为2
            t.Add_slave_node('insert',0,'191.168.1.4')
            t.Add_slave_node('insert',2,'191.168.1.5')
            print(t.all_DB_ip)
            ---------------------------------------------------------------------------------------------------------------
            结果：{
            'insert': 
            {0: ['191.168.1.0', '191.168.1.4'], 1: ['191.168.1.1'], 2: ['191.168.1.2', '191.168.1.5'], 3: ['191.168.1.3']}, 
            'select': 
            {0: ['191.168.1.0', '191.168.1.4'], 1: ['191.168.1.1'], 2: ['191.168.1.2', '191.168.1.5'], 3: ['191.168.1.3']}
            }
- 3、分布式节点匹配
      
      输入sql语句，自动匹配节点直接返回匹配好的sql语句和对应server_ip的列表
      node_sql_list=t.Task_distribution_list('select * from table where uid>15 and uid<79')
      print(node_sql_list)
      ------------------------------------------------------------------------------------
      结果返回列表：
      [
      ('191.168.1.0', 'select * from table where uid > 15'),
      ('191.168.1.1', 'select * from table where uid < 40'), 
      ('191.168.1.5', 'select * from table where uid < 60'), 
      ('191.168.1.3', 'select * from table where uid < 79')
      ]

- 4、读写分离路由，分布式任务匹配节点路由 
- 5、节点热点负载均衡统计 
- 6、分布式数据整合
      
      数据整合列表：self.y
      定义好执行任务函数（可自定义执行方式，本例以作者自定义案例为主），
      把 执行任务函数 的结果储存进self.y列表中方便后面查看结果
      
      如：
      def do_it(self,tuples):
         global t1       #global t1 是共享 分布式任务分发函数 的线程变量 具体内容请看功能介绍第7点
         j=f'{t1.name} do it ===> ip:{tuples[0]} and sql:{tuples[1]}'
         self.y.append((t1.name,j))
      
      
- 7、执行任务函数 与 分布式任务分发函数
      
      执行任务：为接收分布式节点匹配结果列表为参数 的执行函数
      执行任务函数名（任务逻辑可自定义）：
      do_it(tuples) #参数说明：传入一个ip与sql语句 组成的元组
      
      分布式任务分配函数名（任务逻辑可自定义）：Task_distribution(func,node_sql_list) 
      #参数说明：
      func参数为执行任务函数名，如已经定义好的 do_it函数；
      node_sql_list参数为 分布式节点匹配结果 如功能介绍的第三点分布式节点匹配结果：node_sql_list
      
      定义好分布式任务分配函数（可自定义执行方式，本例以作者自定义案例为主）
      def Task_distribution(self,func,node_sql_list):
         global t1
         for i in range(len(b)):
            t1 = threading.Thread(target=func, args=(node_sql_list[i],))
            t1.start()
            
      测试：
      以上面第3、分布式节点匹配 得到的结果做例子
      为了方便，把第3点的执行语法也写在这儿
      node_sql_list=t.Task_distribution_list('select * from table where uid>15 and uid<79')
      
      开始  分布式任务分配
      #该函数是使用异步线程分配执行，所返回的结果整合储存在self.y列表中
      t.Task_distribution(t.do_it,node_sql_list)  #线程变量名为：t1
      print(t.y) #最后结果可以打印t.y列表进行查看
      ---------------------------------------------------------------------------------------------------
      结果：
      [
      ('Thread-1', 'Thread-1 do it ===> ip:191.168.1.0 and sql:select * from table where uid > 15'), 
      ('Thread-2', 'Thread-2 do it ===> ip:191.168.1.1 and sql:select * from table where uid < 40'), 
      ('Thread-3', 'Thread-3 do it ===> ip:191.168.1.2 and sql:select * from table where uid < 60'), 
      ('Thread-4', 'Thread-4 do it ===> ip:191.168.1.3 and sql:select * from table where uid < 79')
      ]
