# config: utf-8
"""
描述：这是一个从响应中提取可能的请求参数的脚本

作者：CreatNULL
创建日期：2024 年 9 月 29 日
版本：1.0
"""
import os
import re
import logging
from mitmproxy import http
from finger.fingerprint import identify_js_fingers
from extract.extractparam import extract_params

# 日志路径
root_path = os.path.split(os.path.realpath(__file__))[0]
log_path = os.path.join(root_path, 'log')
log_file = os.path.join(log_path, 'app.log')
# 调试使用，如果规则没有匹配上，可以在 not_match_log 查看，获取发现原因，之前就是发现原来漏了个 ,
match_log = os.path.join(log_path, 'match_log.txt')
not_match_log = os.path.join(log_path, 'not_match_log.txt')
# 指定输出文件
output_file = os.path.join(root_path, 'output_param.txt')

if not os.path.exists(log_path):
    os.makedirs(log_path)

# 配置日志
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义要跳过的 URL 正则模式
bypass_patterns = [
                   # 微软
                   ".*microsoftonline.com",
                   ".*bbs.sxnews.cn", # 新闻
                   r"akamaized.net",
                   "login.live.com.*",
                   ".*msn.com.*",
                   "ecn.dev.ditu.live.com.*",
                   # bing
                   r".*bing.com.*",
                   ".*nelreports.net.*",
                   # 百度
                   ".*baidu.com.*",
                   # 谷歌
                   ".*google.com.*",
                   ".*googleapis.com.*",
                   ".*google-analytics.com.*",
                   ".*googleusercontent.com",
                   ".*chrome.com.*",
                   ".*doubleclick.net", # 曾经是一家网络广告服务商的网站  2008年3月11日已经被 Google（谷歌）收购 Google AdSense （谷歌广告）
                   # 博客
                   ".*csdn.net", # CSDN
                   ".*cnblogs.com.*",
                   ".*juejin.cn", # 掘金
                   ".*zhihu.com", # 知乎
                   ".*anquanke.com.*"  # 安全客
                   # github
                   ".*github.com",
                   ".*github.io",
                   # 腾讯
                   ".*cloud.tencent.com", # 腾讯 cdn
                   ".*pub.idqqimg.com.*",
                   # B站
                   ".*bilibili.com", # B站
                   ".*bilivideo.cn.*",
                   # 抖音
                   ".*douyin.com.*",
                   # src 平台
                   ".*butian.net",  #  补天
                   # 空间搜索引擎
                   ".*shodan.io",   # 撒旦
                   ".*zoomeye.org",    # 钟馗
                   ".*fofa.info",   # fofa
                   ".*hunter.qianxin.com",   # 鹰图
                   # 奇安信
                   r"qianxin.com",
                   # 反爬虫
                   ".*geevisit.com", # 极验
                   ".*geetest.com.*",
                   # 政府网站
                   ".*miit.gov.cn",  # ICP备案 工信部
                   ".*people.com.cn", # 人民网
                   # 广告
                   ".*casalemedia.com",  # indexexchange 广告
                   ".*talk99.cn",  # talk99 网络营销专用软件
                   # AI
                   ".*hackerai.co.*",
                   # cloudflare
                   ".*cloudflare-dns.com.*",
                   ".*cloudflare.com.*",
                   # 漏洞网站
                   ".*vulners.com.*",
                   # 谷歌插件
                   ".*ctool.de.*v",     # ctool 工具
                   ".*immersivetranslate.com",   # 沉浸式翻译
                   # 未知
                   "union2.50bang.org",
                   # 常见的 图片、视频、音频、文档、压缩文件等静态文件
                   r'(\.jpg|\.jpeg|\.svg|\.bmp|\.webp|\.tiff|\.ico|\.png|\.gif)$',  # 图片
                   r'(\.mp4|\.avi|\.mkv|\.mov|\.wmv|\.flv|\.webm|\.mpeg|\.mpg|\.3gp)$',  # 视频
                   r'(\.mp3|\.wav|\.aac|\.flac|\.ogg|\.wma|\.alac)$',   # 音频
                   r'(\.pdf|\.docx|\.doc|\.xlsx|\.xls|.css)$',   # 文档
                   r'(\.zip|\.rar|\.7z|\.tar|\.zip|\.tar\.gz|\.xz)$',   # 压缩文件
                   # .css?v= 格式的
                   r'(\.css\?)',
                   ]


def write_params_to_file(params):
    try:
        with open(output_file, 'a+', encoding='utf-8') as f:
            for param in params:
                f.write(f"{param['param']}\n")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")


def should_bypass(url):
    result = []
    for param in bypass_patterns:
        if re.search(param, url):
            with open(match_log, 'a+', encoding='utf-8') as f:
                f.write(f"[-] 判断规则: {param}\n")
                f.write(f"[!] 匹配成功 {re.search(param, url)}\n")
            result.append(True)
        else:
            with open(not_match_log, 'a+', encoding='utf-8') as f:
                f.write(f"[-] 判断规则: {param}\n")
                f.write(f"[!] 匹配失败 {re.search(param, url)}\n")
            result.append(False)
    # result = [bool(re.search(pattern, url)) for pattern in bypass_patterns]
    # logging.info("匹配过滤 URL 的结果: " + str(result))
    # logging.info(f"匹配过滤 URL 的结果 Bool: {any(result)}")
    return any(result)


def request(flow: http.HTTPFlow) -> None:
    try:
        logging.info(f"Request to {flow.request.url}")
        # 如果没有匹配到规则
        if not should_bypass(flow.request.url):
            params = extract_params([flow.request.url, flow.request.content.decode('utf-8', 'ignore')])
            logging.info(f"Extracted parameters: {str(params)}")
            write_params_to_file(params)
        else:
            logging.info(f"Skipping request to {flow.request.url}")
    except Exception as e:
        logging.error(f"Error processing request: {e}")


def response(flow: http.HTTPFlow) -> None:
    try:
        logging.info(f"Response from {flow.request.url}")
        # 未匹配到
        if not should_bypass(flow.request.url):
            # 响应内容
            response_content = flow.response.content.decode('utf-8', 'ignore')
            # 响应内容不为空
            if response_content:
                result = identify_js_fingers(content=response_content)
                if result['isfinder']:
                    logging.info("Skipping response, match js file rule")
                else:
                    params = extract_params([flow.response.content.decode('utf-8', 'ignore')])
                    logging.info(f"Extracted parameters: {str(params)}")
                    write_params_to_file(params)
            else:
                logging.info("Empty response from server")
        else:
            logging.info(f"Skipping request to {flow.request.url}")
    except Exception as e:
        logging.error(f"Error processing response: {e}")


if __name__ == '__main__':
    logging.info("使用命令 mitmproxy -s fat_fish.py 运行该脚本")
