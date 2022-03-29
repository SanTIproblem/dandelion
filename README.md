# 蒲公英项目 dandelion 



**答应我，保证永远只在Local做修改，再push到Remote好吗？！**



## 项目简介

2022小挑 蒲公英志愿者公益网站



## 项目结构

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
| comment | 03.28-03.30 |
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

1. 注册能存进数据库，但发不了邮件认证账户==》result
   1. 失败邮箱号: ['945992479@qq.com'], [WinError 10061] 由于目标计算机积极拒绝，无法连接。
   
      ![image-20220329153659056](C:\Users\94599\AppData\Roaming\Typora\typora-user-images\image-20220329153659056.png)
   
      解决：https://github.com/liangliangyy/DjangoBlog/issues/460
2. 论坛===》comment功能





