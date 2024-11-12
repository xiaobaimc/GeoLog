# IP Geolocation Logger

本项目用于解析访问日志中的 IP 地址，通过 GeoIP2 查询地理位置，并生成 HTML 报告

>**本项目超过一半都由GPT编写**

## 项目结构

```
ip_geolocation/
├── config.py              # 配置文件
├── geoip_processor.py     # 处理日志和 GeoIP 查询的模块
├── generate_report.py     # 生成报告并输出 HTML 文件
├── templates/
│   └── report_template.html  # HTML 模板
└── output/
    └── ip_geolocation_output.html  # 输出文件保存目录
```

## 安装与依赖

1. 确保你有Python 3.x

2. 安装依赖包：
    ```
    pip install geoip2 jinja2
    ```

3. 请从 [MaxMind](https://www.maxmind.com/) 注册并下载 `GeoLite2-City.mmdb` 并存放在项目根目录
具体请参考网上相关教程

## 配置

请在 `config.py` 填写你的日志路径或将日志 `access.log` 存放在项目根目录

以及将 `GeoLite2-City.mmdb` 存放在根目录

你可以对 `config.py` 进行修改以满足当前环境

## 使用
默认情况下提供了示例的 `access.log` 以及生成后的 `report_template.html`

你可以将 `access.log` 替换为你实际的日志文件

使用下列命令进行生成
```
python generate_report.py
```
生成后的文件将存放在 `output/report_template.html` 使用浏览器直接打开

每次生成会覆盖原有文件

## 输出样式

如果正确的话，打开html文件应该会看到如下面所示

| IP 地址       | 频率  | 国家      | 城市     |
|--------------|-------|---------|-----------|
| 127.0.0.1    | 1     | Unknown | Unknown   |
| 203.0.113.0  | 1     | USA     | New York  |



