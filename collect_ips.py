import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表（精简有效源）
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
    # 可加更多，如 'https://raw.githubusercontent.com/Mr-AoDr/sc/main/ips.txt'（纯文本 IP）
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
    for url in urls:
        try:
            # 发送HTTP请求获取网页内容
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'

            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 通用解析：优先抓 td（表格），fallback 整个文本
            elements = soup.find_all('td')
            if not elements:
                ip_matches = re.findall(ip_pattern, response.text)
                for ip in ip_matches:
                    file.write(ip + '\n')
                continue

            # 遍历所有元素,查找IP地址
            for element in elements:
                element_text = element.get_text()
                ip_matches = re.findall(ip_pattern, element_text)
                for ip in ip_matches:
                    file.write(ip + '\n')

        except Exception as e:
            print(f"处理 {url} 时出错：{e}")  # 加这行，便于 Actions 日志 debug

print('IP地址已保存到 ip.txt 文件中。')
print(f'总共找到 {len(open("ip.txt").readlines())} 个 IP')  # 加计数，便于检查
