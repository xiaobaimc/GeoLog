# geoip_processor.py

import re
from collections import Counter
import geoip2.database
import logging
from config import LOG_FILE, GEOIP_DB_PATH

# 正则表达式模式，用于匹配 X-Forwarded-For 和 X-Real-IP
XFF_PATTERN = re.compile(r'X-Forwarded-For:\s*([^\s,]+)')
XREALIP_PATTERN = re.compile(r'X-Real-IP:\s*([^\s,]+)')

# 用于缓存已经查询过的 IP 地址的地理信息
geo_cache = {}

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 解析每一行日志
def process_log_line(line):
    # 跳过空行或无效行
    if not line.strip():
        return None

    # 查找 X-Forwarded-For 头部中的 IP 地址
    match_xff = XFF_PATTERN.search(line)
    if match_xff:
        return match_xff.group(1).strip('"')  # 移除多余的引号

    # 查找 X-Real-IP 头部中的 IP 地址
    match_xrealip = XREALIP_PATTERN.search(line)
    if match_xrealip:
        return match_xrealip.group(1).strip('"')  # 移除多余的引号

    # 如果都没有，返回日志中的原始 IP 地址（假设是第一列）
    parts = line.split()
    if parts:
        return parts[0].strip('"')  # 移除多余的引号
    
    # 如果格式不正确，返回 None
    return None

# 使用 GeoIP2 查询 IP 的地理位置信息，并加上缓存
def get_geolocation(ip):
    if ip in geo_cache:
        return geo_cache[ip]

    try:
        with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
            response = reader.city(ip)
            country = response.country.name if response.country.name else 'Unknown'
            city = response.city.name if response.city.name else 'Unknown'
            geo_cache[ip] = (country, city)  # 缓存查询结果
            return country, city
    except geoip2.errors.AddressNotFoundError:
        geo_cache[ip] = ('Unknown', 'Unknown')
        return 'Unknown', 'Unknown'
    except Exception as e:
        logging.error(f"Error processing IP {ip}: {e}")
        geo_cache[ip] = ('Error', 'Error')
        return 'Error', 'Error'

# 读取日志文件并处理
def process_log_file(log_file):
    ip_list = []

    # 逐行读取文件并提取 IP 地址
    with open(log_file, 'r') as f:
        for line in f:
            ip = process_log_line(line)
            if ip:  # 只处理有效的 IP 地址
                ip_list.append(ip)

    # 使用 Counter 统计每个 IP 的出现次数
    ip_counts = Counter(ip_list)

    # 按照出现次数从大到小排序
    ip_counts_sorted = ip_counts.most_common()

    # 查询每个 IP 的地理信息
    geolocation_results = []
    for ip, count in ip_counts_sorted:
        country, city = get_geolocation(ip)
        geolocation_results.append((ip, count, country, city))

    return geolocation_results
