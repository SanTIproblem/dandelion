# 蒲公英项目 dandelion 



### 学项目步骤（方法论）

1. 决定要学的项目（Github找源码），查找官方文档、相关的总结文章，整理出大概的学习内容与目标
2. 运行项目，观察项目总体表现（大致知道项目每个模块是干嘛的）
3. 拆解出模块制作的顺序，按照顺序逐个模块击破
   1. 先根据模块功能思考自己会怎么实现，并写一版自己实现的代码（自己动手！）
   2. 根据项目的源码进行debug，不断优化自己的代码
   3. 在debug的过程中进行相关知识的学习，并大致梳理出此模块功能实现的流程（可画图）
   4. 记录问题，把不理解的内容以问题的方式记录下来
   5. （有时间的话）写文章、笔记，尝试逐个解决之前遗留的问题



## 项目简介

2022小挑 领航·蒲公英志愿者公益网站（门户+论坛网站）



## 网站结构

![领航 · 蒲公英 网站](D:\蔡明宸\项目 ＆ 学习\2022年小挑\省赛\领航 · 蒲公英 网站.png)

### 代码结构

accounts：注册、登录功能；用户个人管理

comments：评论区（与发帖区关联）

portal：门户

posts：发帖区



## 时间安排

|      页面       |      时间       |
| :-------------: | :-------------: |
|      首页       |  一期：22.01.05-22.01.12 |
|                 |  二期：22.01.13-22.01.20|
|                  |          |
| **登录+志愿者页面** | **22.02.10-22.02.13** |
| account & portal | 22.02.10-22.02.12 |
| 美化 | 22.02.12-22.02.13 |
|                 |                 |
| **论坛** | 22.03.28-22.04.01 |
| post&comment | 03.28-03.30 |
| 美化 | 03.31-04.01 |
|                     |                         |



**细化任务：**

22.02.14：

1. 静态文件包 static 1
2. **改所有静态文件的路径** 1
3. account:（cbv）
   1. models 1
   2. views: register 1；login 1；forgetpwd
4. portal:（fbv）
   1. models 1
   2. views: home 1
5. **解决静态文件问题：404**  1



22.03.28：

1. 注册能存进数据库，但发不了邮件认证账户==》result    *1*
   1. 问题一：失败邮箱号: ['945992479@qq.com'], [WinError 10061] 由于目标计算机积极拒绝，无法连接。

      解决：开端口，https://blog.csdn.net/weixin_46900108/article/details/119773973

   2. 问题二：

      ![image-20220329153659056](C:\Users\94599\AppData\Roaming\Typora\typora-user-images\image-20220329153659056.png)

      解决：改settings.py中的邮件配置，不能有中文

      ​			https://blog.csdn.net/junxieshiguan/article/details/81811100

2. 论坛===》post&comment功能

   1. 先制定页面框架，再实现基本逻辑，最后细化页面
   2. 论坛页、不同的帖子细则页
   
3. 用request.POST，可以读出表单里的内容



22.04.05

bugs：

1. 登录功能，登录后回首页还是未登录状态

   解法：其实登出了，但是nav状态没有更改

2. digital_file: NoneType不可调用，看看怎么get form 

   解法：直接query_dict

![image-20220405163833729](C:\Users\94599\AppData\Roaming\Typora\typora-user-images\image-20220405163833729.png)

如果直接用request.POST的话，就会是一个QueryDict，而不是形成一个form（字典）



想法：

1. 点击用户名，跳转到用户专属页面normaluser.html，页面有发帖记录&调查表记录（LIstView）
2. 帖子页面article_index&article_detail



04.14：

bugs：

1. 登出以后nav条不变

   解决：删除cache，不缓存导航条

2. **addrow&removerow不能成功 （and views层中处理的应该是一对多关系）**



04.18：

1. 论坛部分开始制作，任务量较大，加油加油！



04.19：

1. 论坛部分框架搭建完成，add details
2. 开始做评论区
   1. 已有评论 comment_list
   2. 发布评论 post_comment
   3. 回复评论 comment_item_tree



bugs：

1. index页点击帖子，应该跳转到详情页：完成article类中get_absolute_url函数

   ![image-20220419205741364](C:\Users\94599\AppData\Roaming\Typora\typora-user-images\image-20220419205741364.png)



04.23：

bugs：

1. comments：什么时候form_valid（评论成功） 

![image-20220423235329265](C:\Users\94599\AppData\Roaming\Typora\typora-user-images\image-20220423235329265.png)

2. post：创建帖子需要自动匹配author
