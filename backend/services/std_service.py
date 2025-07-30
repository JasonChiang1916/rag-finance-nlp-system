from pymilvus import MilvusClient
from dotenv import load_dotenv
from utils.embedding_factory import EmbeddingFactory
from utils.embedding_config import EmbeddingProvider, EmbeddingConfig
import os
from typing import List, Dict
import logging

# 尝试加载运行时配置
try:
    from config.runtime_config import DEFAULT_EMBEDDING_MODEL, DEFAULT_EMBEDDING_PROVIDER
except ImportError:
    # 如果没有配置文件，使用轻量模型作为默认
    DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    DEFAULT_EMBEDDING_PROVIDER = "huggingface"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class StdService:
    """
    金融术语标准化服务
    使用向量数据库进行金融术语的标准化和相似度搜索
    """
    def __init__(self,
                 provider=None,
                 model=None,
                 db_path="db/financial_terms_minilm.db",
                 collection_name="financial_terms"):
        """
        初始化标准化服务

        Args:
            provider: 嵌入模型提供商 (openai/bedrock/huggingface)
            model: 使用的模型名称
            db_path: Milvus 数据库路径
            collection_name: 集合名称
        """
        # 使用配置文件中的默认值
        if provider is None:
            provider = DEFAULT_EMBEDDING_PROVIDER
        if model is None:
            model = DEFAULT_EMBEDDING_MODEL
        # 根据 provider 字符串匹配正确的枚举值
        provider_mapping = {
            'openai': EmbeddingProvider.OPENAI,
            'bedrock': EmbeddingProvider.BEDROCK,
            'huggingface': EmbeddingProvider.HUGGINGFACE
        }
        
        # 创建 embedding 函数
        embedding_provider = provider_mapping.get(provider.lower())
        if embedding_provider is None:
            raise ValueError(f"Unsupported provider: {provider}")
            
        config = EmbeddingConfig(
            provider=embedding_provider,
            model_name=model
        )
        self.embedding_func = EmbeddingFactory.create_embedding_function(config)
        
        # 连接 Milvus
        self.client = MilvusClient(db_path)
        self.collection_name = collection_name

        # 加载集合（如果存在）
        try:
            # 检查集合是否存在
            collections = self.client.list_collections()
            if self.collection_name in collections:
                self.client.load_collection(self.collection_name)
                logger.info(f"成功加载集合: {self.collection_name}")
            else:
                logger.warning(f"集合 {self.collection_name} 不存在，请先运行数据库创建脚本")
                logger.info("提示: 运行 'python3 tools/create_financial_terms_db.py' 创建数据库")
        except Exception as e:
            logger.error(f"加载集合失败: {e}")
            logger.warning("系统将继续启动，但标准化功能可能不可用")

    def search_similar_terms(self, query: str, limit: int = 5) -> List[Dict]:
        """
        搜索与查询文本相似的金融术语

        Args:
            query: 查询文本
            limit: 返回结果的最大数量

        Returns:
            包含相似术语信息的列表，每个术语包含：
            - term_id: 术语ID
            - term_name: 术语名称
            - term_type: 术语类型
            - domain: 金融领域
            - category: 术语分类
            - distance: 相似度距离
        """
        # 获取查询的向量表示
        query_embedding = self.embedding_func.embed_query(query)
        
        # 设置搜索参数
        search_params = {
            "collection_name": self.collection_name,
            "data": [query_embedding],
            "limit": limit,
            "output_fields": [
                "term_id", "term_name", "term_type",
                "domain", "category"
            ],
            # "filter": "domain == 'Finance'"
        }
        
        # 搜索相似项
        search_result = self.client.search(**search_params)

        results = []
        for hit in search_result[0]:
            results.append({
                "concept_id": hit['entity'].get('concept_id'),
                "concept_name": hit['entity'].get('concept_name'),
                "domain_id": hit['entity'].get('domain_id'),
                "vocabulary_id": hit['entity'].get('vocabulary_id'),
                "concept_class_id": hit['entity'].get('concept_class_id'),
                "standard_concept": hit['entity'].get('standard_concept'),
                "concept_code": hit['entity'].get('concept_code'),
                "synonyms": hit['entity'].get('synonyms'),
                "distance": float(hit['distance'])
            })

        return results

    def __del__(self):
        """清理资源，释放集合"""
        if hasattr(self, 'client') and hasattr(self, 'collection_name'):
            self.client.release_collection(self.collection_name)