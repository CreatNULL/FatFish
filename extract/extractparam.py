# coding: utf-8
"""
原理:
    提取类似：
            '/index?name=John',
            '/index?name=&age=25',
            '/index/user:id',
    POST 提交，基本都是在 {:} 包裹范围内
    提取 {
        param: 'value'
    }
    但是对于http头部进行过滤，不需要
    提供自定义的过滤列表
"""
import re
import json
import logging
from urllib.parse import urlparse, parse_qs

# 测试用的 字符串列表
demo_contents_url = [
    'https://www.bing.com/osjson.aspx?query=1&language=&PC=U316',
    '/index?name=John',
    '/index?name=&age=25',
    '/index/user:id',
    '百度的是 https://www.baidu.com/query?wd=&ie=utf-8&pn= 哈哈哈',
    ]

demo_contents_js_requests = ["""
    const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://example.com/api?param1=value1&param2=value2&param3=value3');
xhr.onload = function() {
    if (xhr.status === 200) {
        console.log(xhr.responseText);
    }
};
xhr.send();
    """,
    """
const xhr = new XMLHttpRequest();
xhr.open('POST', 'https://example.com/api');
xhr.setRequestHeader('Content-Type', 'application/json');
const data = { param4: 'value1', param5: 'value2' };
xhr.send(JSON.stringify(data));
xhr.onload = function() {
    if (xhr.status === 200) {
        console.log(xhr.responseText);
    }
};
""",
    """ 
    fetch('https://example.com/api?bbb=value1&cccc2=value2')
       .then(response => response.json())
       .then(data => console.log(data))
       .catch(error => console.error('Error:', error));
    """,
    """ 
    fetch('https://example.com/api', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ ppppp: 'value1', dddd: 'value2' })
})
    """,
    """ 
```javascript
$.ajax({
    url: 'https://example.com/api',
    method: 'POST',
    data: {
        eeee: 'value1',
        gggg: 'value2'
    },
    success: function(data) {
        console.log(data);
    },
    error: function(error) {
        console.error(error);
    }
});    
    """]

demo_contents_html_input = [
    """ 
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Example</title>
</head>
<body>
    <form action="/submit" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br>

        <label for="age">Age:</label>
        <input type="number" id="age" name="age">
        <br>

        <label for="subscribe">Subscribe to newsletter:</label>
        <input type="checkbox" id="subscribe" name="subscribe" value="yes">
        <br>

        <input type="submit" value="Submit">
    </form>
</body>
</html>
    """
]
demo_contents_log = [""" 
2024-09-28 22:31:10,732 - INFO - https://www.bing.com/fd/ls/l?IG=41F99C701D1C4F1392E6BC40F41DBD70&TYPE=Event.TabFocusChanged&DATA=%5B%7B%22T%22%3A%22CI.TabFocusChanged%22%2C%22TS%22%3A1727533870563%2C%22Name%22%3A%22visible%22%2C%22FID%22%3A%22TabFocused%22%7D%5D
2024-09-28 22:31:10,733 - INFO - Extracted parameters: None
2024-09-28 22:31:11,553 - INFO - https://www.bing.com/fd/ls/lsp.aspx
2024-09-28 22:31:11,553 - INFO - Extracted parameters: None
2024-09-28 22:31:12,029 - INFO - https://www.bing.com/osjson.aspx?query=&language=zh-CN&PC=U316
2024-09-28 22:31:12,029 - INFO - Extracted parameters: None
2024-09-28 22:31:12,144 - INFO - Extracted parameters: None
2024-09-28 22:31:12,840 - INFO - https://www.baidu.com/
2024-09-28 22:31:12,840 - INFO - Extracted parameters: None
2024-09-28 22:31:13,026 - INFO - Extracted parameters: None
2024-09-28 22:31:13,603 - INFO - https://www.baidu.com/sugrec?&prod=pc_his&from=pc_web&json=1&sid=60825&hisdata=&_t=1727533873598&req=2&csor=0
2024-09-28 22:31:13,603 - INFO - Extracted parameters: None
2024-09-28 22:31:13,662 - INFO - Extracted parameters: None
2024-09-28 22:31:13,718 - INFO - https://mbd.baidu.com/ztbox?action=zpblog&appname=pcsearch&v=2.0&data=%7B%22cateid%22%3A%2299%22%2C%22actiondata%22%3A%7B%22id%22%3A18463%2C%22type%22%3A%220%22%2C%22timestamp%22%3A1727533873570%2C%22content%22%3A%7B%22page%22%3A%22home%22%2C%22source%22%3A%22%22%2C%22from%22%3A%22search%22%2C%22type%22%3A%22display%22%2C%22ext%22%3A%7B%7D%7D%7D%7D
2024-09-28 22:31:13,718 - INFO - Extracted parameters: None
2024-09-28 22:31:13,841 - INFO - https://sp1.baidu.com/-L-Xsjip0QIZ8tyhnq/v.gif?logactid=1234567890&showTab=10000&opType=showpv&mod=superman%3Alib&submod=index&superver=supernewplus&glogid=2148355645&type=2011&pid=315&isLogin=0&version=PCHome&terminal=PC&qid=0xcb0d966e000d4e3d&sid=&super_frm=&from_login=&from_reg=&query=&curcard=2&curcardtab=&_r=0.874912750795479
2024-09-28 22:31:13,842 - INFO - Extracted parameters: None
2024-09-28 22:31:13,844 - INFO - https://sp1.baidu.com/-L-Xsjip0QIZ8tyhnq/v.gif?logactid=1234567890&showTab=10000&opType=nodepv&mod=superman%3Alib&submod=index&superver=supernewplus&glogid=2148355645&type=2011&pid=315&isLogin=0&version=PCHome&terminal=PC&qid=0xcb0d966e000d4e3d&sid=&super_frm=&from_login=&from_reg=&query=&curcard=2&curcardtab=&_r=0.06389833235671416
2024-09-28 22:31:13,844 - INFO - Extracted parameters: None
    """]

