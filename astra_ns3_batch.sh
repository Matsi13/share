#!/usr/bin/env bash

# 可修改变量
workload_filepath="/path/to/workload"
system_filepath="/path/to/system"
network_filepath="/path/to/network"
remote_path="/path/to/remote_memory_config.yml"
logical_filepath="/path/to/logical"
config="default_config"  # 你可以修改为需要的配置名
idx_filepath="possible_optimal.txt"  # possible_optimal.txt文件路径
output_file_path="/path/to/output"  # 输出文件路径

echo "Starting AstraSim NS3 batch processing..."
echo "Config: $config"
echo "Reading indices from: $idx_filepath"

# 检查possible_optimal.txt文件是否存在
if [ ! -f "$idx_filepath" ]; then
    echo "Error: File $idx_filepath not found!"
    echo "Please run astra_analytical_batch.sh first to generate possible_optimal.txt"
    exit 1
fi

# 读取索引列表
indices=()
while IFS= read -r line; do
    # 跳过空行
    if [ -n "$line" ]; then
        indices+=("$line")
    fi
done < "$idx_filepath"

if [ ${#indices[@]} -eq 0 ]; then
    echo "Error: No indices found in $idx_filepath"
    exit 1
fi

echo "Found ${#indices[@]} indices to process: ${indices[*]}"

# 处理每个索引
for idx in "${indices[@]}"; do
    workload_filename="${workload_filepath}_${config}_${idx}_workload.txt"
    system_filename="${system_filepath}_${config}_${idx}_system.json"
    network_filename="${network_filepath}_${config}_${idx}_config.txt"
    logical_filename="${logical_filepath}_${config}_${idx}_logical_network.json"
    output_filename="${output_file_path}_${config}_${idx}_ns3_output.txt"

    echo "Processing index $idx..."

    # 检查输入文件是否存在
    if [ ! -f "$workload_filename" ]; then
        echo "Warning: Workload file $workload_filename not found, skipping..."
        continue
    fi
    if [ ! -f "$system_filename" ]; then
        echo "Warning: System file $system_filename not found, skipping..."
        continue
    fi
    if [ ! -f "$network_filename" ]; then
        echo "Warning: Network file $network_filename not found, skipping..."
        continue
    fi
    if [ ! -f "$logical_filename" ]; then
        echo "Warning: Logical file $logical_filename not found, skipping..."
        continue
    fi

    ./extern/network_backend/ns-3/build/scratch/ns3.42-AstraSimNetwork-default \
        --workload-configuration="$workload_filename" \
        --system-configurations="$system_filename" \
        --network-configuration="$network_filename" \
        --remote-memory-configuration="$remote_path" \
        --logical-topology-configuration="$logical_filename" \
        --comm-group-configuration="empty" \
        > "$output_filename" 2>&1

    echo "Completed index $idx, output saved to $output_filename"
done

echo "All NS3 runs completed. Starting analysis..."

# 调用Python脚本进行结果分析
python3 ../errpy/analyze_ns3_output.py "$output_file_path" "$config" "$idx_filepath"

echo "NS3 analysis completed." 
