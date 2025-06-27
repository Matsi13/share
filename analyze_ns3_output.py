import os
import re
import sys

def analyze_ns3_output(output_file_path, config, idx_list):
    """
    分析ns3输出文件，提取cycle_count并找到最优的配置
    
    Args:
        output_file_path: 输出文件的基础路径
        config: 配置名称
        idx_list: 需要分析的索引列表
    """
    cycle_counts = {}  # 存储每个文件的max_cycle_count
    
    # 遍历所有输出文件
    for idx in idx_list:
        filename = f"{output_file_path}_{config}_{idx}_ns3_output.txt"
        
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
    
    # 找到对应的idx
    optimal_idx = None
    for idx, max_cycle_count in cycle_counts.items():
        if max_cycle_count == optimal_cycle_count:
            optimal_idx = idx
            break
    
    print(f"\n=== NS3 Analysis Results ===")
    print(f"Optimal configuration:")
    print(f"  Index: {optimal_idx}")
    print(f"  Max cycle count: {optimal_cycle_count}")
    
    return optimal_idx, optimal_cycle_count

def read_possible_optimal_indices(idx_filepath):
    """
    从possible_optimal.txt文件中读取索引列表
    
    Args:
        idx_filepath: possible_optimal.txt文件路径
    
    Returns:
        list: 索引列表
    """
    indices = []
    try:
        with open(idx_filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # 跳过空行
                    indices.append(int(line))
    except FileNotFoundError:
        print(f"Error: File {idx_filepath} not found")
        return []
    
    return indices

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python analyze_ns3_output.py <output_file_path> <config> <idx_filepath>")
        sys.exit(1)
    
    output_file_path = sys.argv[1]
    config = sys.argv[2]
    idx_filepath = sys.argv[3]
    
    # 读取索引列表
    idx_list = read_possible_optimal_indices(idx_filepath)
    if not idx_list:
        print("No indices found in possible_optimal.txt")
        sys.exit(1)
    
    print(f"Analyzing {len(idx_list)} files from possible_optimal.txt")
    analyze_ns3_output(output_file_path, config, idx_list) 