demo_contents_js = [""" 
var passport=passport||window.passport||{};passport._modulePool=passport._modulePool||{},passport._define=passport._define||function(s,a){passport._modulePool[s]=a&&a()},passport._getModule=passport._getModule||function(s){return passport._modulePool[s]},window.upsmsStore={reg_upsms:"106929130003000002",verify_upsms:"106929130003000004",verify_text_upsms:"1069 2913 0003 000 004"},window.YY_TPL_CONFIG="yylive,yyliveserver,yyanchor,pcyy,yyudbsec,bdgameassist,yoyuyin,";try{if(window.localStorage&&window.localStorage.getItem("upsms-pcApi"))try{window.upsmsStore=JSON.parse(window.localStorage.getItem("upsms-pcApi"))}catch(e){}}catch(e){}var passport=window.passport||{};passport._load=passport._load||function(s,a,e){var t=document,n=t.createElement("SCRIPT");if(a){n.type="text/javascript",n.charset="UTF-8";var p=s.split("?")[0],o=Math.round(1e3*Math.random()),i=(new Date).getTime();n.readyState?n.onreadystatechange=function(){if("loaded"===n.readyState||"complete"===n.readyState){if(n.onreadystatechange=null,100===o){var s=(new Date).getTime()-i;(new Image).src=document.location.protocol+"//nsclick.baidu.com/v.gif?pid=111&type=1023&url="+encodeURIComponent(p)+"&time="+s}e&&e()}}:n.onload=function(){if(100===o){var s=(new Date).getTime()-i;(new Image).src=document.location.protocol+"//nsclick.baidu.com/v.gif?pid=111&type=1023&url="+encodeURIComponent(p)+"&time="+s}e&&e()},n.src=100===o?p+"?t="+Math.random():s,t.getElementsByTagName("head")[0].appendChild(n)}else n.type="text/javascript",n.charset="UTF-8",n.src=s,t.getElementsByTagName("head")[0].appendChild(n),n.readyState?n.onreadystatechange=function(){("loaded"===n.readyState||"complete"===n.readyState)&&(n.onreadystatechange=null,e&&e())}:n.onload=function(){e&&e()}},passport.ieVersion=function(){var s;try{var a=navigator.userAgent.toLowerCase(),e=a.indexOf("msie")>-1;e&&a.match(/msie ([\d.]+)/)&&(s=a.match(/msie ([\d.]+)/)[1])}catch(t){s=0}return s},passport.getDomain=function(){var s={"http:":"http://ppui-static-pc.cdn.bcebos.com","https:":"https://ppui-static-pc.cdn.bcebos.com"};passport.ieVersion()<=8&&(s={"http:":"http://passport.baidu.com","https:":"https://passport.baidu.com"});var a;return a=passport&&"https"===passport._protocol?"https:":window.location?window.location.protocol.toLowerCase():document.location.protocol.toLowerCase(),s[a]||s["https:"]},passport._use=passport._use||function(s,a,e){function t(){passport._load("https://wappass.baidu.com/static/waplib/moonshad.js?tt="+(new Date).getTime(),!0,function(){var s=passport._getModule(p);if(!s)throw new Error("load "+p+"module script error.");e&&e(s)})}var n=passport.getDomain()+a,p=s+".js",o=passport._getModule(p);o?e&&e(o):passport._load(n,!0,t)},passport.loadPass=function(s,a){var e=passport.getDomain()+s,t=document.createElement("link");t.rel="stylesheet",t.type="text/css",t.href=e,document.getElementsByTagName("head")[0].appendChild(t),t.readyState?t.onreadystatechange=function(){("loaded"==t.readyState||"complete"==t.readyState)&&(t.onreadystatechange=null,a&&a())}:t.onload=function(){a&&a()}},passport.use=passport.use||function(s,a,e){var t=a&&a.tangram===!1?"":"_tangram";a&&a.protocol&&(passport._protocol=a.protocol),"reg"===s&&a&&a.regPhoneOnly&&(s="regPhone");var n,p,o,i="login"===s&&a&&a.loginVersion&&"v4"===a.loginVersion,r="login"===s&&a&&a.loginVersion&&"v5"===a.loginVersion;r?(o="/passApi/css/loginv5_6871e8a.css",p="/passApi/js/loginv5_tangram_323a2d3.js",n="/passApi/js/loginv5_f4a5816.js"):i?(o="/passApi/css/loginv4_7b5ffbb.css",p="/passApi/js/loginv4_tangram_8774221.js",n="/passApi/js/loginv4_ad1ccce.js"):(o="/passApi/css/uni_login_merge_40e1964.css",p="/passApi/js/login_tangram_d43fd90.js",n="/passApi/js/login_7366a76.js");var c={login:n,login_tangram:p,smsloginEn:"/passApi/js/smsloginEn_c1bd98c.js",smsloginEn_tangram:"/passApi/js/smsloginEn_tangram_f664dd8.js",loginWLtoPC:"/passApi/js/loginWLtoPC_9ee0278.js",accConnect:"/passApi/js/accConnect_7d975b2.js",accConnect_tangram:"/passApi/js/accConnect_tangram_4f7c863.js",accRealName:"/passApi/js/accRealName_ea2a8fa.js",accRealName_tangram:"/passApi/js/accRealName_tangram_ff869dd.js",checkPhone:"/passApi/js/checkPhone_2f6ed25.js",checkPhone_tangram:"/passApi/js/checkPhone_tangram_0f9670a.js",checkIDcard:"/passApi/js/checkIDcard_ee95aa8.js",checkIDcard_tangram:"/passApi/js/checkIDcard_tangram_a74e79a.js",travelComplete:"/passApi/js/travelComplete_02f64ad.js",travelComplete_tangram:"/passApi/js/travelComplete_tangram_542b124.js",bindGuide:"/passApi/js/bindGuide_9019191.js",bindGuide_tangram:"/passApi/js/bindGuide_tangram_83f1373.js",accSetPwd:"/passApi/js/accSetPwd_29cfd1a.js",accSetPwd_tangram:"/passApi/js/accSetPwd_tangram_2407659.js",IDCertify:"/passApi/js/IDCertify_c730e8b.js",IDCertify_tangram:"/passApi/js/IDCertify_tangram_1c359a0.js",secondCardList:"/passApi/js/secondCardList_de40440.js",secondCardList_tangram:"/passApi/js/secondCardList_tangram_02f8bc1.js",secondCardVerify:"/passApi/js/secondCardVerify_203b20e.js",secondCardVerify_tangram:"/passApi/js/secondCardVerify_tangram_f7d218e.js",IDCertifyQrcode:"/passApi/js/IDCertifyQrcode_f8d004d.js",IDCertifyQrcode_tangram:"/passApi/js/IDCertifyQrcode_tangram_0ac77aa.js",loadingApi:"/passApi/js/loadingApi_7044589.js",loadingApi_tangram:"/passApi/js/loadingApi_tangram_b26de94.js",loginWap:"/passApi/js/loginWap_61eb9c9.js",reg:"/passApi/js/reg_94cc2e5.js",reg_tangram:"/passApi/js/reg_tangram_8e023af.js",regPhone:"/passApi/js/regPhone_1664037.js",regPhone_tangram:"/passApi/js/regPhone_tangram_6345b60.js",fillUserName:"/passApi/js/fillUserName_850c5c7.js",fillUserName_tangram:"/passApi/js/fillUserName_tangram_4b74dc9.js",qrcode:"/passApi/js/qrcode_a405554.js",qrcode_tangram:"/passApi/js/qrcode_tangram_f0d728a.js",realUserTag:"/passApi/js/realUserTag_074a49c.js",realUserTag_tangram:"/passApi/js/realUserTag_tangram_1b3fb9c.js",bind:"/passApi/js/bind_383797b.js",bind_tangram:"/passApi/js/bind_tangram_82989f0.js",multiBind:"/passApi/js/multiBind_8622611.js",multiBind_tangram:"/passApi/js/multiBind_tangram_d74a9ef.js",multiUnbind:"/passApi/js/multiUnbind_424e3c9.js",multiUnbind_tangram:"/passApi/js/multiUnbind_tangram_361d7e9.js",changeUser:"/passApi/js/changeUser_bf67558.js",changeUser_tangram:"/passApi/js/changeUser_tangram_21109ac.js",loginMultichoice:"/passApi/js/loginMultichoice_55dd458.js",loginMultichoice_tangram:"/passApi/js/loginMultichoice_tangram_9a1a52b.js",confirmWidget:"/passApi/js/confirmWidget_ece8ce0.js",confirmWidget_tangram:"/passApi/js/confirmWidget_tangram_8170b43.js",uni_rebindGuide:"/passApi/js/uni_rebindGuide_9e22e37.js",uni_rebindGuide_tangram:"/passApi/js/uni_rebindGuide_tangram_a0d5501.js",ucTravelComplete:"/passApi/js//ucTravelComplete.js",ucTravelComplete_tangram:"/passApi/js/ucTravelComplete_tangram_5f7a98b.js"},d={login:o,ucTravelComplete:"/passApi/css/ucTravelComplete_329b943.css"},l=s+t;2===arguments.length&&(e=a),a&&a.tangramInst&&(passport.tangramInst=a.tangramInst),a&&a.defaultCss&&d[s]?passport.loadPass(d[s],function(){passport._use(l,c[l],e)}):passport._use(l,c[l],e)};
"""]

