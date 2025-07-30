#!/usr/bin/env python3
"""
金融术语标准化系统快速设置脚本
提供不同配置选项，避免下载大型模型
"""

import os
import sys
import subprocess

def print_banner():
    print("🚀 金融术语标准化系统快速设置")
    print("=" * 50)

def choose_setup_mode():
    """选择设置模式"""
    print("\n请选择设置模式:")
    print("1. 快速模式 (轻量模型, 90MB, 适合测试)")
    print("2. 平衡模式 (中等模型, 420MB, 推荐)")
    print("3. 完整模式 (最佳模型, 2.27GB, 最高精度)")
    print("4. 仅前端模式 (不下载任何模型)")
    
    while True:
        choice = input("\n请输入选择 (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return int(choice)
        print("无效选择，请输入 1-4")

def setup_lightweight():
    """轻量模式设置"""
    print("\n🔧 设置轻量模式...")

    # 创建配置文件
    config_content = '''# 轻量模式配置
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_EMBEDDING_PROVIDER = "huggingface"
'''

    with open("backend/config/runtime_config.py", 'w', encoding='utf-8') as f:
        f.write(config_content)

    # 更新数据库创建脚本
    script_path = "backend/tools/create_financial_terms_db.py"
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换模型选择
        content = content.replace('model_choice = "lightweight"', 'model_choice = "lightweight"')

        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ 已配置轻量级嵌入模型")

    return "sentence-transformers/all-MiniLM-L6-v2"

def setup_balanced():
    """平衡模式设置"""
    print("\n🔧 设置平衡模式...")

    # 创建配置文件
    config_content = '''# 平衡模式配置
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
DEFAULT_EMBEDDING_PROVIDER = "huggingface"
'''

    with open("backend/config/runtime_config.py", 'w', encoding='utf-8') as f:
        f.write(config_content)

    script_path = "backend/tools/create_financial_terms_db.py"
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace('model_choice = "lightweight"', 'model_choice = "balanced"')

        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ 已配置平衡型嵌入模型")

    return "sentence-transformers/all-mpnet-base-v2"

def setup_full():
    """完整模式设置"""
    print("\n🔧 设置完整模式...")
    print("⚠️  注意: 将下载 2.27GB 的模型文件")

    confirm = input("确认继续? (y/N): ").strip().lower()
    if confirm != 'y':
        print("已取消完整模式设置")
        return None

    # 创建配置文件
    config_content = '''# 完整模式配置
DEFAULT_EMBEDDING_MODEL = "BAAI/bge-m3"
DEFAULT_EMBEDDING_PROVIDER = "huggingface"
'''

    with open("backend/config/runtime_config.py", 'w', encoding='utf-8') as f:
        f.write(config_content)

    script_path = "backend/tools/create_financial_terms_db.py"
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace('model_choice = "lightweight"', 'model_choice = "best"')

        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ 已配置最佳嵌入模型")

    return "BAAI/bge-m3"

def setup_frontend_only():
    """仅前端模式"""
    print("\n🔧 设置仅前端模式...")
    print("📝 此模式只启动前端界面，不进行后端模型下载")
    print("💡 适合查看界面效果或前端开发")
    
    return None

def create_database(model_name):
    """创建数据库"""
    if not model_name:
        print("⏭️  跳过数据库创建")
        return
    
    print(f"\n📊 创建金融术语数据库 (使用模型: {model_name})...")
    
    try:
        # 使用绝对路径运行脚本
        script_path = os.path.join(os.getcwd(), "backend", "tools", "create_financial_terms_db.py")
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, timeout=300, cwd=os.getcwd())

        if result.returncode == 0:
            print("✅ 数据库创建成功")
        else:
            print(f"❌ 数据库创建失败: {result.stderr}")
            print(f"标准输出: {result.stdout}")

    except subprocess.TimeoutExpired:
        print("⏰ 数据库创建超时，请手动运行")
    except Exception as e:
        print(f"❌ 数据库创建出错: {e}")

def show_next_steps(mode, model_name):
    """显示后续步骤"""
    print("\n🎉 设置完成!")
    print("=" * 50)
    
    if mode == 4:  # 仅前端模式
        print("📋 后续步骤 (仅前端):")
        print("1. cd frontend")
        print("2. npm install")
        print("3. npm start")
        print("4. 访问 http://localhost:3000")
    else:
        print("📋 后续步骤:")
        print("1. 启动后端:")
        print("   cd backend")
        print("   python3 main.py")
        print("")
        print("2. 启动前端:")
        print("   cd frontend") 
        print("   npm install")
        print("   npm start")
        print("")
        print("3. 访问系统: http://localhost:3000")
        
        if model_name:
            print(f"\n🤖 使用的模型: {model_name}")

def main():
    print_banner()
    
    # 检查必要文件
    if not os.path.exists("万条金融标准术语.csv"):
        print("❌ 未找到金融术语数据文件: 万条金融标准术语.csv")
        return
    
    mode = choose_setup_mode()
    model_name = None
    
    if mode == 1:
        model_name = setup_lightweight()
    elif mode == 2:
        model_name = setup_balanced()
    elif mode == 3:
        model_name = setup_full()
    elif mode == 4:
        model_name = setup_frontend_only()
    
    # 创建数据库 (除了仅前端模式)
    if mode != 4:
        create_database(model_name)
    
    show_next_steps(mode, model_name)

if __name__ == "__main__":
    main()
