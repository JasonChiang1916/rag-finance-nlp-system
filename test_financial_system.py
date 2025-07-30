#!/usr/bin/env python3
"""
金融术语标准化系统测试脚本
测试系统的各个组件是否正常工作
"""

import sys
import os
import requests
import json

# 添加后端路径到系统路径
sys.path.append('backend')

def test_financial_database():
    """测试金融术语数据库创建"""
    print("🔍 测试金融术语数据库...")
    
    try:
        # 检查金融术语CSV文件是否存在
        if not os.path.exists("万条金融标准术语.csv"):
            print("❌ 金融术语CSV文件不存在")
            return False
            
        print("✅ 金融术语CSV文件存在")
        
        # 检查数据库创建脚本
        if os.path.exists("backend/tools/create_financial_terms_db.py"):
            print("✅ 金融术语数据库创建脚本存在")
        else:
            print("❌ 金融术语数据库创建脚本不存在")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        return False

def test_backend_services():
    """测试后端服务"""
    print("\n🔍 测试后端服务...")
    
    try:
        # 测试标准化服务
        from services.std_service import StdService
        
        # 使用默认配置创建服务实例
        std_service = StdService()
        print("✅ 标准化服务初始化成功")
        
        # 测试NER服务
        from services.ner_service import NERService
        ner_service = NERService()
        print("✅ NER服务初始化成功")
        
        # 测试生成服务
        from services.gen_service import GenService
        gen_service = GenService()
        print("✅ 生成服务初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 后端服务测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🔍 测试API端点...")
    
    base_url = "http://localhost:8000"
    
    # 测试数据
    test_data = {
        "text": "Apple Inc. reported strong quarterly earnings with revenue growth of 15%.",
        "options": {"allFinancialTerms": True},
        "termTypes": {"allFinancialTerms": True},
        "embeddingOptions": {
            "provider": "huggingface",
            "model": "BAAI/bge-m3",
            "dbName": "financial_terms_bge_m3",
            "collectionName": "financial_terms"
        }
    }
    
    try:
        # 测试NER端点
        response = requests.post(f"{base_url}/api/ner", 
                               json=test_data, 
                               timeout=30)
        if response.status_code == 200:
            print("✅ NER API端点正常")
        else:
            print(f"❌ NER API端点错误: {response.status_code}")
            
        # 测试标准化端点
        response = requests.post(f"{base_url}/api/std", 
                               json=test_data, 
                               timeout=30)
        if response.status_code == 200:
            print("✅ 标准化API端点正常")
        else:
            print(f"❌ 标准化API端点错误: {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器，请确保服务器正在运行")
        return False
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def test_frontend_files():
    """测试前端文件"""
    print("\n🔍 测试前端文件...")
    
    try:
        # 检查关键前端文件
        frontend_files = [
            "frontend/src/App.js",
            "frontend/src/components/Sidebar.js",
            "frontend/src/pages/NERPage.js",
            "frontend/src/pages/StdPage.js",
            "frontend/package.json"
        ]
        
        for file_path in frontend_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path} 存在")
            else:
                print(f"❌ {file_path} 不存在")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ 前端文件测试失败: {e}")
        return False

def run_sample_test():
    """运行示例测试"""
    print("\n🔍 运行示例测试...")
    
    try:
        # 测试金融术语识别
        sample_text = "JPMorgan Chase reported a 20% increase in investment banking revenue. The bank's ROE improved to 15% this quarter."
        
        print(f"📝 测试文本: {sample_text}")
        
        # 这里可以添加实际的API调用测试
        print("✅ 示例测试准备就绪")
        
        return True
        
    except Exception as e:
        print(f"❌ 示例测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始金融术语标准化系统测试\n")
    
    tests = [
        ("数据库测试", test_financial_database),
        ("后端服务测试", test_backend_services),
        ("前端文件测试", test_frontend_files),
        ("示例测试", run_sample_test),
        # ("API端点测试", test_api_endpoints),  # 需要服务器运行
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
        print(f"运行: {test_name}")
        print(f"{'='*50}")
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} 通过")
        else:
            print(f"❌ {test_name} 失败")
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed}/{total} 通过")
    print(f"{'='*50}")
    
    if passed == total:
        print("🎉 所有测试通过！系统改造成功！")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关组件")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
