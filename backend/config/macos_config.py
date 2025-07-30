"""
macOS 特定配置优化
针对 macOS CPU 环境的性能优化设置
"""

import os
import platform
import torch

def get_macos_config():
    """获取 macOS 优化配置"""
    config = {
        "device": "cpu",
        "num_threads": os.cpu_count(),
        "use_mps": False,  # Metal Performance Shaders (Apple Silicon)
        "batch_size": 32,  # CPU 友好的批处理大小
        "max_length": 512,  # 限制序列长度以节省内存
    }
    
    # 检测 Apple Silicon (M1/M2)
    if platform.machine() == "arm64":
        config["use_mps"] = torch.backends.mps.is_available()
        config["batch_size"] = 64  # M1/M2 可以处理更大批次
        print("🍎 检测到 Apple Silicon，启用优化配置")
    else:
        print("💻 检测到 Intel Mac，使用标准 CPU 配置")
    
    # 设置 PyTorch 线程数
    torch.set_num_threads(config["num_threads"])
    
    return config

def optimize_for_macos():
    """应用 macOS 优化设置"""
    config = get_macos_config()
    
    # 环境变量优化
    os.environ["OMP_NUM_THREADS"] = str(config["num_threads"])
    os.environ["MKL_NUM_THREADS"] = str(config["num_threads"])
    os.environ["TOKENIZERS_PARALLELISM"] = "false"  # 避免警告
    
    print(f"🔧 已优化 macOS 配置:")
    print(f"   - CPU 线程数: {config['num_threads']}")
    print(f"   - 批处理大小: {config['batch_size']}")
    print(f"   - MPS 支持: {config['use_mps']}")
    
    return config

if __name__ == "__main__":
    optimize_for_macos()
