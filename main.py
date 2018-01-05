import requests
from lxml import etree

import time


headers = {
    'Cookie': 'select_city=440300; all-lj=6341ae6e32895385b04aae0cf3d794b0; lianjia_uuid=ad7a11ce-7f53-41b0-8424-54a7397b5531; lianjia_ssid=6e93e3a3-f8d7-4c69-838d-0f543e339b4f',
    'Host': 'sz.lianjia.com',
    'Connection': 'close',
    'User-Agent': 'Paw/3.1.5 (Macintosh; OS X/10.12.6) GCDHTTPRequest'

}


def get_content(url):
    """
    功能：获取页面信息；
        参数：url=网页地址
        返回值：页面的HTML代码
    """
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.content
