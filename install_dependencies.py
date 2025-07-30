#!/usr/bin/env python3
"""
依赖安装脚本
为 macOS 金融术语标准化系统安装必要的 Python 依赖
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"🐍 Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 版本过低，需要 Python 3.8+")
        return False
    
    print("✅ Python 版本符合要求")
    return True

def check_system():
    """检查系统信息"""
    print(f"💻 操作系统: {platform.system()} {platform.release()}")
    print(f"🏗️  架构: {platform.machine()}")
    
    if platform.system() == "Darwin":
        if platform.machine() == "arm64":
            print("🍎 检测到 Apple Silicon (M1/M2)")
        else:
            print("🍎 检测到 Intel Mac")
    
    return True

def upgrade_pip():
    """升级 pip"""
    print("\n📦 升级 pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✅ pip 升级成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  pip 升级失败: {e}")
        return False

def install_core_dependencies():
    """安装核心依赖"""
    print("\n🔧 安装核心依赖...")
    
    # 核心依赖列表 - 使用项目实际版本
    core_deps = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "pydantic==1.10.22",
        "pydantic-settings==2.0.0",
        "python-multipart==0.0.5",
        "python-dotenv==1.0.1",
        "requests==2.26.0",
        "httpx==0.27.2",
        "aiofiles==23.2.1",
        "pandas==2.0.3",
        "numpy==1.24.3",
        "tqdm==4.66.4"
    ]
    
    for dep in core_deps:
        try:
            print(f"  安装: {dep}")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 安装失败: {dep}")
            return False
    
    print("✅ 核心依赖安装完成")
    return True

def install_ml_dependencies():
    """安装机器学习依赖"""
    print("\n🤖 安装机器学习依赖...")
    
    # 先安装 PyTorch CPU 版本
    try:
        print("  安装 PyTorch (CPU 版本)...")
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "torch==2.2.2", "torchvision==0.17.2", "torchaudio==2.2.2",
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ], check=True, capture_output=True)
        print("  ✅ PyTorch 安装成功")
    except subprocess.CalledProcessError:
        print("  ❌ PyTorch 安装失败")
        return False
    
    # 安装其他 ML 依赖 - 使用项目实际版本
    ml_deps = [
        "transformers==4.46.3",
        "sentence-transformers==3.2.1",
        "huggingface-hub==0.26.5",
        "tokenizers==0.15.2",
        "safetensors==0.4.5",
        "scipy==1.10.1",
        "scikit-learn==1.3.2"
    ]
    
    for dep in ml_deps:
        try:
            print(f"  安装: {dep}")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print(f"  ❌ 安装失败: {dep}")
            return False
    
    print("✅ 机器学习依赖安装完成")
    return True

def install_vector_db():
    """安装向量数据库依赖"""
    print("\n🗄️  安装向量数据库依赖...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pymilvus==2.5.14"],
                      check=True, capture_output=True)
        print("✅ Milvus 客户端安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ Milvus 客户端安装失败")
        return False

def install_langchain():
    """安装 LangChain 依赖"""
    print("\n🔗 安装 LangChain 依赖...")
    
    langchain_deps = [
        "langchain==0.2.17",
        "langchain-community==0.2.17",
        "langchain-core==0.2.42",
        "langchain-openai==0.1.25",
        "langchain-huggingface==0.1.2",
        "langchain-aws==0.2.4",
        "openai==1.97.1",
        "boto3==1.35.67",
        "langsmith==0.1.143"
    ]
    
    for dep in langchain_deps:
        try:
            print(f"  安装: {dep}")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print(f"  ❌ 安装失败: {dep}")
            return False
    
    print("✅ LangChain 依赖安装完成")
    return True

def install_from_requirements():
    """从 requirements 文件安装"""
    req_file = "requirements_mac(no GPU).txt"
    
    if not os.path.exists(req_file):
        print(f"❌ 未找到 {req_file}")
        return False
    
    print(f"\n📋 从 {req_file} 安装依赖...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], 
                      check=True)
        print("✅ 所有依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def verify_installation():
    """验证安装"""
    print("\n🔍 验证安装...")
    
    test_imports = [
        ("fastapi", "FastAPI"),
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("sentence_transformers", "Sentence Transformers"),
        ("pymilvus", "Milvus"),
        ("pandas", "Pandas"),
        ("langchain", "LangChain"),
        ("langchain_community", "LangChain Community"),
        ("langchain_huggingface", "LangChain HuggingFace"),
        ("pydantic", "Pydantic"),
        ("uvicorn", "Uvicorn"),
        ("dotenv", "Python-dotenv"),
        ("numpy", "NumPy"),
        ("tqdm", "TQDM")
    ]
    
    success_count = 0
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"  ✅ {name}")
            success_count += 1
        except ImportError:
            print(f"  ❌ {name}")
    
    print(f"\n📊 验证结果: {success_count}/{len(test_imports)} 成功")
    return success_count == len(test_imports)

def main():
    """主函数"""
    print("🚀 macOS 金融术语标准化系统依赖安装")
    print("=" * 50)
    
    # 系统检查
    if not check_python_version():
        return False
    
    check_system()
    
    # 选择安装方式
    print("\n🤔 选择安装方式:")
    print("1. 完整安装 (推荐)")
    print("2. 分步安装")
    print("3. 仅从 requirements.txt 安装")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == "3":
        success = install_from_requirements()
    elif choice == "2":
        # 分步安装
        steps = [
            ("升级 pip", upgrade_pip),
            ("核心依赖", install_core_dependencies),
            ("机器学习依赖", install_ml_dependencies),
            ("向量数据库", install_vector_db),
            ("LangChain", install_langchain)
        ]
        
        success = True
        for step_name, step_func in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            if not step_func():
                success = False
                break
    else:
        # 完整安装
        success = (upgrade_pip() and 
                  install_core_dependencies() and
                  install_ml_dependencies() and
                  install_vector_db() and
                  install_langchain())
    
    # 验证安装
    if success:
        verify_installation()
        print("\n🎉 依赖安装完成！")
        print("\n📋 下一步:")
        print("1. 运行: python3 start_macos.py")
        print("2. 或手动启动后端: cd backend && python3 main.py")
    else:
        print("\n❌ 依赖安装失败")
        print("💡 建议:")
        print("1. 检查网络连接")
        print("2. 尝试使用虚拟环境")
        print("3. 手动安装失败的包")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
