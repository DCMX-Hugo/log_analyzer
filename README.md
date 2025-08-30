# 日志分析器

这是一个用于分析Web服务访问日志的Python脚本，能够统计总请求数、平均响应时间、HTTP状态码分布和最繁忙时段。

## 功能特性

- 统计日志文件中的总请求次数
- 计算所有请求的平均响应时长（毫秒）
- 统计每种HTTP状态码出现的次数
- 确定一天中请求最繁忙的小时（0-23）

## 如何运行

### 环境要求
- Python 3.6+

### 运行指令
```bash
# 直接运行
python log_analyzer.py /path/to/access.log

# 或添加执行权限后运行
chmod +x log_analyzer.py
./log_analyzer.py /path/to/access.log
