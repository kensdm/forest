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
- - - 5) bind：绑定当前节点信息
- - - 6) put_dict：订单队列，用于添加订单信息 
           数据结构为:
           {'用户uid':{'uid':14},'事件':'支付','商品id':{'spid':3},'数量':4,'价格':10,'事件对象uid':{'uid':12}}
- - - 7) get_sql：根据订单信息匹配对应mysql信息与生成sql语句，返回列表，列表元素结构为：
                  (sql语句,(dbname,ip:port,admin))
        
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
         
- - 4)指定集群添加主节点add_master，有6个参数，分别是:Cluster_nam,'insert', dbname, Level, ip, admin
- - - 1) Cluster_nam：添加主节点时需要传入对应的Cluster_nam，比如上面我们创建了2个集群管理器，一个是用户，一个是商品，如果这次我们添加的主节点是                         属于用户集群的，那么这个Cluster_nam的值就需要定义为'用户'
- - - 2) 'insert'：第二个参数需要传入'insert',这个参数可无视但是传参时不能漏掉，写代码的时候乱加的，到时会去掉
- - - 3) dbname：传入对应ip的数据库名称
- - - 4) Level：传入水平分表设置的最大范围值
- - - 5) ip ： 传入对应数据库的ip地址需带上端口号，格式为:'127.0.0.1:3306' 
- - - 6) admin ：mysql的账号密码，格式为：{'user': 'root', 'passwd': 'root'}

               Cluster_name='用户'
               Cluster_name1='商品'
               qt='insert'
               dbname = 'test'
               Level = 20
               ip = '127.0.0.1:3306'
               ip1='127.0.0.1:3307'
               admin={'user': 'root', 'passwd': 'root'}

               #打包成元组
               yh_data=(Cluster_name,qt,dbname,Level,ip,admin)
               sp_data=(Cluster_name1,qt,dbname,Level,ip1,admin)
               Bf.add_master(yh_data)#注意:参数需要以元组方式传入
               Bf.add_master(sp_data)
               ----------------------------------------------------
               由服务端返回结果：
               server>> 已处理完成：master节点已经添加完成
               server>> 已处理完成：master节点已经添加完成

- - 5) 指定集群添加垂直节点信息add_split,add_split和add_master函数操作一样，有6个参数，分别是:Cluster_nam,'insert', dbname, Level, ip, admin
- - - 1) Cluster_nam：添加垂直节点时需要传入对应的Cluster_nam，比如上面我们创建了2个集群管理器，一个是用户，一个是商品，如果这次我们添加的主节点是                         属于用户集群的，那么这个Cluster_nam的值就需要定义为'用户'
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
               ip = '127.0.0.1:3308'
               admin={'user': 'root', 'passwd': 'root'}

               #打包成元组
               data=(Cluster_name,qt,dbname,Level,ip,admin)
               Bf.add_split(data)#注意:参数需要以元组方式传入
               ----------------------------------------------------
               由服务端返回结果：
               server>> 已处理完成：垂直节点已添加完成

- - 6) 指定集群添加从节点信息add_add_slave,和add_master函数操作一样，有7个参数前6个和主节点参数一样，第7个是指定垂直节点的号码，
       分别是:Cluster_nam,'insert', dbname, Level, ip, admin，split_num
- - - 1) Cluster_nam：添加从节点时需要传入对应的Cluster_nam，比如上面我们创建了2个集群管理器，一个是用户，一个是商品，如果这次我们添加的主节点是                         属于用户集群的，那么这个Cluster_nam的值就需要定义为'用户'
- - - 2) 'insert'：第二个参数需要传入'insert',这个参数可无视但是传参时不能漏掉，写代码的时候乱加的，到时会去掉
- - - 3) dbname：传入对应ip的数据库名称
- - - 4) Level：传入水平分表设置的最大范围值
- - - 5) ip ： 传入对应数据库的ip地址需带上端口号，格式为:'127.0.0.1:3306' 
- - - 6) admin ：mysql的账号密码，格式为：{'user': 'root', 'passwd': 'root'}
- - - 7) split_num ：指定垂直号码，如何区别垂直号码，请参考管理器说明图，从整个结构了解(暂时无图)
- - - 8) 注意：如果没有添加主节点的情况下，添加从节点是不成功的，系统会红字提示：先添加主节点再添加从节点

               Cluster_name='用户'
               qt='insert'
               dbname = 'test'
               Level = 20
               ip = '127.0.0.1:3309'
               admin={'user': 'root', 'passwd': 'root'}
               '''
               说明：
               刚才我们添加了一个主节点、一个垂直节点，这时我们有两个节点，他们对应的下标是:主节点:0,垂直节点:1
               如果在添加从节点前再添加一次垂直节点,下标数就会变成：主节点:0,垂直节点:1，垂直节点:2 
               3个节点的关系以平时的3表联表操作的方式理解,而下标值代表的是split_num值
               '''
               
               split_num=1 #我们由两个[0,1]节点中挑选一个下标，1
               #打包成元组
               data=(Cluster_name,qt,dbname,Level,ip,admin,split_num)
               Bf.add_slave(data)#注意:参数需要以元组方式传入
               ----------------------------------------------------
               由服务端返回结果：
               server>> 已处理完成：从节点已添加完成

- - 7) 添加完节点之后，还需要一步操作，绑定指定集群所有节点数据，使用bind函数,bind函数带有1个参数，Cluster_name（集群名称）

               Cluster_name='用户'
               Bf.bind(Cluster_name)
               ----------------------------------------------------
               由服务端返回结果：
               server>> 已处理完成：已经绑定用户集群所有表
               
- - 8) put_dict:订单队列，当添加完所有节点后，我们可以开始做分布式匹配工作了

               
               #我们先硬性定义一个订单支付信息（目前只能以下面的key内容为准用来示例，后面会做修改）
               data={'用户uid':{'uid':14},'事件':'支付','商品id':{'spid':3},'数量':4,'价格':10,'事件对象uid':{'uid':12}}
               Bf.put_dict(data) #加入执行队列
               ----------------------------------------------------
               由服务端返回结果：
               server>> 已处理完成：
               {'用户uid': {'uid': 14}, '事件': '支付', '商品id': {'spid': 3}, '数量': 4, '价格': 10, '事件对象uid': {'uid': 12}}
               已经入队

- - 9) get_sql: 订单加入队列后可通过get_sql函数来执行，匹配各个节点信息与生成对应sql语句,返回订单的所有sql内容

               Bf.get_sql()#匹配和生成速度瞬时完成
               ----------------------------------------------------
               server>> 已处理完成：[
               ('update go set monney=monney-40 where uid=14;', ('test', '127.0.0.1:3306', {'user': 'root', 'passwd': 'root'})),
               ('update look set kc=kc-4 where spuid=3;', ('test', '127.0.0.1:3307', {'user': 'root', 'passwd': 'root'})), 
               ('update go set monney=monney+40 where uid=12;', ('test', '127.0.0.1:3306', {'user': 'root', 'passwd': 'root'}))
               ]

 
