#!/usr/bin/env python3
"""
日志分析器 - 分析Web服务访问日志并生成统计报告

功能：
- 统计总请求次数
- 计算平均响应时间
- 统计HTTP状态码分布
- 确定最繁忙的小时段
"""

import json
import sys
from collections import defaultdict
from datetime import datetime

def analyze_log_file(file_path):
    """
    分析日志文件并返回统计结果

    Args:
        file_path (str): 日志文件路径

    Returns:
        dict: 包含统计结果的字典
    """
    total_requests = 0
    total_response_time = 0
    status_code_counts = defaultdict(int)
    hour_counts = defaultdict(int)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    log_entry = json.loads(line)
                    # 验证必要字段存在
                    if 'timestamp' not in log_entry or 'response_time_ms' not in log_entry:
                        print(f"警告: 第 {line_num} 行缺少必要字段", file=sys.stderr)
                        continue
                    total_requests += 1
                    total_response_time += log_entry['response_time_ms']
                    # 统计状态码
                    if 'http_status' in log_entry:
                        status_code = log_entry['http_status']
                        status_code_counts[status_code] += 1
                    # 解析时间戳并统计小时
                    timestamp = log_entry['timestamp']
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hour_counts[dt.hour] += 1
                except json.JSONDecodeError:
                    print(f"警告: 第 {line_num} 行JSON格式错误", file=sys.stderr)
                except ValueError as e:
                    print(f"警告: 第 {line_num} 行时间格式错误: {e}", file=sys.stderr)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 '{file_path}' 不存在")
    except Exception as e:
        raise RuntimeError(f"读取文件时发生错误: {e}")
    # 计算统计结果
    avg_response_time = round(total_response_time / total_requests, 2) if total_requests > 0 else 0
    # 找出最繁忙的小时
    busiest_hour = max(hour_counts.items(), key=lambda x: x[1], default=(0, 0))[0]
    return {
        "total_requests": total_requests,
        "average_response_time_ms": avg_response_time,
        "status_code_counts": dict(status_code_counts),
        "busiest_hour": busiest_hour
    }

def main():
    """主函数 - 处理命令行参数并输出结果"""
    if len(sys.argv) != 2:
        print("用法: python log_analyzer.py <日志文件路径>")
        sys.exit(1)
    log_file_path = sys.argv[1]
    try:
        result = analyze_log_file(log_file_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()