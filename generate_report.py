# generate_report.py

from geoip_processor import process_log_file
from config import LOG_FILE, OUTPUT_HTML_DIR, OUTPUT_HTML_FILE
from jinja2 import Template
import os

# 生成 HTML 报告
def generate_html_report(geolocation_results):
    # 确保输出目录存在
    if not os.path.exists(OUTPUT_HTML_DIR):
        os.makedirs(OUTPUT_HTML_DIR)

    # 读取 HTML 模板
    with open('templates/report_template.html', 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # 渲染 HTML
    template = Template(template_content)
    rendered_html = template.render(geolocation_results=geolocation_results)

    # 输出生成的 HTML 到文件
    output_html_path = os.path.join(OUTPUT_HTML_DIR, OUTPUT_HTML_FILE)
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    
    print(f"HTML 报告已生成：{output_html_path}")

if __name__ == "__main__":
    # 处理日志文件并生成地理位置结果
    geolocation_results = process_log_file(LOG_FILE)

    # 生成并保存 HTML 报告
    generate_html_report(geolocation_results)