#!/usr/bin/env python3
"""
macOS 专用启动脚本
针对 macOS CPU 环境优化的金融术语标准化系统启动器
"""

import os
import sys
import subprocess
import platform
import time

def check_macos_compatibility():
    """检查 macOS 兼容性"""
    print("🍎 macOS 兼容性检查")
    print("=" * 40)
    
    # 检查操作系统
    if platform.system() != "Darwin":
        print("❌ 此脚本仅适用于 macOS")
        return False
    
    print(f"✅ 操作系统: {platform.system()} {platform.release()}")
    print(f"✅ 架构: {platform.machine()}")
    
    # 检查 Python 版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Python 版本过低: {python_version.major}.{python_version.minor}")
        print("   需要 Python 3.8+")
        return False
    
    print(f"✅ Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要文件
    required_files = [
        "万条金融标准术语.csv",
        "backend/main.py",
        "frontend/package.json"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ 文件存在: {file_path}")
        else:
            print(f"❌ 文件缺失: {file_path}")
            return False
    
    return True

def install_dependencies():
    """安装依赖"""
    print("\n📦 安装 Python 依赖...")
    
    try:
        # 检查是否有 requirements 文件
        req_file = "requirements_mac(no GPU).txt"
        if os.path.exists(req_file):
            print(f"使用: {req_file}")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], check=True)
        else:
            # 安装基本依赖
            basic_deps = [
                "fastapi", "uvicorn", "transformers", "torch", 
                "sentence-transformers", "pymilvus", "pandas", "tqdm"
            ]
            for dep in basic_deps:
                print(f"安装: {dep}")
                subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
        
        print("✅ Python 依赖安装完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def setup_lightweight_model():
    """设置轻量模型"""
    print("\n🚀 配置轻量模型 (macOS CPU 优化)...")
    
    # 应用 macOS 优化配置
    sys.path.append('backend')
    try:
        from config.macos_config import optimize_for_macos
        optimize_for_macos()
    except ImportError:
        print("⚠️  macOS 配置模块未找到，使用默认设置")
    
    # 设置轻量模型
    script_path = "backend/tools/create_financial_terms_db.py"
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 确保使用轻量模型
        content = content.replace('model_choice = "best"', 'model_choice = "lightweight"')
        content = content.replace('model_choice = "balanced"', 'model_choice = "lightweight"')
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 已配置轻量级模型 (90MB)")
    
    return True

def create_database():
    """创建数据库"""
    print("\n📊 创建金融术语数据库...")
    print("💡 使用轻量模型，下载约 90MB")
    
    try:
        os.chdir("backend")
        
        # 显示进度
        print("⏳ 正在下载模型和创建数据库...")
        
        process = subprocess.Popen([
            sys.executable, "tools/create_financial_terms_db.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 实时显示输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        return_code = process.poll()
        os.chdir("..")
        
        if return_code == 0:
            print("✅ 数据库创建成功")
            return True
        else:
            print("❌ 数据库创建失败")
            return False
            
    except Exception as e:
        print(f"❌ 数据库创建出错: {e}")
        os.chdir("..")
        return False

def cleanup_database_locks():
    """清理数据库锁文件"""
    print("🧹 清理数据库锁文件...")

    import glob
    lock_files = glob.glob("backend/db/.*.db.lock")
    for lock_file in lock_files:
        try:
            os.remove(lock_file)
            print(f"  清理: {lock_file}")
        except:
            pass

def start_backend():
    """启动后端服务"""
    print("\n🔧 启动后端服务...")

    # 清理可能的锁文件
    cleanup_database_locks()

    try:
        os.chdir("backend")
        print("🚀 后端服务启动中... (Ctrl+C 停止)")
        print("📡 API 地址: http://localhost:8000")
        
        subprocess.run([sys.executable, "main.py"])
        
    except KeyboardInterrupt:
        print("\n⏹️  后端服务已停止")
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
    finally:
        os.chdir("..")

def show_manual_steps():
    """显示手动步骤"""
    print("\n📋 手动启动步骤:")
    print("=" * 40)
    print("1. 启动后端:")
    print("   cd backend")
    print("   uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    print("")
    print("2. 新终端启动前端:")
    print("   cd frontend")
    print("   npm install")
    print("   npm start")
    print("")
    print("3. 访问: http://localhost:3000")

def main():
    """主函数"""
    print("🍎 macOS 金融术语标准化系统启动器")
    print("=" * 50)
    
    # 兼容性检查
    if not check_macos_compatibility():
        return
    
    # 询问是否自动设置
    print("\n🤔 选择启动模式:")
    print("1. 自动设置 (推荐)")
    print("2. 仅显示手动步骤")
    
    choice = input("请选择 (1-2): ").strip()
    
    if choice == "2":
        show_manual_steps()
        return
    
    # 自动设置流程
    steps = [
        ("安装依赖", install_dependencies),
        ("配置轻量模型", setup_lightweight_model),
        ("创建数据库", create_database),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_func():
            print(f"❌ {step_name} 失败")
            show_manual_steps()
            return
    
    print("\n🎉 设置完成！")
    
    # 询问是否启动后端
    start_now = input("\n是否现在启动后端服务? (y/N): ").strip().lower()
    if start_now == 'y':
        start_backend()
    else:
        show_manual_steps()

if __name__ == "__main__":
    main()
