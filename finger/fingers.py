# coding: utf-8
"""
    配置文件，填入文件指纹
    JSFileFinger，常见的js文件指纹
"""


class JSFileFinger:
    js_fingers = [
        {
            "name": "angular",
            "method": "reg",
            "operation": "&&",
            "rule": [r"AngularJS v\d{1,}.\d{1,}.\d{1,}\s.*\(c\) \d{4}-\d{4}"],
        },
        {
            "name": "backbone",
            "method": "reg",
            "operation": "&&",
            "rule": [r"Backbone.js \d{1,}\.\d{1,}\.\d{1,}\s\s//[ \t]+\(c\)|//@ sourceMappingURL=backbone-min.map"],
        },
        {
            "name": "bootstrap",
            "method": "reg",
            "operation": "&&",
            "rule": [r"[Bb]ootstrap-?\w{0,}\.js by @fat|[Bb]ootstrap-?\w{0,}\.js v\d{1,}\.\d{1,}\.\d{1,}|sourceMappingURL=bootstrap.min.js.map"],
        },
        {
            "name": "dojo",
            "method": "reg",
            "operation": "&&",
            "rule": [r"Copyright \(c\) \d{4}-\d{4}, The Dojo Foundation All Rights Reserved"],
        },
        {
            "name": "ext_core",
            "method": "reg",
            "operation": "&&",
            "rule": [r"Ext Core Library \d{1,}\.\d{0,}\.?\d{0,}\s"],
        },
        {
            "name": "highcharts",
            "method": "reg",
            "operation": "&&",
            "rule": [r"Highcharts JS v\d{1,}\.\d{0,}\.?\d{0,} \(\d{4}-\d{1,2}-\d{1,2}\)\s|theme for Highcharts JS\s"],
        },
        {
            "name": "highstock",
            "method": "reg",
            "operation": "&&",
            "rule": [r"Highstock JS v\d{1,}\.\d{0,}\.?\d{0,} \(\d{4}-\d{1,2}-\d{1,2}\)\s|Data plugin for Highcharts v\d{1,}\.\d{1,}\.?\d{0,}\s"],
        },
        {
            "name": "jquery",
            "method": "reg",
            "operation": "&&",
            "rule": [r"[jJ][qQ]uery v\d{1,}\.\d{1,}\.?\d{0,}.*\(c\) \d{0,4},[ ]?\d{0,4}[ ]?[jJ][qQ]uery|[jJ][qQ]uery JavaScript Library"],
        },
        {
            "name": "jquery_mobile",
            "method": "reg",
            "operation": "&&",
            "rule": [r"jQuery Mobile Framework Git Build|jQuery Mobile vGit Build|jQuery Mobile \d\.\d\.?\d{0,}\s.*Git"],
        },
        {
            "name": "jquery_ui",
            "method": "reg",
            "operation": "&&",
            "rule": [r"jQuery UI - v\d{1,}\.\d{1,}\.?\d{0,} - \d{4}-\d{1,2}-\d{1,2}"],
        },
        {
            "name": "jquery_cookie",
            "method": "reg",
            "operation": "&&",
            "rule": [r"jQuery Cookie Plugin v\d{1,}\.\d{1,}\.?\d{0,}$"],
        },
        {
            "name": "jquery_migrate",
            "method": "reg",
            "operation": "&&",
            "rule": [r"jQuery Migrate.*v\d{1,}\.\d{1,}\.?\d{0,}.*\d{4}-\d{1,2}-\d{1,2}$"],
        },
        {
            "name": "jquery_tools",
            "method": "reg",
            "operation": "&&",
            "rule": [r"jQuery Tools [v]?\d{1,}\.\d{1,}\.?\d{0,} - The missing UI library for the Web"],
        },
        {
            "name": "json2",
            "method": "reg",
            "operation": "&&",
            "rule": [r"\\u0000\\u00ad\\u0600-\\u0604\\u070f\\u17b4\\u17b5\\u200c-\\u200f\\u2028-\\u202f\\u2060-\\u206f\\ufeff\\ufff0-\\uffff"],
        },
        {
            "name": "lesscss",
            "method": "reg",
            "operation": "&&",
            "rule": [r"LESS - Leaner CSS v?\d{1,3}\.\d{1,3}\.?\d{0,3}"],
        },
        {
            "name": "mootools",
            "method": "reg",
            "operation": "&&",
            "rule": [r"[var |this\.]MooTools[ ]?=[ ]?{[\s]?[ ]{0,}\s?['\"]?version['\"]?:[ ]{0,}['\"]\d{1,3}\.\d{1,3}\.?\d{0,3}['\"]\s?"],
        },
        {
            "name": "prototype",
            "method": "reg",
            "operation": "&&",
            "rule": [r"var Prototype[ ]?=[ ]?{[\s]?[\s]?[ ]{0,}\s?['\"]?[vV]ersion['\"]?:[ ]{0,}['\"]\d{1,3}\.\d{1,3}\.?\d{0,3}\.?\d{0,3}['\"]\s?"],
        },
        {
            "name": "qunit",
            "method": "reg",
            "operation": "&&",
            "rule": [r"QUnit v?\d{1,}\.\d{1,}\.?\d{0,3}[ ]{0,}-[ ]{0,}A JavaScript Unit Testing Framework"],
        },
        {
            "name": "scriptaculous",
            "method": "reg",
            "operation": "&&",
            "rule": [r"var Scriptaculous[ ]{0,}=[ ]{0,}{\s?[ ]{0,}Version[ ]{0,}:[ ]{0,}[\"']\d{1,}\.\d{1,}\.?\d{0,}[\"']"],
        },
        {
            "name": "swfobject",
            "method": "reg",
            "operation": "&&",
            "rule": [r"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"],
        },
        {
            "name": "underscore",
            "method": "reg",
            "operation": "&&",
            "rule": [r"/\\\\\|'\|\\r\|\\n\|\\t\|\\u2028\|\\u2029\/g;"],
        },
        {
            "name": "webfont",
            "method": "reg",
            "operation": "&&",
            "rule": [r"['\"]//webfonts.fontslive.com/css/['\"][ ]{0,}\+[ ]{0,}((this\.e\.key)|(this\.[\w]\.key)|(key))[ ]{0,}\+[ ]{0,}['\"]\.css['\"]"]
        },
        {
            "name": "yui",
            "method": "md5",
            "operation": "||",
            "rule": [
                "41dc0754e0649fe27a3d0f6eada07483",
                "a0ce33b9732545dc67315c4b535680e2",
                "8d6d6c0480612b7d7ddca90cb818b6ca",
                "6b36a3248d235a0d849326e980836880",
                "f34686b7d4c2c2afa0a561c285353045",
                "a197a9fcba89049599ddb9794e3627fa",
                "a3522acc7a286b96c7d14dd1b5e177c0",
            ],
        },
        {
            "name": "clipboard",
            "method": "keyword",
            "operation": "&&",
            "rule": [r"https://clipboardjs.com/", "clipboard.js"]
        }
    ]

    file_links = {
        "angular": [
            r"https://lib.sinaapp.com/js/angular.js/angular-1.0.3/angular-bootstrap-prettify.js",
            r'https://lib.sinaapp.com/js/angular.js/angular-1.0.3/angular-bootstrap-prettify.min.js',
            r"https://lib.sinaapp.com/js/angular.js/angular-1.0.3/angular-bootstrap.js",
            r"https://lib.sinaapp.com/js/angular.js/angular-1.0.3/angular-cookies.js",
        ],
        "backbone": [
            r"https://lib.sinaapp.com/js/backbone/0.9.2/backbone.js",
            r"https://lib.sinaapp.com/js/backbone/0.9.2/backbone.min.js",
            r"https://lib.sinaapp.com/js/backbone/1.0.0/backbone-min.js",
        ],
        "bootstrap": [
            r"https://lib.sinaapp.com/js/bootstrap/2.0.2/js/bootstrap.js",
            r"https://lib.sinaapp.com/js/bootstrap/2.0.2/js/bootstrap.min.js",
            r"https://lib.sinaapp.com/js/bootstrap/4.0.0/js/bootstrap.js",
        ],
        "dojo": [
            r"https://lib.sinaapp.com/js/dojo/1.2.2/dojo.js",
        ],
        "ext_core": [
            "https://lib.sinaapp.com/js/ext-core/3.0.0/ext-core-debug.js",
            "https://lib.sinaapp.com/js/ext-core/3.1.0/ext-core.js"
        ],
        "highcharts": [
            r"https://lib.sinaapp.com/js/highcharts/2.1.9/highcharts.js",
            r"https://lib.sinaapp.com/js/highcharts/2.1.9/highcharts.src.js",
            r"https://lib.sinaapp.com/js/highcharts/2.1.9/themes/dark-blue.js",
            r"https://lib.sinaapp.com/js/highcharts/2.1.9/modules/exporting.js",
            r"https://lib.sinaapp.com/js/highcharts/2.1.9/adapters/mootools-adapter.src.js"
        ],
        "highstock": [
            r"https://lib.sinaapp.com/js/highstock/1.2.4/adapters/mootools-adapter.js",
            r"https://lib.sinaapp.com/js/highstock/1.2.4/adapters/mootools-adapter.src.js",
            r"https://lib.sinaapp.com/js/highstock/1.2.4/adapters/prototype-adapter.js",
            r"https://lib.sinaapp.com/js/highstock/1.2.4/adapters/prototype-adapter.src.js",
            r"https://lib.sinaapp.com/js/highstock/1.2.4/modules/canvas-tools.js",
            r"https://lib.sinaapp.com/js/highstock/1.2.4/modules/data.js",
            r"https://lib.sinaapp.com/js/highstock/1.2.4/modules/exporting.js"
        ],
        "jquery": [
            r"https://lib.sinaapp.com/js/jq.mobi/1.0/jq.mobi.min.js", # 无法匹配正则
            r"https://lib.sinaapp.com/js/jq.mobi/1.0/jq.ui.min.js",  # 无法匹配正则
            r"https://lib.sinaapp.com/js/jq.mobi/1.2/jq.ui.min.js", # 无法匹配
            r"https://lib.sinaapp.com/js/jquery/1.10/jquery-1.10.0.min.js",
            r"https://lib.sinaapp.com/js/jquery/3.1.0/jquery-3.1.0.slim.js",
        ],
        "jquery_mobile": [
            r"https://lib.sinaapp.com/js/jquery-mobile/1.2.0/jquery.mobile-1.2.0.js",
            r"https://lib.sinaapp.com/js/jquery-mobile/1.3.1/jquery.mobile-1.3.1.js",
        ],
        "jquery_ui": [
            r"https://lib.sinaapp.com/js/jquery-ui/1.12.1/jquery-ui.js",
            r"https://lib.sinaapp.com/js/jquery-ui/1.12.1/jquery-ui.min.js"
        ],
        "jquery_cookie": [
            r"https://lib.sinaapp.com/js/jquery.cookie/jquery.cookie.js"
        ],
        "jquery_migrate": [
            r"https://lib.sinaapp.com/js/jquery.migrate/1.2.1/jquery-migrate-1.2.1.js",
            r"https://lib.sinaapp.com/js/jquery.migrate/1.2.1/jquery-migrate-1.2.1.min.js"
        ],
        "jquery_tools": [
            r"https://lib.sinaapp.com/js/jquerytools/1.2.5/jquery.tools.min.js",
            r"https://lib.sinaapp.com/js/jquerytools/1.2.7/jquery.tools.min.js"
        ],
        "json2": [
            r"https://lib.sinaapp.com/js/json2/json2.js",
        ],
        "lesscss": [
            r"https://lib.sinaapp.com/js/lesscss/1.3.3/less-1.3.3.min.js",
        ],
        "mootools": [
            r"https://lib.sinaapp.com/js/mootools/1.1.1/mootools.js",
            r"https://lib.sinaapp.com/js/mootools/1.1.1/mootools.min.js",
            r"https://lib.sinaapp.com/js/mootools/1.2.5/mootools.js",
            r"https://lib.sinaapp.com/js/mootools/1.4.5/mootools.js",
        ],
        "prototype": [
            r"https://lib.sinaapp.com/js/prototype/1.5.0.0/prototype.js",
            r"https://lib.sinaapp.com/js/prototype/1.5.0.0/prototype.min.js",
            r"https://lib.sinaapp.com/js/prototype/1.5.1.0/prototype.js",
            r"https://lib.sinaapp.com/js/prototype/1.5.1.0/prototype.min.js"
            r"https://lib.sinaapp.com/js/prototype/1.7.0.0/prototype.js",
            r"https://lib.sinaapp.com/js/prototype/1.7.0.0/prototype.min.js",
        ],
        "qunit": [
            r"https://lib.sinaapp.com/js/qunit/1.4/qunit.js",
            r"https://lib.sinaapp.com/js/qunit/1.11/qunit.js",
        ],
        "scriptaculous": [
            r"https://lib.sinaapp.com/js/scriptaculous/1.8.1/scriptaculous.js",
            r"https://lib.sinaapp.com/js/scriptaculous/1.8.1/scriptaculous.min.js",
            r"https://lib.sinaapp.com/js/scriptaculous/1.9.0/scriptaculous.js",
        ],
        "swfobject": [
            r"https://lib.sinaapp.com/js/swfobject/2.1/swfobject.js",
            r"https://lib.sinaapp.com/js/swfobject/2.1/swfobject_src.js",
            r"https://lib.sinaapp.com/js/swfobject/2.2/swfobject.js",
            r"https://lib.sinaapp.com/js/swfobject/2.2/swfobject_src.js",
        ],
        "underscore": [
            r"https://lib.sinaapp.com/js/underscore/1.3.3/underscore.js",
            r"https://lib.sinaapp.com/js/underscore/1.3.3/underscore.min.js",
            r"https://lib.sinaapp.com/js/underscore/1.4.4/underscore-min.js",
            r"https://lib.sinaapp.com/js/underscore/1.4.4/underscore.js"
        ],
        "webfont": [
            r"https://lib.sinaapp.com/js/webfont/1.0.4/webfont.js",
            r"https://lib.sinaapp.com/js/webfont/1.0.4/webfont_debug.js",
            r"https://lib.sinaapp.com/js/webfont/1.0.10/webfont.js",
            r"https://lib.sinaapp.com/js/webfont/1.0.10/webfont_debug.js",
            r"https://lib.sinaapp.com/js/webfont/1.0.16/webfont.js",
            r"https://lib.sinaapp.com/js/webfont/1.0.16/webfont_debug.js"
        ],
        "yui": [
            r"https://lib.sinaapp.com/js/yui/3.9/yui-coverage.js",
            r"https://lib.sinaapp.com/js/yui/3.9/yui-debug.js",
            r"https://lib.sinaapp.com/js/yui/3.9/yui.js",
            r"https://lib.sinaapp.com/js/yui/3.9/yui-min.js",
            r"https://lib.sinaapp.com/js/yui/2.8.2/yui-min.js",
            r"https://lib.sinaapp.com/js/yui/2.8.2/yui.js",
            r"https://lib.sinaapp.com/js/yui/2.7.0/yui-min.js",
        ],
        "clipboard": [
            r"https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/clipboard.js/2.0.10/clipboard.min.js",
            r"https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/clipboard.js/2.0.10/clipboard.js",

        ]
    }