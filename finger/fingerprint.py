import re
import hashlib
from finger.fingers import JSFileFinger

DEBUG = True


def __calculate_md5(string):
    """ 计算字符串的md5值
    """
    if type(string) is not str:
        raise TypeError(f"计算md5失败，给出的不是字符串: {type(string)}")

    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()


def __fingers_verify(fingers: list) -> bool:
    """  验证 配置文件中的 fingers的配置列表，为下面的函数提供验证

    :param fingers: 指纹列表
    :return bool: 验证通过返回 True, 失败直接抛出异常
    """

    # 判断配置
    for finger in fingers:
        # 名称
        name = finger.get("name")
        if not name:
            raise ValueError(f"name 丢失或 键 name 错误 : {finger}")

        # 处理的判断规则的逻辑
        operation = finger.get("operation")
        if operation != '&&' and operation != '||' or not operation:
            raise ValueError(f"请检查 {name}, 错误的判断逻辑 (operation): {operation}")

        # 模式
        method = finger.get("method")
        if method != "reg" and method != "md5" and method != "keyword":
            raise ValueError(f"请检查 {name}, 错误的模式 (method): {method}")

        # 匹配规则
        rule = finger.get("rule")
        if not rule:
            raise ValueError(f"请填写 {name} 的规则 (rule): {rule}")
        elif type(rule) != list:
            raise ValueError(f"请检查 {name} 的规则 (rule) 格式: {rule}")

    return True


def __identify_fingers(content: str = '', file: str = '', fingers=None) -> dict:
    """ 识别指纹

    :param content: js 文件内容
    :param file: js 文件文件
    :param fingers: 指纹列表
    :return: 返回 字典格式 {'isfinder': <bool>是否匹配到规则, 'name': <str>规则名称, 'result': <str>匹配到的结果}
    """

    if not content and not file:
        raise ValueError("缺少必要参数 content 或 file")

    if content and file:
        raise ValueError("多余的参数 content 或 file")

    if fingers is None:
        raise ValueError("缺少必要参数 fingers")

    if type(fingers) is not list:
        raise ValueError("指纹列表格式错误")

    # 验证指纹配置文件是否正确
    __fingers_verify(fingers)

    content_string = content

    # 读取文件
    if not content:
        # 判断文件是否存在:
        try:
            with open(file, 'r', encoding='utf-8') as fp:
                content_string = fp.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"指定的文件 {file} 不存在.")

    # 结果
    result = None

    # 识别指纹
    for finger in fingers:
        name = finger["name"]
        # operation = None
        # 规则处理逻辑:
        operation = finger["operation"]
        # method = None
        # 规则处理模式
        method = finger['method']

        # 所有逻辑都得满足
        if operation == "&&":
            if method == "reg":
                # 遍历规则
                for rule in finger["rule"]:
                    # 判断逻辑
                    result = ''.join(re.findall(rule, content_string)) if re.findall(rule, content_string) else ''  # 正则匹配的返回列表转为字符串
                    if not result:
                        break
            elif method == "keyword":
                # 遍历规则
                for rule in finger["rule"]:
                    # 判断逻辑
                    result = str(finger["rule"]) if rule in content_string else '' # 匹配的规则关键字列表转为字符串
                    if not result:
                        break
            elif method == "md5":
                # 遍历规则
                for rule in finger["rule"]:
                    # 判断逻辑
                    result = __calculate_md5(content_string)  # md5 字符串
                    if rule != result:
                        break
            else:
                raise ValueError("错误的 method")
            if result:
                return {"isfinder": True, "name": name, "result": result}
        elif operation == "||":
             # 判断逻辑
             if method == "reg":
                 # 遍历规则
                 for rule in finger["rule"]:
                     re_result = ''.join(re.findall(rule, content_string)) if re.findall(rule, content_string) else '' # 正则匹配的返回列表转为字符串
                     # 匹配到一个
                     if re_result:
                         return {"isfinder": True, "name": name, "result": result}
             elif method == "keyword":
                 # 遍历规则
                 for rule in finger["rule"]:
                     result = str(finger["rule"]) if rule in content_string else '' # 匹配的规则关键字列表转为字符串
                     if result:
                         return {"isfinder": True, "name": name, "result": result}
             elif method == "md5":
                 # 遍历规则
                 for rule in finger["rule"]:
                     result = __calculate_md5(content_string) # md5 字符串
                     if result == rule:
                         return {"isfinder": True, "name": name, "result": result}
             else:
                raise ValueError("错误的 method")
        else:
            raise ValueError(f"错误的判断逻辑: {operation}")

    if not result:
        return {"isfinder": False, "name": '', "result": result}


def identify_js_fingers(content: str = '', file: str = '', fingers=None) -> dict:
    if fingers is None:
        fingers = JSFileFinger.js_fingers

    return __identify_fingers(content=content, file=file, fingers=fingers)


if __name__ == '__main__':
    # 指纹
    print("测试数据: ")
    print(identify_js_fingers(file='test.js'))