from pymilvus import MilvusClient, DataType, FieldSchema, CollectionSchema
import pandas as pd
from tqdm import tqdm
import logging
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import torch
import numpy as np

load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化嵌入函数 - 可选择轻量模型
# 选项1: BGE-M3 (2.27GB) - 最佳效果
# 选项2: all-MiniLM-L6-v2 (90MB) - 轻量快速
# 选项3: all-mpnet-base-v2 (420MB) - 平衡选择

model_choice = "lightweight"  # 可选: "best", "lightweight", "balanced"

if model_choice == "best":
    model_name = 'BAAI/bge-m3'
elif model_choice == "lightweight":
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
else:  # balanced
    model_name = 'sentence-transformers/all-mpnet-base-v2'

# 创建SentenceTransformer嵌入函数
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
embedding_model = SentenceTransformer(model_name, device=device)

def embedding_function(texts):
    """嵌入函数，将文本转换为向量"""
    if isinstance(texts, str):
        texts = [texts]
    embeddings = embedding_model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist() if len(texts) > 1 else embeddings[0].tolist()

print(f"使用嵌入模型: {model_name}")

# 文件路径
file_path = "万条金融标准术语.csv"

# 根据模型选择确定数据库路径
if model_choice == "best":
    db_path = "backend/db/financial_terms_bge_m3.db"
elif model_choice == "lightweight":
    db_path = "backend/db/financial_terms_minilm.db"
else:  # balanced
    db_path = "backend/db/financial_terms_mpnet.db"

# 连接到 Milvus
client = MilvusClient(db_path)

collection_name = "financial_terms"

# 加载数据
logging.info("Loading financial terms data from CSV")
df = pd.read_csv(file_path, 
                 names=['term_name', 'term_type'],  # 指定列名
                 dtype=str, 
                 low_memory=False,
                 ).fillna("NA")

logging.info(f"Loaded {len(df)} financial terms")

# 获取向量维度（使用一个样本文档）
sample_doc = "Sample Financial Term"
sample_embedding = embedding_function(sample_doc)
vector_dim = len(sample_embedding)
logging.info(f"Vector dimension: {vector_dim}")

# 构造Schema - 适配金融术语结构
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=vector_dim), # BGE-m3 向量
    FieldSchema(name="term_id", dtype=DataType.VARCHAR, max_length=50),  # 术语ID
    FieldSchema(name="term_name", dtype=DataType.VARCHAR, max_length=200),  # 术语名称
    FieldSchema(name="term_type", dtype=DataType.VARCHAR, max_length=20),  # 术语类型 (FINTERM)
    FieldSchema(name="domain", dtype=DataType.VARCHAR, max_length=50),  # 金融领域
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=50),  # 术语分类
    FieldSchema(name="input_file", dtype=DataType.VARCHAR, max_length=500),
]
schema = CollectionSchema(fields, 
                          "Financial Terms Collection", 
                          enable_dynamic_field=True)

# 如果集合存在，先删除
if client.has_collection(collection_name):
    client.drop_collection(collection_name)
    logging.info(f"Dropped existing collection: {collection_name}")

# 创建集合
client.create_collection(
    collection_name=collection_name,
    schema=schema,
)
logging.info(f"Created new collection: {collection_name}")

# 在创建集合后添加索引
index_params = client.prepare_index_params()
index_params.add_index(
    field_name="vector",  # 指定要为哪个字段创建索引，这里是向量字段
    index_type="AUTOINDEX",  # 使用自动索引类型，Milvus会根据数据特性选择最佳索引
    metric_type="COSINE",  # 使用余弦相似度作为向量相似度度量方式
    params={"nlist": 1024}  # 索引参数：nlist表示聚类中心的数量，值越大检索精度越高但速度越慢
)

client.create_index(
    collection_name=collection_name,
    index_params=index_params
)
logging.info("Created vector index")

# 批量处理
batch_size = 1024

for start_idx in tqdm(range(0, len(df), batch_size), desc="Processing financial terms batches"):
    end_idx = min(start_idx + batch_size, len(df))
    batch_df = df.iloc[start_idx:end_idx]

    # 准备文档 - 金融术语
    docs = []
    for _, row in batch_df.iterrows():
        # 使用术语名称作为文档内容
        docs.append(row['term_name'])

    # 生成嵌入
    try:
        embeddings = embedding_function(docs)
        logging.info(f"Generated embeddings for batch {start_idx // batch_size + 1}")
    except Exception as e:
        logging.error(f"Error generating embeddings for batch {start_idx // batch_size + 1}: {e}")
        continue

    # 准备数据 - 金融术语
    data = [
        {
            "vector": embeddings[idx],
            "term_id": f"FIN_{start_idx + idx:06d}",  # 生成术语ID
            "term_name": str(row['term_name']),
            "term_type": str(row['term_type']),
            "domain": "Finance",  # 统一设为金融领域
            "category": "Standard",  # 标准术语
            "input_file": file_path
        } for idx, (_, row) in enumerate(batch_df.iterrows())
    ]

    # 插入数据 - 批量插入金融术语
    try:
        res = client.insert(
            collection_name=collection_name,
            data=data
        )
        logging.info(f"Inserted batch {start_idx // batch_size + 1}, result: {res}")
    except Exception as e:
        logging.error(f"Error inserting batch {start_idx // batch_size + 1}: {e}")

logging.info("Financial terms insert process completed.")

# 示例查询 - 测试金融术语搜索
test_queries = ["investment", "bank", "loan", "stock", "bond"]

for query in test_queries:
    query_embedding = embedding_function(query)

    # 搜索余弦相似度最高的金融术语
    search_result = client.search(
        collection_name=collection_name,
        data=[query_embedding],
        limit=3,
        output_fields=["term_name",
                       "term_type",
                       "domain",
                       "category"
                       ]
    )
    logging.info(f"Search result for '{query}': {[hit['entity']['term_name'] for hit in search_result[0]]}")

# 统计信息
stats = client.get_collection_stats(collection_name)
logging.info(f"Collection stats: {stats}")
