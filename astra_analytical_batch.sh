#!/usr/bin/env bash

# 可修改变量
wafer_num=10  # 你可以修改为需要的循环次数
workload_filepath="/path/to/workload"
system_filepath="/path/to/system"
network_filepath="/path/to/network"
remote_path="/path/to/remote_memory_config.yml"
config="default_config"  # 你可以修改为需要的配置名
output_file_path="/path/to/output"  # 输出文件路径
error_rate=0.1  # 错误率，浮点数

echo "Starting AstraSim Analytical batch processing..."
echo "Config: $config"
echo "Wafer number: $wafer_num"
echo "Error rate: $error_rate"

for ((idx=1; idx<=wafer_num; idx++)); do
    idx_padded=$(printf "%06d" "$idx")
    workload_filename="${workload_filepath}_${config}_${idx_padded}_workload.txt"
    system_filename="${system_filepath}_${config}_${idx_padded}_system.json"
    network_filename="${network_filepath}_${config}_${idx_padded}_network.yml"
    output_filename="${output_file_path}_${config}_${idx}_analytical_output.txt"

    echo "Processing wafer $idx/$wafer_num..."
    
    ./build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_unaware \
        --workload-configuration="$workload_filename" \
        --system-configuration="$system_filename" \
        --network-configuration="$network_filename" \
        --remote-memory-configuration="$remote_path" \
        > "$output_filename" 2>&1
    
    echo "Completed wafer $idx, output saved to $output_filename"
done

echo "All AstraSim runs completed. Starting analysis..."

# 调用Python脚本进行结果分析
python3 ../errpy/analyze_analytical_output.py "$output_file_path" "$config" "$wafer_num" "$error_rate"

echo "Analysis completed. Check possible_optimal.txt for results."
