# Bigforest
分布式节点路由管理器
# Distributed-node-management-python
## 功能介绍
- 1、数据库数据水平分表 
本管理器根据水平分表需求的思路进行设计，所以在使用本管理器时，需先设定表的最大行数

      import gorun
      #RowMax是设置每个表的最大行数
      '''当然根据自己数据库的表的原思路来定义这个数值'''
      t=gorun(RowMax=20)
 
- 2、动态节点扩展 动态添加节点不用重新修改配置，整个节点管理器分为两层：
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
