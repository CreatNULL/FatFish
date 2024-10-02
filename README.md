# Fat_Fish

## 这是什么？

```text
  一个提取网站中可能的参数，作为字典（需要自己对结果去重）

  我是个小丑🤡，┭┮﹏┭┮。 看完了公共号文章，试试它说的插件，结果试了半天burpsuite报错，好好好，自己写。没想到写好了刷微信公号的时候看到了其他大佬写好的工具，还是俩，呜呜
  - https://github.com/theLSA/burp-sensitive-param-extractor
  - https://github.com/goddemondemongod/god_param?tab=readme-ov-file
       
   想起了 "老墨，我想吃鱼啦" 于是取了个名字叫 fat_fish，希望带来丰收吧，桀桀桀
```

## 功能介绍
    很简单，作为代理服务器，监听请求，获取请求以及响应的数据中的可能的参数名称，提供给未授权测试使用的参数。

## 逻辑：
- 就是匹配表单，提取参数
- 看参数可能的格式就 {参数: "参数值"}
- 然后过滤掉常见的http头部（感谢大佬的 https://github.com/synacktiv/HopLa ，嘿嘿， http头部就是从这里面拿来用的）
- 过滤掉不符合命名规范的
- 过滤掉常见的js文件
  
## 模块介绍
    finger模块:
        自定义指纹：
            仅仅实现了简单常见的js文件的指纹，后续遇见什么自己添加即可。提供给fat_fish 过滤 常见的 js库 文件
        指纹规则匹配的方式: 
            1. 文件的md5（md5）
            2. 文件中存在的关键字 (keyword)
            3. 正则匹配 (reg)
        规则处理逻辑: 
            1. &&  全部匹配则算命中
            2. ||  匹配到一个即算命中
    
    extract模块:
        提取模块, 实现参数的提取， 提取的规则: 
        提取:
            1. {"": ""} 格式的
            2. url 中出现的可能的参数
            3. input 表单中的 参数
        过滤:
            1. 对出现的 http  头部进行过滤
            2. 不符合变量命名规范的
            3. 用户自定义的参数过滤

    fat_fish入口文件:
        程序的入口脚本，通过安装 mitmproxy 库，然后安装他的证书，利用它劫持响应数据。将数据发送给 finger 和 extract 模块处理
        finger -> 发送 请求的 body 数据，
        extract -> 发送 请求的 body 和  url
        bypass_patterns 指定过滤的 url 不进行提取

## 注意:
    启动使用:
        mitmproxy -s  .\fat_fish.py
    监听端口:
        默认 8080 和 burpsuite 监听端口相同
        使用 mitmproxy -p 8081 -s  .\fat_fish.py 切换端口
    证书安装:
        证书记得安装，不然抓不了https流量, 可以选择我下载好的，安装，也可启动后访问 mitm.it 来下载证书
    添加指纹:
        finger/fingers.py 中添加
    添加不提取的参数名称:
        extract/extractparam.py 中的 BYPASS_LIST 添加
    添加不匹配的 url:
        fat_fish.py 中的 bypass_patterns
    如果添加了规则，并且确定规则没问题。则看看末尾是否漏了, 

```python
BYPASS_LIST = [
'_',
''
]
```



