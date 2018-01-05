import requests
from lxml import etree

import time
import os
import csv

import conf


headers = {
    'Cookie': 'select_city=440300; all-lj=6341ae6e32895385b04aae0cf3d794b0; lianjia_uuid=ad7a11ce-7f53-41b0-8424-54a7397b5531; lianjia_ssid=6e93e3a3-f8d7-4c69-838d-0f543e339b4f',
    'Host': 'sz.lianjia.com',
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

}


def getContent(url):
    """
    功能：获取页面信息；
        参数：url=网页地址
        返回值：页面的HTML代码
    """
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.content


def parseHtml(htmlContent):
    root = etree.HTML(htmlContent)
    house_info = []
    house_list = root.xpath('//*[(@class= "sellListContent")]/li')
    for house in house_list:
        house_title = ''.join(house.xpath(
            'div[(@class="info clear")]/div[(@class="title")]/a/text()'))
        house_url = ''.join(house.xpath(
            'div[(@class="info clear")]/div[(@class="title")]/a/@href'))
        # 提取多个标签下的文字
        house_address = house.xpath(
            'div[(@class="info clear")]/div[(@class="address")]/div[(@class="houseInfo")]')[0].xpath('string()')
        house_address_url = ''.join(house.xpath(
            'div[(@class="info clear")]/div[(@class="address")]/div[(@class="houseInfo")]/a/@href'))
        house_flood = house.xpath(
            'div[(@class="info clear")]/div[(@class="flood")]')[0].xpath('string()')
        house_followInfo = house.xpath(
            'div[(@class="info clear")]/div[(@class="followInfo")]')[0].xpath('string()')
        # house_tag_subway = house.xpath('div[(@class="info clear")]/div[(@class="tag")]/span[(@class="subway")]/text()')
        # house_tag_taxfree = house.xpath('div[(@class="info clear")]/div[(@class="tag")]/span[(@class="taxfree")]/text()')
        # house_tag_haskey = house.xpath('div[(@class="info clear")]/div[(@class="tag")]/span[(@class="haskey")]/text()')
        house_tag = house.xpath(
            'div[(@class="info clear")]/div[(@class="tag")]/span/text()')

        house_priceInfo_total = house.xpath(
            'div[(@class="info clear")]/div[(@class="priceInfo")]//div[(@class="totalPrice")]')[0].xpath('string()')
        house_priceInfo_uintPrice = house.xpath(
            'div[(@class="info clear")]/div[(@class="priceInfo")]//div[(@class="unitPrice")]')[0].xpath('string()')
        house_info.append([house_title, house_address, house_flood, house_followInfo,
                           house_priceInfo_total, house_priceInfo_uintPrice, ' | '.join(house_tag), house_url])
    return house_info


def saveHouseInfoToTxt(houseInfo, txtFile):
    # TODO:判断txtFile中是否存在该信息，如果没有，则添加
    if not os.path.exists(txtFile):
        with open(txtFile, mode='w', encoding='utf-8') as f:
            f.write()
    for info in houseInfo:
        with open(txtFile, mode='a', encoding='utf-8') as f:
            f.write(' * '.join(info) + os.linesep)


def saveHouseInfoToCSV(houseInfo, csvFile):
    # TODO:判断csvFile中是否存在该信息，如果没有，则添加
    if not os.path.exists(csvFile):
        with open(csvFile, mode='w', encoding='utf-8', newline='') as f:
            csvWriter = csv.writer(f, dialect='excel')
            csvWriter.writerow(
                ['标题', '地址', '户型', '关注', '总价', '均价', '房源标签', '房源链接'])
    for info in houseInfo:
        with open(csvFile, mode='a', encoding='utf-8', newline='') as f:
            csvWriter = csv.writer(f, dialect='excel')
            csvWriter.writerow(info)


def saveHouseInfoToDB(houseInfo, dataBase):
    pass


def getAllHouseInfo(urlList):
    for url in urlList:
        htmlContent = getContent(url)
        houseInfo = parseHtml(htmlContent)
        saveHouseInfoToTxt(houseInfo, conf.TXT_FILE)
        saveHouseInfoToCSV(houseInfo, conf.CSV_FILE)
        print('获取第{num}页'.format(num=url.split('pg')[-1].split('.')[0]))
        time.sleep(0.5)
    print('信息获取完成')


def main():
    urlList = [conf.LJ_URL + 'pg{num}'.format(num=i) for i in range(1, 101)]
    getAllHouseInfo(urlList)


if __name__ == '__main__':
    main()
