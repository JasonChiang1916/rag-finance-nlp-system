"""
模型配置文件
提供不同性能需求的模型选择
"""

# 嵌入模型配置
EMBEDDING_MODELS = {
    "lightweight": {
        "name": "sentence-transformers/all-MiniLM-L6-v2",
        "size": "90MB",
        "dimension": 384,
        "description": "轻量级模型，快速启动，适合开发测试"
    },
    "balanced": {
        "name": "sentence-transformers/all-mpnet-base-v2", 
        "size": "420MB",
        "dimension": 768,
        "description": "平衡性能和大小，推荐用于生产环境"
    },
    "best": {
        "name": "BAAI/bge-m3",
        "size": "2.27GB", 
        "dimension": 1024,
        "description": "最佳性能，支持多语言，适合高精度需求"
    }
}

# NER模型配置
NER_MODELS = {
    "general": {
        "name": "dbmdz/bert-large-cased-finetuned-conll03-english",
        "size": "1.3GB",
        "description": "通用英文NER模型，识别人名、组织、地点"
    },
    "lightweight": {
        "name": "dslim/bert-base-NER",
        "size": "420MB", 
        "description": "轻量级NER模型"
    },
    "financial": {
        "name": "models/Financial-NER",  # 本地模型路径
        "size": "varies",
        "description": "专门的金融领域NER模型（如果可用）"
    }
}

# 默认配置
DEFAULT_CONFIG = {
    "embedding_model": "lightweight",  # 默认使用轻量模型
    "ner_model": "lightweight",
    "database_name": "financial_terms_bge_m3",
    "collection_name": "financial_terms"
}

def get_embedding_model_config(model_type="lightweight"):
    """获取嵌入模型配置"""
    return EMBEDDING_MODELS.get(model_type, EMBEDDING_MODELS["lightweight"])

def get_ner_model_config(model_type="lightweight"):
    """获取NER模型配置"""
    return NER_MODELS.get(model_type, NER_MODELS["lightweight"])

def print_model_options():
    """打印所有可用的模型选项"""
    print("🤖 可用的嵌入模型:")
    for key, config in EMBEDDING_MODELS.items():
        print(f"  {key}: {config['name']} ({config['size']}) - {config['description']}")
    
    print("\n🔍 可用的NER模型:")
    for key, config in NER_MODELS.items():
        print(f"  {key}: {config['name']} ({config['size']}) - {config['description']}")

if __name__ == "__main__":
    print_model_options()
