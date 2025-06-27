import os
import re
import sys

def analyze_analytical_output(output_file_path, config, wafer_num, error_rate):
    """
    分析analytical输出文件，提取cycle_count并找到符合条件的文件
    
    Args:
        output_file_path: 输出文件的基础路径
        config: 配置名称
        wafer_num: wafer数量
        error_rate: 错误率（浮点数）
    """
    cycle_counts = {}  # 存储每个文件的max_cycle_count
    
    # 遍历所有输出文件
    for idx in range(1, wafer_num + 1):
        filename = f"{output_file_path}_{config}_{idx}_analytical_output.txt"
        
        if not os.path.exists(filename):
            print(f"Warning: File {filename} not found, skipping...")
            continue
            
        max_cycle_count = 0
        
        # 读取文件内容
        with open(filename, 'r') as f:
            for line in f:
                # 使用正则表达式匹配 "sys[{int}] finished, {int} cycles" 格式
                match = re.search(r'sys\[(\d+)\] finished, (\d+) cycles', line)
                if match:
                    cycle_count = int(match.group(2))
                    max_cycle_count = max(max_cycle_count, cycle_count)
        
        if max_cycle_count > 0:
            cycle_counts[idx] = max_cycle_count
            print(f"File {idx}: max_cycle_count = {max_cycle_count}")
        else:
            print(f"Warning: No valid cycle count found in file {filename}")
    
    if not cycle_counts:
        print("Error: No valid cycle counts found in any files")
        return
    
    # 找到optimal_cycle_count（所有max_cycle_count的最小值）
    optimal_cycle_count = min(cycle_counts.values())
    print(f"Optimal cycle count: {optimal_cycle_count}")
    
    # 计算sup_cycle_count
    sup_cycle_count = (1 + error_rate) * optimal_cycle_count
    print(f"Sup cycle count: {sup_cycle_count}")
    
    # 找到所有max_cycle_count小于sup_cycle_count的文件
    possible_optimal_indices = []
    for idx, max_cycle_count in cycle_counts.items():
        if max_cycle_count < sup_cycle_count:
            possible_optimal_indices.append(idx)
    
    # 将结果写入possible_optimal.txt文件
    with open("possible_optimal.txt", 'w') as f:
        for idx in sorted(possible_optimal_indices):
            f.write(f"{idx}\n")
    
    print(f"Found {len(possible_optimal_indices)} files with max_cycle_count < sup_cycle_count")
    print("Results written to possible_optimal.txt")
    print("Indices:", sorted(possible_optimal_indices))

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python analyze_analytical_output.py <output_file_path> <config> <wafer_num> <error_rate>")
        sys.exit(1)
    
    output_file_path = sys.argv[1]
    config = sys.argv[2]
    wafer_num = int(sys.argv[3])
    error_rate = float(sys.argv[4])
    
    analyze_analytical_output(output_file_path, config, wafer_num, error_rate) 
