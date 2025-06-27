import os

def generate_config_txt(wafer_num: int, config: str, physical_filepath: str, output_filepath: str):
    """
    生成批量config.txt文件
    
    Args:
        wafer_num: wafer数量
        config: 配置名称
        physical_filepath: physical_network.txt文件的基础路径
        output_filepath: 输出文件路径
    """
    # 确保输出目录存在
    if not os.path.exists(output_filepath):
        os.makedirs(output_filepath)
    
    # 直接嵌入config.txt的完整内容
    config_content = [
        "ENABLE_QCN 1",
        "USE_DYNAMIC_PFC_THRESHOLD 1",
        "",
        "PACKET_PAYLOAD_SIZE 1000",
        "",
        "TOPOLOGY_FILE ../../scratch/topology/8_nodes_1_switch_topology.txt",  # 第六行，将被替换
        "FLOW_FILE ../../scratch/output/flow.txt",
        "TRACE_FILE ../../scratch/output/trace.txt",
        "TRACE_OUTPUT_FILE ../../scratch/output/mix.tr",
        "FCT_OUTPUT_FILE ../../scratch/output/fct.txt",
        "PFC_OUTPUT_FILE ../../scratch/output/pfc.txt",
        "QLEN_MON_FILE ../../scratch/output/qlen.txt",
        "QLEN_MON_START 0",
        "QLEN_MON_END 20000",
        "",
        "",
        "SIMULATOR_STOP_TIME 40000000000000.00",
        "",
        "CC_MODE 12",
        "ALPHA_RESUME_INTERVAL 1",
        "RATE_DECREASE_INTERVAL 4",
        "CLAMP_TARGET_RATE 0",
        "RP_TIMER 900",
        "EWMA_GAIN 0.00390625",
        "FAST_RECOVERY_TIMES 1",
        "RATE_AI 50Mb/s",
        "RATE_HAI 100Mb/s",
        "MIN_RATE 100Mb/s",
        "DCTCP_RATE_AI 1000Mb/s",
        "",
        "ERROR_RATE_PER_LINK 0.0000",
        "L2_CHUNK_SIZE 4000",
        "L2_ACK_INTERVAL 1",
        "L2_BACK_TO_ZERO 0",
        "",
        "HAS_WIN 1",
        "GLOBAL_T 0",
        "VAR_WIN 1",
        "FAST_REACT 1",
        "U_TARGET 0.95",
        "MI_THRESH 0",
        "INT_MULTI 1",
        "MULTI_RATE 0",
        "SAMPLE_FEEDBACK 0",
        "PINT_LOG_BASE 1.05",
        "PINT_PROB 1.0",
        "NIC_TOTAL_PAUSE_TIME 0",
        "",
        "RATE_BOUND 1",
        "",
        "ACK_HIGH_PRIO 0",
        "",
        "LINK_DOWN 0 0 0",
        "",
        "ENABLE_TRACE 1",
        "",
        "KMAX_MAP 6 25000000000 400 40000000000 800 100000000000 1600 200000000000 2400 400000000000 3200 2400000000000 3200",
        "KMIN_MAP 6 25000000000 100 40000000000 200 100000000000 400 200000000000 600 400000000000 800 2400000000000 800",
        "PMAX_MAP 6 25000000000 0.2 40000000000 0.2 100000000000 0.2 200000000000 0.2 400000000000 0.2 2400000000000 0.2",
        "",
        "BUFFER_SIZE 32"
    ]
    
    # 为每个wafer生成config.txt文件
    for idx in range(1, wafer_num + 1):
        idx_padded = f"{idx:06d}"
        physical_filename = f"{physical_filepath}_{config}_{idx_padded}_physical_network.txt"
        output_filename = f"{config}_{idx_padded}_config.txt"
        output_file = os.path.join(output_filepath, output_filename)
        
        # 创建新的内容，只修改第六行
        new_content = []
        for i, line in enumerate(config_content):
            if i == 5:  # 第六行（索引为5）
                new_content.append(f"TOPOLOGY_FILE {physical_filename}\n")
            else:
                new_content.append(line + "\n" if not line.endswith("\n") else line)
        
        # 写入输出文件
        with open(output_file, 'w') as f:
            f.writelines(new_content)
        
        print(f"Generated: {output_filename}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 5:
        print("Usage: python generate_config_txt.py <wafer_num> <config> <physical_filepath> <output_filepath>")
        sys.exit(1)
    
    wafer_num = int(sys.argv[1])
    config = sys.argv[2]
    physical_filepath = sys.argv[3]
    output_filepath = sys.argv[4]
    
    generate_config_txt(wafer_num, config, physical_filepath, output_filepath) 
