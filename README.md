# 蒲公英项目 dandelion 



1. **答应我，保证永远只在Local做修改，再push到Remote好吗？！**

2. **不要高估自己的能力，错误地预估工作量！**





## 项目简介

2022小挑 蒲公英志愿者公益网站



## 项目结构

![领航 · 蒲公英 网站](D:\蔡明宸\项目 ＆ 学习\2022年小挑\省赛\领航 · 蒲公英 网站.png)

accounts：用户注册、登录功能

comments：评论功能（与发帖功能关联）

portal：门户

posts：发帖功能



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
2. addrow&removerow不能成功 （and views层中处理的应该是一对多关系）



04.18：

1. 论坛部分开始制作，任务量较大，加油加油！