# 常见的HTTP 请求头部
HTTP_HEADERS = [
    "Authorization: Bearer",
    "Accept",
    "Accept-Application",
    "Accept-Charset",
    "Accept-Datetime",
    "Accept-Encoding",
    "Accept-Encodxng",
    "Accept-Language",
    "Accept-Ranges",
    "Accept-Version",
    "Access-Control-Allow-Credentials",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods",
    "Access-Control-Allow-Origin",
    "Access-Control-Expose-Headers",
    "Access-Control-Max-Age",
    "Access-Control-Request-Headers",
    "Access-Control-Request-Method",
    "Access-Token",
    "Accesskey",
    "Action",
    "Age",
    "Ajax",
    "Allow",
    "App",
    "App-Env",
    "App-Key",
    "Appcookie",
    "Appname",
    "Appversion",
    "Atcept-Language",
    "Auth",
    "Auth-Any",
    "Auth-Basic",
    "Auth-Digest",
    "Auth-Digest-Ie",
    "Auth-Gssneg",
    "Auth-Key",
    "Auth-Ntlm",
    "Auth-Password",
    "Auth-Realm",
    "Auth-Type",
    "Auth-User",
    "Authentication",
    "Authorization",
    "Bad-Gateway",
    "Bad-Request",
    "Base",
    "Base-Url",
    "Basic",
    "Bearer-Indication",
    "Body-Maxlength",
    "Body-Truncated",
    "Browser-User-Agent",
    "Cache-Control",
    "Cache-Info",
    "Case-Files",
    "Catalog",
    "Catalog-Server",
    "Category",
    "Cert-Cookie",
    "Cert-Flags",
    "Cert-Issuer",
    "Cert-Keysize",
    "Cert-Secretkeysize",
    "Cert-Serialnumber",
    "Cert-Server-Issuer",
    "Cert-Server-Subject",
    "Cert-Subject",
    "Cf-Connecting-Ip",
    "Cf-Ipcountry",
    "Cf-Template-Path",
    "Cf-Visitor",
    "Ch",
    "Challenge-Response",
    "Charset",
    "chunked",
    "Chunk-Size",
    "Client",
    "Client-Address",
    "Client-Bad-Request",
    "Client-Conflict",
    "Client-Error-Cannot-Access-Local-File",
    "Client-Error-Cannot-Connect",
    "Client-Error-Communication-Failure",
    "Client-Error-Connect",
    "Client-Error-Invalid-Parameters",
    "Client-Error-Invalid-Server-Address",
    "Client-Error-No-Error",
    "Client-Error-Protocol-Failure",
    "Client-Error-Unspecified-Error",
    "Client-Expectation-Failed",
    "Client-Forbidden",
    "Client-Gone",
    "Client-Ip",
    "Client-IP",
    "Client-Length-Required",
    "Client-Method-Not-Allowed",
    "Client-Not-Acceptable",
    "Client-Not-Found",
    "Client-Payment-Required",
    "Client-Precondition-Failed",
    "Client-Proxy-Auth-Required",
    "Client-Quirk-Mode",
    "Client-Request-Timeout",
    "Client-Request-Too-Large",
    "Client-Request-Uri-Too-Large",
    "Client-Requested-Range-Not-Possible",
    "Client-Unauthorized",
    "Client-Unsupported-Media-Type",
    "Clientaddress",
    "Clientip",
    "Cloudfront-Viewer-Country",
    "Cloudinary-Name",
    "Cloudinary-Public-Id",
    "Cloudinary-Version",
    "Cloudinaryurl",
    "Cluster-Client-IP",
    "Code",
    "Coming-From",
    "Compress",
    "Conflict",
    "Connection",
    "Connection-Type",
    "Contact",
    "Content",
    "Content-Disposition",
    "Content-Encoding",
    "Content-Language",
    "Content-Length",
    "Content-Location",
    "Content-MD5",
    "Content-Md5",
    "Content-Range",
    "Content-Security-Policy",
    "Content-Security-Policy-Report-Only",
    "Content-Type",
    "Content-Type-Xhtml",
    "Context-Path",
    "Continue",
    "Cookie",
    "Cookie-Domain",
    "Cookie-Httponly",
    "Cookie-Parse-Raw",
    "Cookie-Path",
    "Cookie-Secure",
    "Cookie-Vars",
    "Cookie2",
    "Cookies",
    "Core-Base",
    "Correlates",
    "Created",
    "Credentials-Filepath",
    "Curl",
    "Curl-Multithreaded",
    "Custom-Header",
    "Custom-Secret-Header",
    "Dataserviceversion",
    "Date",
    "Debug",
    "Deflate-Level-Def",
    "Deflate-Level-Max",
    "Deflate-Level-Min",
    "Deflate-Strategy-Def",
    "Deflate-Strategy-Filt",
    "Deflate-Strategy-Fixed",
    "Deflate-Strategy-Huff",
    "Deflate-Strategy-Rle",
    "Deflate-Type-Gzip",
    "Deflate-Type-Raw",
    "Deflate-Type-Zlib",
    "Delete",
    "Depth",
    "Destination",
    "Destroy",
    "Devblocksproxybase",
    "Devblocksproxyhost",
    "Devblocksproxyssl",
    "Device-Stock-Ua",
    "Digest",
    "Dir",
    "Dir-Name",
    "Dir-Resource",
    "Disable-Gzip",
    "Dkim-Signature",
    "DNT",
    "Dnt",
    "Download-Attachment",
    "Download-Bad-Url",
    "Download-Bz2",
    "Download-Cut-Short",
    "Download-E-Headers-Sent",
    "Download-E-Invalid-Archive-Type",
    "Download-E-Invalid-Content-Type",
    "Download-E-Invalid-File",
    "Download-E-Invalid-Param",
    "Download-E-Invalid-Request",
    "Download-E-Invalid-Resource",
    "Download-E-No-Ext-Mmagic",
    "Download-E-No-Ext-Zlib",
    "Download-Inline",
    "Download-Mime-Type",
    "Download-No-Server",
    "Download-Size",
    "Download-Status-Not-Found",
    "Download-Status-Server-Error",
    "Download-Status-Unauthorized",
    "Download-Status-Unknown",
    "Download-Tar",
    "Download-Tgz",
    "Download-Url",
    "Download-Zip",
    "E-Encoding",
    "E-Header",
    "E-Invalid-Param",
    "E-Malformed-Headers",
    "E-Message-Type",
    "E-Querystring",
    "E-Request",
    "E-Request-Method",
    "E-Request-Pool",
    "E-Response",
    "E-Runtime",
    "E-Socket",
    "E-Url",
    "Enable-Gzip",
    "Enable-No-Cache-Headers",
    "Encoding-Stream-Flush-Full",
    "Encoding-Stream-Flush-None",
    "Encoding-Stream-Flush-Sync",
    "Env-Silla-Environment",
    "Env-Vars",
    "Error",
    "Error-1",
    "Error-2",
    "Error-3",
    "Error-4",
    "Error-Formatting-Html",
    "Espo-Authorization",
    "Espo-Cgi-Auth",
    "Etag",
    "Eve-Charid",
    "Eve-Charname",
    "Eve-Solarsystemid",
    "Eve-Solarsystemname",
    "Eve-Trusted",
    "Ex-Copy-Movie",
    "Expect",
    "Expectation-Failed",
    "Expires",
    "Ext",
    "Failed-Dependency",
    "Fake-Header",
    "Fastly-Client-Ip",
    "Fb-Appid",
    "Fb-Secret",
    "File-Not-Found",
    "Filename",
    "Files",
    "Files-Vars",
    "Fire-Breathing-Dragon",
    "Foo",
    "Foo-Bar",
    "Forbidden",
    "Force-Language",
    "Force-Local-Xhprof",
    "Format",
    "Forwarded",
    "Forwarded-For",
    "Forwarded-For-Ip",
    "Forwarded-Proto",
    "From",
    "Fromlink",
    "Front-End-Https",
    "Gateway-Interface",
    "Gateway-Time-Out",
    "Get",
    "Get-Vars",
    "Givenname",
    "Global-All",
    "Global-Cookie",
    "Global-Get",
    "Global-Post",
    "Gone",
    "Google-Code-Project-Hosting-Hook-Hmac",
    "Gzip-Level",
    "H0st",
    "Head",
    "Header",
    "Header-Lf",
    "Header-Status-Client-Error",
    "Header-Status-Informational",
    "Header-Status-Redirect",
    "Header-Status-Server-Error",
    "Header-Status-Successful",
    "Home",
    "Host",
    "Host-Liveserver",
    "Host-Name",
    "Host-Unavailable",
    "Hosti",
    "Htaccess",
    "Http-Accept",
    "Http-Accept-Encoding",
    "Http-Accept-Language",
    "Http-Authorization",
    "Http-Connection",
    "Http-Cookie",
    "Http-Host",
    "Http-Phone-Number",
    "Http-Referer",
    "Http-Url",
    "Http-User-Agent",
    "HTTP2-Settings",
    "Https",
    "Https-From-Lb",
    "Https-Keysize",
    "Https-Secretkeysize",
    "Https-Server-Issuer",
    "Https-Server-Subject",
    "If",
    "If-Match",
    "If-Modified-Since",
    "If-Modified-Since-Version",
    "If-None-Match",
    "If-Posted-Before",
    "If-Range",
    "If-Unmodified-Since",
    "If-Unmodified-Since-Version",
    "Image",
    "Images",
    "Incap-Client-Ip",
    "Info",
    "Info-Download-Size",
    "Info-Download-Time",
    "Info-Return-Code",
    "Info-Total-Request-Stat",
    "Info-Total-Response-Stat",
    "Insufficient-Storage",
    "Internal-Server-Error",
    "Ipresolve-Any",
    "Ipresolve-V4",
    "Ipresolve-V6",
    "Ischedule-Version",
    "Iv-Groups",
    "Iv-User",
    "Javascript",
    "Jenkins",
    "Keep-Alive",
    "Kiss-Rpc",
    "Label",
    "Large-Allocation",
    "Last-Event-Id",
    "Last-Modified",
    "Length-Required",
    "Link",
    "Local-Addr",
    "Local-Content-Sha1",
    "Local-Dir",
    "Location",
    "Lock-Token",
    "Locked",
    "Mail",
    "Mandatory",
    "Max-Conn",
    "Max-Forwards",
    "Max-Request-Size",
    "Max-Uri-Length",
    "Maxdataserviceversion",
    "Message",
    "Message-B",
    "Meth-Acl",
    "Meth-Baseline-Control",
    "Meth-Checkin",
    "Meth-Checkout",
    "Meth-Connect",
    "Meth-Copy",
    "Meth-Delete",
    "Meth-Get",
    "Meth-Head",
    "Meth-Label",
    "Meth-Lock",
    "Meth-Merge",
    "Meth-Mkactivity",
    "Meth-Mkcol",
    "Meth-Mkworkspace",
    "Meth-Move",
    "Meth-Options",
    "Meth-Post",
    "Meth-Propfind",
    "Meth-Proppatch",
    "Meth-Put",
    "Meth-Report",
    "Meth-Trace",
    "Meth-Uncheckout",
    "Meth-Unlock",
    "Meth-Update",
    "Meth-Version-Control",
    "Method",
    "Method-Not-Allowed",
    "Mimetype",
    "Mod-Env",
    "Mod-Rewrite",
    "Mod-Security-Message",
    "Modauth",
    "Mode",
    "Module-Class",
    "Module-Class-Path",
    "Module-Name",
    "Moved-Permanently",
    "Moved-Temporarily",
    "Ms-Asprotocolversion",
    "Msg-None",
    "Msg-Request",
    "Msg-Response",
    "Msisdn",
    "Multi-Status",
    "Multipart-Boundary",
    "Multiple-Choices",
    "Must",
    "My-Header",
    "Mysqlport",
    "Native-Sockets",
    "Negotiate",
    "Nl",
    "No-Content",
    "Non-Authoritative",
    "Nonce",
    "Not-Acceptable",
    "Not-Exists",
    "Not-Extended",
    "Not-Found",
    "Not-Implemented",
    "Not-Modified",
    "Notification-Template",
    "Oc-Chunked",
    "Ocs-Apirequest",
    "Ok",
    "On-Behalf-Of",
    "Onerror-Continue",
    "Onerror-Die",
    "Onerror-Return",
    "Only",
    "Opencart",
    "Options",
    "Organizer",
    "Orig_path_info",
    "Origin",
    "Originator",
    "Overwrite",
    "Params-Allow-Comma",
    "Params-Allow-Failure",
    "Params-Default",
    "Params-Get-Catid",
    "Params-Get-Currentday",
    "Params-Get-Disposition",
    "Params-Get-Downwards",
    "Params-Get-Givendate",
    "Params-Get-Lang",
    "Params-Get-Type",
    "Params-Raise-Error",
    "Partial-Content",
    "Passkey",
    "Password",
    "Path",
    "Path-Base",
    "Path-Info",
    "Path-Themes",
    "Path-Translated",
    "Payment-Required",
    "Pc-Remote-Addr",
    "Permanent",
    "Phone-Number",
    "Php",
    "Php-Auth-Pw",
    "Php-Auth-User",
    "Phpthreads",
    "Pink-Pony",
    "Port",
    "Portsensor-Auth",
    "Post",
    "Post-Error",
    "Post-Files",
    "Post-Vars",
    "Postredir-301",
    "Postredir-302",
    "Postredir-All",
    "Pragma",
    "Pragma-No-Cache",
    "Precondition-Failed",
    "Prefer",
    "Processing",
    "Profile",
    "Protocol",
    "Protocols",
    "Proxy",
    "Proxy-Agent",
    "Proxy-Authenticate",
    "Proxy-Authentication-Required",
    "Proxy-Authorization",
    "Proxy-Connection",
    "Proxy-Host",
    "Proxy-Http",
    "Proxy-Http-1-0",
    "Proxy-Password",
    "Proxy-Port",
    "Proxy-Pwd",
    "Proxy-Request-Fulluri",
    "Proxy-Socks4",
    "Proxy-Socks4a",
    "Proxy-Socks5",
    "Proxy-Socks5-Hostname",
    "Proxy-Url",
    "Proxy-User",
    "Public-Key-Pins",
    "Public-Key-Pins-Report-Only",
    "Pull",
    "Put",
    "Query-String",
    "Querystring",
    "Querystring-Type-Array",
    "Querystring-Type-Bool",
    "Querystring-Type-Float",
    "Querystring-Type-Int",
    "Querystring-Type-Object",
    "Querystring-Type-String",
    "Range",
    "Range-Not-Satisfiable",
    "Raw-Post-Data",
    "Read-State-Begin",
    "Read-State-Body",
    "Read-State-Headers",
    "Real-Ip",
    "Real-Method",
    "Reason",
    "Reason-Phrase",
    "Recipient",
    "Redirect",
    "Redirect-Found",
    "Redirect-Perm",
    "Redirect-Post",
    "Redirect-Problem-Withoutwww",
    "Redirect-Problem-Withwww",
    "Redirect-Proxy",
    "Redirect-Temp",
    "Redirected-Accept-Language",
    "Redirection-Found",
    "Redirection-Multiple-Choices",
    "Redirection-Not-Modified",
    "Redirection-Permanent",
    "Redirection-See-Other",
    "Redirection-Temporary",
    "Redirection-Unused",
    "Redirection-Use-Proxy",
    "Ref",
    "Referer",
    "Referrer",
    "Referrer-Policy",
    "Refferer",
    "Refresh",
    "Remix-Hash",
    "Remote-Addr",
    "Remote-Host",
    "Remote-Host-Wp",
    "Remote-User",
    "Remote-Userhttps",
    "Report-To",
    "Request",
    "Request-Entity-Too-Large",
    "Request-Error",
    "Request-Error-File",
    "Request-Error-Gzip-Crc",
    "Request-Error-Gzip-Data",
    "Request-Error-Gzip-Method",
    "Request-Error-Gzip-Read",
    "Request-Error-Proxy",
    "Request-Error-Redirects",
    "Request-Error-Response",
    "Request-Error-Url",
    "Request-Http-Ver-1-0",
    "Request-Http-Ver-1-1",
    "Request-Mbstring",
    "Request-Method",
    "Request-Method-Delete",
    "Request-Method-Get",
    "Request-Method-Head",
    "Request-Method-Options",
    "Request-Method-Post",
    "Request-Method-Put",
    "Request-Method-Trace",
    "Request-Time-Out",
    "Request-Timeout",
    "Request-Uri",
    "Request-Uri-Too-Large",
    "Request-Vars",
    "Request2-Tests-Base-Url",
    "Request2-Tests-Proxy-Host",
    "Requesttoken",
    "Reset-Content",
    "Response",
    "Rest-Key",
    "Rest-Sign",
    "Retry-After",
    "Returned-Error",
    "Rlnclientipaddr",
    "Root",
    "Safe-Ports-List",
    "Safe-Ports-Ssl-List",
    "Save-Data",
    "Schedule-Reply",
    "Scheme",
    "Script-Name",
    "Sec-Websocket-Accept",
    "Sec-Websocket-Extensions",
    "Sec-Websocket-Key",
    "Sec-Websocket-Key1",
    "Sec-Websocket-Key2",
    "Sec-Websocket-Origin",
    "Sec-Websocket-Protocol",
    "Sec-Websocket-Version",
    "Secretkey",
    "See-Other",
    "Self",
    "Send-X-Frame-Options",
    "Server",
    "Server-Bad-Gateway",
    "Server-Error",
    "Server-Gateway-Timeout",
    "Server-Internal",
    "Server-Name",
    "Server-Not-Implemented",
    "Server-Port",
    "Server-Port-Secure",
    "Server-Protocol",
    "Server-Service-Unavailable",
    "Server-Software",
    "Server-Unsupported-Version",
    "Server-Vars",
    "Server-Varsabantecart",
    "Service-Unavailable",
    "Session-Id-Tag",
    "Session-Vars",
    "Set-Cookie",
    "Set-Cookie2",
    "Shib-Application-Id",
    "Shib-Identity-Provider",
    "Shib-Logouturl",
    "Shopilex",
    "Slug",
    "Sn",
    "Soapaction",
    "Socket-Connection-Err",
    "Socketlog",
    "Somevar",
    "Sourcemap",
    "Sp-Client",
    "Sp-Host",
    "Ssl",
    "Ssl-Https",
    "Ssl-Offloaded",
    "Ssl-Session-Id",
    "Ssl-Version-Any",
    "Sslsessionid",
    "Start",
    "Status",
    "Status-403",
    "Status-403-Admin-Del",
    "Status-404",
    "Status-Bad-Request",
    "Status-Code",
    "Status-Forbidden",
    "Status-Ok",
    "Status-Platform-403",
    "Str-Match",
    "Strict-Transport-Security",
    "Success-Accepted",
    "Success-Created",
    "Success-No-Content",
    "Success-Non-Authoritative",
    "Success-Ok",
    "Success-Partial-Content",
    "Success-Reset-Content",
    "Support",
    "Support-Encodings",
    "Support-Events",
    "Support-Magicmime",
    "Support-Requests",
    "Support-Sslrequests",
    "Surrogate-Capability",
    "Switching-Protocols",


    "TE",
    "Te",
    "Ticket",
    "Time-Out",
    "Timeout",
    "Timing-Allow-Origin",
    "Token",
    "Trailer",
    "Transfer-Encoding",
    "Translate",
    "True-Client-Ip",
    "True-Client-IP",
    "Upgrade",
    "Upgrade-Insecure-Requests",
    "Upgrade-Required",
    "Uri",
    "Url",
    "Url-From-Env",
    "Url-Join-Path",
    "Url-Join-Query",
    "Url-Replace",
    "Url-Sanitize-Path",
    "Use-Gzip",
    "Use-Proxy",
    "User",
    "User-Agent",
    "User-Agent-Via",
    "User-Email",
    "User-Id",
    "User-Mail",
    "User-Name",
    "User-Photos",
    "Useragent",
    "Useragent-Via",
    "Vary",
    "Verbose",
    "Version",
    "Via",
    "Wap-Connection",
    "Www-Address",
    "Www-Authenticate",
    "X-Access-Token",
    "X-Api-Key",
    "X-Api-Signature",
    "X-Api-Timestamp",
    "X-Apitoken",
    "X-Auth-Key",
    "X-Auth-Mode",
    "X-Auth-Password",
    "X-Auth-Service-Provider",
    "X-Auth-Token",
    "X-Auth-User",
    "X-Auth-Userid",
    "X-Auth-Username",
    "X-Authentication",
    "X-Authentication-Key",
    "X-Authorization",
    "X-Browser-Height",
    "X-Browser-Width",
    "X-Cascade",
    "X-Cf-Url",
    "X-Chrome-Extension",
    "X-Client-Host",
    "X-Client-Id",
    "X-Client-Ip",
    "X-Client-IP",
    "X-Client-Key",
    "X-Client-Os",
    "X-Client-Os-Ver",
    "X-Clientip",
    "X-Cluster-Client-Ip",
    "X-Confirm-Delete",
    "X-Content-Type",
    "X-Content-Type-Options",
    "X-Correlation-ID",
    "X-Credentials-Request",
    "X-Csrf-Crumb",
    "X-Csrf-Token",
    "X-Csrftoken",
    "X-Custom",
    "X-Debug-Test",
    "X-Device-User-Agent",
    "X-Dialog",
    "X-Dns-Prefetch-Control",
    "X-Do-Not-Track",
    "X-Environment-Override",
    "X-File-Id",
    "X-File-Name",
    "X-File-Resume",
    "X-File-Size",
    "X-File-Type",
    "X-Filename",
    "X-Flash-Version",
    "X-Foo",
    "X-Foo-Bar",
    "X-Forward-For",
    "X-Forward-Proto",
    "X-Forwarded",
    "X-Forwarded-By",
    "X-Forwarded-For",
    "X-Forwarded-For-Original",
    "X-Forwarded-Host",
    "X-Forwarded-Port",
    "X-Forwarded-Proto",
    "X-Forwarded-Protocol",
    "X-Forwarded-Scheme",
    "X-Forwarded-Server",
    "X-Forwarded-Ssl",
    "X-Forwarder-For",
    "X-From",
    "X-Geoip-Country",
    "X-Get-Checksum",
    "X-Host",
    "X-Http-Destinationurl",
    "X-Http-Host-Override",
    "X-Http-Method",
    "X-Http-Method-Override",
    "X-Http-Path-Override",
    "X-Https",
    "X-If-Unmodified-Since",
    "X-Ip",
    "X-Json",
    "X-Locking",
    "X-Machine",
    "X-Mandrill-Signature",
    "X-Method-Override",
    "X-Mobile-Gateway",
    "X-Mobile-Ua",
    "X-Moz",
    "X-Ms-Policykey",
    "X-Network-Info",
    "X-Options",
    "X-Orig-Client",
    "X-Original-Host",
    "X-Original-Http-Command",
    "X-Original-Remote-Addr",
    "X-Original-Url",
    "X-Original-User-Agent",
    "X-Originally-Forwarded-For",
    "X-Originally-Forwarded-Proto",
    "X-Originating-Ip",
    "X-Originating-IP",
    "X-Password",
    "X-Prototype-Version",
    "X-Proxy-Url",
    "X-Pswd",
    "X-Purpose",
    "X-Real-Ip",
    "X-Remote-Addr",
    "X-Remote-IP",
    "X-Remote-Protocol",
    "X-Render-Partial",
    "X-Request",
    "X-Request-ID",
    "X-Request-Id",
    "X-Request-Signature",
    "X-Request-Start",
    "X-Request-Timestamp",
    "X-Requested-With",
    "X-Response-Format",
    "X-Rest-Cors",
    "X-Rest-Password",
    "X-Rest-Username",
    "X-Rewrite-Url",
    "X-Scanner",
    "X-Scheme",
    "X-Screen-Height",
    "X-Screen-Width",
    "X-Sendfile-Type",
    "X-Serial-Number",
    "X-Serialize",
    "X-Server-Id",
    "X-Server-Name",
    "X-Server-Port",
    "X-Signature",
    "X-Ssl",
    "X-Subdomain",
    "X-Timer",
    "X-Tomboy-Client",
    "X-Tor",
    "X-Twilio-Signature",
    "X-Ua-Device",
    "X-Update",
    "X-Update-Range",
    "X-Upload-Maxresolution",
    "X-Upload-Name",
    "X-Upload-Size",
    "X-Upload-Type",
    "X-Url-Scheme",
    "X-User",
    "X-User-Agent",
    "X-Username",
    "X-Varnish",
    "X-Wap-Client-Sdu-Size",
    "X-Wap-Clientid",
    "X-Wap-Gateway",
    "X-Wap-Profile",
    "X-Wap-Proxy-Cookie",
    "X-Wap-Session-Id",
    "X-Wikimedia-Debug",
    "X-Wp-Nonce",
    "X-Wp-Pjax-Prefetch",
    "X-Ws-Api-Key",
    "X-Xc-Schema-Version",
    "X-Xhprof-Debug",
    "X-Xhr-Referer",
    "X-Xmlhttprequest",
    "X-Xpid",
    "Accept-Patch",
    "Alt-Svc",
    "ETag",
    "IM",
    "P3P",
    "WWW-Authenticate",
    "X-Frame-Options",
    "X-HTTP-Method-Override",
    "x-wap-profile",
    "Cross-Origin-Resource-Policy",
    "Expect-CT",
    "Feature-Policy",
    "Sec-Fetch-Dest",
    "Sec-Fetch-Mode",
    "Sec-Fetch-Site",
    "Sec-Fetch-User",
    "Sec-WebSocket-Accept"
]

