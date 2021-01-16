import logging
import re
from urllib import request

# 匹配合法 IP 地址
regex_ip = re.compile(
    r"\D*("
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)"
    + r")\D*")


# 增强鲁棒性，用多种方式获取 IP
def get_ip():
    return (get_ip_by_ipip()
            or get_ip_by_httpbin())


# 这几个函数会在 DNS 遭受污染时失效
def get_ip_by_ipip():
    url = 'http://myip.ipip.net/'
    try:
        resp = request.urlopen(url=url, timeout=10).read()
        return regex_ip.match(resp.decode("utf-8")).group(1)
    except Exception as e:
        logging.warning("get_ip_by_ipip FAILED, error: %s", str(e))
        return None


def get_ip_by_httpbin():
    url = 'http://www.httpbin.org/ip'
    try:
        resp = request.urlopen(url=url, timeout=10).read()
        return regex_ip.match(resp.decode("utf-8")).group(1)
    except Exception as e:
        logging.warning("get_ip_by_httpbin FAILED, error: %s", str(e))
        return None


# 测试
if __name__ == '__main__':
    print(get_ip())
    print(get_ip_by_ipip())
    print(get_ip_by_httpbin())
