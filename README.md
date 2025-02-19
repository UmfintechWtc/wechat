# wechat

#### 介绍
企业微信应用消息回调

#### 软件架构
软件架构说明


#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明
##### 告警接口

+ 请求方法  
    ```python
    POST、GET
    ```

+ 请求接口  
    ```python
    /alarm
    ```  
  
+ 请求类型  
    ```python
    {"Content-Type": "application/json"}  
    ```

+ 请求参数说明
    
    + agentid: int
       - 必要参数
        > 企业微信应用 agentid
      
    + secret: string
        - 必要参数
        > 企业微信应用 secret
    
    + receiver: Dict[string, List[string]]
        - 必要参数，三选一
        ```python
        {"touser": []}    # 指定接收消息的成员
        {"toparty": []}   # 指定接收消息的部门
        {"totag": []}     # 指定接收消息的标签
        ```
    + content: string
        > 告警内容
    
    + msg_type: string
        > 消息格式 text | markdown

      


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