# 自定义的过滤的列表
BYPASS_LIST = [
    '_',
    ''
]


def is_valid_param_name(param_name):
    # 检查参数名是否符合规范（字母、数字、下划线）
    return bool(re.match(r'^[a-zA-Z_]\w*$', param_name))


def extract_params(contents: list, bypass_list: list = None) -> list:
    """ 从字符串列表中提取字可能的参数

    :param contents: 字符串列表
    :param bypass_list: 过滤指定的参数, 默认过滤 http 头部同名的参数
    :return: 参数字典列表
    """
    if not bypass_list:
        bypass_list = []

    if type(bypass_list) is not list:
        raise ValueError("提取参数函数中， 参数 bypass_list 过滤列表类型错误，应当为 list")

    bypass_list += BYPASS_LIST

    params_list = []

    # 1. 提取 {"": ""} 格式
    # 提取类似 {key:"value",key2:"value2"} 格式的内容
    for content in contents:
        json_matches = re.findall(r'\{([^{}]+)\}', content)
        for match in json_matches:
            key_value_pairs = re.findall(r'(\w+):"(.*?)"', match)
            for key, value in key_value_pairs:
                params_list.append({"param": key, "value": value[:50]})


    # 2. 匹配 URL 并提取查询参数

    for content in contents:
        # 匹配 URL 并提取查询参数
        urls = re.findall(r'https?://[^\s]+', content)
        for url in urls:
            # 提取查询参数
            query_string = re.search(r'\?([^#]*)', url)
            if query_string:
                # 使用正则匹配参数名和值
                params = re.findall(r'([^&=]+)=?([^&]*)', query_string.group(1))
                for key, value in params:
                    # 处理空值的情况
                    if value == '':
                        params_list.append({"param": key, "value": ""})  # 空值情况
                    else:
                        params_list.append({"param": key, "value": value[:50]})  # 限制长度为30个字符
            else:
                # 处理没有查询参数的情况（如果需要）
                params_list.append({"param": "", "value": ""})


    # 3. 匹配特定格式
    for content in contents:
        # 匹配 /index?name=格式
        path_param_matches = re.findall(r'/[^?\s]+(?:\?[^&\s]+)?', content)
        for match in path_param_matches:
            parsed_url = urlparse(match)
            if parsed_url.query:
                query_params = parse_qs(parsed_url.query)
                for key, values in query_params.items():
                    for value in values:
                        params_list.append({"param": key, "value": value[:50]})

        # 匹配路径参数 /user:id 格式
        path_matches = re.findall(r'/([\w\d_]+):([\w\d_]+)', content)
        for key, value in path_matches:
            params_list.append({"param": value, "value": ''})

    # 遍历 params_list 过滤 不符合的命名规范的， 以及 HTTP_HEADERS = [] ，和 # 自定义的过滤的列表
    # BYPASS_LIST = [
    # ]

    # 过滤不符合命名规范、HTTP_HEADERS 和 BYPASS_LIST 中的参数
    filtered_params = [
        param for param in params_list
        if is_valid_param_name(param["param"]) and
           param["param"] not in HTTP_HEADERS and
           param["param"] not in bypass_list
    ]
    return filtered_params


if __name__ == '__main__':
    print("测试数据:")
    for param in extract_params(demo_contents_js):
        print(param)
    print("-"*30)
    for param in extract_params(demo_contents_url):
        print(param)
    print("-"*30)
    for param in extract_params(demo_contents_log):
        print(param)
    print("-"*30)
    for param in extract_params(demo_contents_html_input):
        print(param)
    print("-"*30)
    for param in extract_params(demo_contents_js_requests):
        print(param)
    print("-"*30)