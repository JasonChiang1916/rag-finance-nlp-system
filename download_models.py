#!/usr/bin/env python3
"""
模型下载脚本
自动下载项目所需的模型文件
"""

import os
import subprocess
import sys

def check_git_lfs():
    """检查 Git LFS 是否安装"""
    try:
        result = subprocess.run(['git', 'lfs', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git LFS 已安装")
            return True
        else:
            print("❌ Git LFS 未安装")
            return False
    except FileNotFoundError:
        print("❌ Git 或 Git LFS 未安装")
        return False

def install_git_lfs():
    """安装 Git LFS"""
    print("🔧 正在安装 Git LFS...")
    
    # 检测操作系统
    import platform
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        try:
            subprocess.run(['brew', 'install', 'git-lfs'], check=True)
            subprocess.run(['git', 'lfs', 'install'], check=True)
            print("✅ Git LFS 安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ Git LFS 安装失败，请手动安装: brew install git-lfs")
            return False
    elif system == "linux":
        print("请手动安装 Git LFS:")
        print("  Ubuntu/Debian: sudo apt install git-lfs")
        print("  然后运行: git lfs install")
        return False
    else:
        print("请手动安装 Git LFS 并运行: git lfs install")
        return False

def download_model(model_url, target_dir=None):
    """下载模型"""
    model_name = model_url.split('/')[-1]
    print(f"📥 下载模型: {model_name}")
    
    try:
        os.chdir("backend/models")
        
        # 使用 git lfs clone 下载
        cmd = ['git', 'lfs', 'clone', f'https://huggingface.co/{model_url}']
        subprocess.run(cmd, check=True)
        
        # 如果指定了目标目录，进行重命名
        if target_dir and target_dir != model_name:
            if os.path.exists(target_dir):
                subprocess.run(['rm', '-rf', target_dir], check=True)
            subprocess.run(['mv', model_name, target_dir], check=True)
            print(f"✅ 模型已下载并重命名为: {target_dir}")
        else:
            print(f"✅ 模型已下载: {model_name}")
        
        os.chdir("../..")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 下载失败: {e}")
        os.chdir("../..")
        return False

def main():
    print("🤖 金融术语标准化系统 - 模型下载工具")
    print("=" * 50)
    
    # 检查 Git LFS
    if not check_git_lfs():
        if not install_git_lfs():
            print("请先安装 Git LFS 后再运行此脚本")
            sys.exit(1)
    
    # 创建 models 目录
    os.makedirs("backend/models", exist_ok=True)
    
    print("\n📋 可下载的模型:")
    print("1. 基础模型 (必需)")
    print("2. 中文模型 (可选)")
    print("3. 高性能模型 (可选)")
    print("4. 全部模型")
    
    choice = input("\n请选择要下载的模型 (1-4): ").strip()
    
    models_to_download = []
    
    if choice == "1":
        models_to_download = [
            ("dbmdz/bert-large-cased-finetuned-conll03-english", None),
            ("sentence-transformers/all-MiniLM-L6-v2", None),
            ("dslim/bert-base-NER", None)
        ]
    elif choice == "2":
        models_to_download = [
            ("hfl/chinese-bert-wwm-ext", "Financial-NER")
        ]
    elif choice == "3":
        models_to_download = [
            ("sentence-transformers/all-mpnet-base-v2", None),
            ("BAAI/bge-m3", None)
        ]
    elif choice == "4":
        models_to_download = [
            ("dbmdz/bert-large-cased-finetuned-conll03-english", None),
            ("sentence-transformers/all-MiniLM-L6-v2", None),
            ("dslim/bert-base-NER", None),
            ("hfl/chinese-bert-wwm-ext", "Financial-NER"),
            ("sentence-transformers/all-mpnet-base-v2", None),
            ("BAAI/bge-m3", None)
        ]
    else:
        print("❌ 无效选择")
        sys.exit(1)
    
    print(f"\n🚀 开始下载 {len(models_to_download)} 个模型...")
    
    success_count = 0
    for model_url, target_dir in models_to_download:
        if download_model(model_url, target_dir):
            success_count += 1
    
    print(f"\n📊 下载完成: {success_count}/{len(models_to_download)} 成功")
    
    if success_count == len(models_to_download):
        print("🎉 所有模型下载成功！现在可以启动系统了。")
    else:
        print("⚠️  部分模型下载失败，系统仍可运行但可能需要在线下载模型。")

if __name__ == "__main__":
    main()
