from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from services.ner_service import NERService
from services.std_service import StdService
from services.abbr_service import AbbrService
from services.corr_service import CorrService
from services.gen_service import GenService
from typing import List, Dict, Optional, Literal, Union, Any
import logging

# 尝试加载运行时配置
try:
    from config.runtime_config import DEFAULT_EMBEDDING_MODEL, DEFAULT_EMBEDDING_PROVIDER
except ImportError:
    # 如果没有配置文件，使用轻量模型作为默认
    DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    DEFAULT_EMBEDDING_PROVIDER = "huggingface"

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI()

# 配置跨域资源共享
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化各个服务
ner_service = NERService()  # 命名实体识别服务
standardization_service = StdService()  # 术语标准化服务
abbr_service = AbbrService()  # 缩写扩展服务
gen_service = GenService()  # 文本生成服务
corr_service = CorrService()  # 拼写纠正服务

# 基础模型类
class BaseInputModel(BaseModel):
    """基础输入模型，包含所有模型共享的字段"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    llmOptions: Dict[str, str] = Field(
        default_factory=lambda: {
            "provider": "ollama",
            "model": "qwen2.5:7b"
        },
        description="大语言模型配置选项"
    )

class EmbeddingOptions(BaseModel):
    """向量数据库配置选项"""
    provider: Literal["huggingface", "openai", "bedrock"] = Field(
        default="huggingface",
        description="向量数据库提供商"
    )
    model: str = Field(
        default=DEFAULT_EMBEDDING_MODEL,
        description="嵌入模型名称"
    )
    dbName: str = Field(
        default="financial_terms_minilm",
        description="向量数据库名称"
    )
    collectionName: str = Field(
        default="financial_terms",
        description="集合名称"
    )

class TextInput(BaseInputModel):
    """文本输入模型，用于标准化和命名实体识别"""
    text: str = Field(..., description="输入文本")
    options: Dict[str, bool] = Field(
        default_factory=dict,
        description="处理选项"
    )
    termTypes: Dict[str, bool] = Field(
        default_factory=dict,
        description="术语类型"
    )
    embeddingOptions: EmbeddingOptions = Field(
        default_factory=EmbeddingOptions,
        description="向量数据库配置选项"
    )

class AbbrInput(BaseInputModel):
    """缩写扩展输入模型"""
    text: str = Field(..., description="输入文本")
    context: str = Field(
        default="",
        description="上下文信息"
    )
    method: Literal["simple_ollama", "query_db_llm_rerank", "llm_rank_query_db"] = Field(
        default="simple_ollama",
        description="处理方法"
    )
    embeddingOptions: Optional[EmbeddingOptions] = Field(
        default_factory=EmbeddingOptions,
        description="向量数据库配置选项"
    )

class ErrorOptions(BaseModel):
    """错误生成选项"""
    probability: float = Field(
        default=0.3,
        description="错误生成概率",
        ge=0.0,
        le=1.0
    )
    maxErrors: int = Field(
        default=5,
        description="最大错误数量",
        ge=1
    )
    keyboard: Literal["qwerty", "azerty"] = Field(
        default="qwerty",
        description="键盘布局"
    )

class CorrInput(BaseInputModel):
    """拼写纠正输入模型"""
    text: str = Field(..., description="输入文本")
    method: Literal["correct_spelling", "add_mistakes"] = Field(
        default="correct_spelling",
        description="处理方法"
    )
    errorOptions: ErrorOptions = Field(
        default_factory=ErrorOptions,
        description="错误生成选项"
    )

class CompanyInfo(BaseModel):
    """公司信息模型"""
    name: str = Field(..., description="公司名称")
    sector: Optional[str] = Field(
        None,
        description="行业板块"
    )
    market_cap: Optional[str] = Field(
        None,
        description="市值"
    )
    financial_history: Optional[str] = Field(
        None,
        description="财务历史"
    )

class GenInput(BaseInputModel):
    """金融内容生成输入模型"""
    company_info: CompanyInfo = Field(..., description="公司信息")
    financial_data: List[str] = Field(..., description="财务数据列表")
    analysis_type: str = Field(
        default="",
        description="分析类型"
    )
    recommendations: str = Field(
        default="",
        description="建议"
    )
    market_data: List[str] = Field(
        default_factory=list,
        description="市场数据"
    )
    portfolio_info: str = Field(
        default="",
        description="投资组合信息"
    )
    market_conditions: Dict = Field(
        default_factory=dict,
        description="市场条件"
    )
    method: Literal["generate_financial_report", "generate_investment_analysis", "generate_risk_assessment"] = Field(
        default="generate_financial_report",
        description="生成方法"
    )

# API 端点：术语标准化
@app.post("/api/std")
async def standardization(input: TextInput):
    try:
        # 记录请求信息
        logger.info(f"Received request: text={input.text}, options={input.options}, embeddingOptions={input.embeddingOptions}")

        # 配置术语类型
        all_financial_terms = input.options.pop('allFinancialTerms', False)
        term_types = {'allFinancialTerms': all_financial_terms}

        # 进行命名实体识别
        ner_results = ner_service.process(input.text, input.options, term_types)

        # 初始化标准化服务
        standardization_service = StdService(
            provider=input.embeddingOptions.provider,
            model=input.embeddingOptions.model,
            db_path=f"db/{input.embeddingOptions.dbName}.db",
            collection_name=input.embeddingOptions.collectionName
        )

        # 获取识别到的实体
        entities = ner_results.get('entities', [])
        if not entities:
            return {"message": "No financial terms have been recognized", "standardized_terms": []}

        # 标准化每个实体
        standardized_results = []
        for entity in entities:
            std_result = standardization_service.search_similar_terms(entity['word'])
            standardized_results.append({
                "original_term": entity['word'],
                "entity_group": entity['entity_group'],
                "standardized_results": std_result
            })

        return {
            "message": f"{len(entities)} financial terms have been recognized and standardized",
            "standardized_terms": standardized_results
        }

    except Exception as e:
        logger.error(f"Error in standardization processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# API 端点：命名实体识别
@app.post("/api/ner")
async def ner(input: TextInput):
    try:
        logger.info(f"Received NER request: text={input.text}, options={input.options}, termTypes={input.termTypes}")
        results = ner_service.process(input.text, input.options, input.termTypes)
        return results
    except Exception as e:
        logger.error(f"Error in NER processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# API 端点：拼写纠正
@app.post("/api/corr")
async def correct_notes(input: CorrInput):
    try:
        if input.method == "correct_spelling":  # 拼写纠正
            return corr_service.correct_spelling(input.text, input.llmOptions)
        elif input.method == "add_mistakes":  # 添加错误（测试用）
            return corr_service.add_mistakes(input.text, input.errorOptions)
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
    except Exception as e:
        logger.error(f"Error in correction processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# API 端点：缩写扩展
@app.post("/api/abbr")
async def expand_abbreviations(input: AbbrInput):
    try:
        if input.method == "simple_ollama":  # 简单扩展
            output = abbr_service.simple_ollama_expansion(input.text, input.llmOptions)
            return {"input": input.text, "output": output}
        elif input.method == "query_db_llm_rerank":  # 数据库查询+重排序
            return abbr_service.query_db_llm_rerank(
                input.text, 
                input.context, 
                input.llmOptions,
                input.embeddingOptions
            )
        elif input.method == "llm_rank_query_db":  # LLM扩展+数据库标准化
            return abbr_service.llm_rank_query_db(
                input.text, 
                input.context, 
                input.llmOptions,
                input.embeddingOptions
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
    except Exception as e:
        logger.error(f"Error in abbreviation expansion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# API 端点：金融文本生成
@app.post("/api/gen")
async def generate_financial_content(input: GenInput):
    try:
        if input.method == "generate_financial_report":  # 生成金融报告
            return gen_service.generate_financial_report(
                input.company_info,
                input.financial_data,
                input.analysis_type,
                input.recommendations,
                input.llmOptions
            )
        elif input.method == "generate_investment_analysis":  # 生成投资分析
            return gen_service.generate_investment_analysis(
                input.market_data,
                input.llmOptions
            )
        elif input.method == "generate_risk_assessment":  # 生成风险评估
            return gen_service.generate_risk_assessment(
                input.portfolio_info,
                input.market_conditions,
                input.llmOptions
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
    except Exception as e:
        logger.error(f"Error in financial content generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 配置信息API
@app.get("/api/config")
async def get_config():
    """获取当前系统配置信息"""
    try:
        # 获取当前配置
        config_info = {
            "embedding": {
                "provider": DEFAULT_EMBEDDING_PROVIDER,
                "model": DEFAULT_EMBEDDING_MODEL,
                "dbName": get_db_name_from_model(DEFAULT_EMBEDDING_MODEL),
                "collectionName": "financial_terms"
            },
            "model_info": get_model_info(DEFAULT_EMBEDDING_MODEL),
            "available_models": {
                "lightweight": {
                    "model": "sentence-transformers/all-MiniLM-L6-v2",
                    "size": "90MB",
                    "dbName": "financial_terms_minilm",
                    "description": "轻量快速，适合测试"
                },
                "balanced": {
                    "model": "sentence-transformers/all-mpnet-base-v2",
                    "size": "420MB",
                    "dbName": "financial_terms_mpnet",
                    "description": "平衡性能，推荐使用"
                },
                "complete": {
                    "model": "BAAI/bge-m3",
                    "size": "2.27GB",
                    "dbName": "financial_terms_bge_m3",
                    "description": "最佳效果，完整功能"
                }
            }
        }

        return {
            "status": "success",
            "data": config_info
        }

    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取配置失败: {str(e)}")

def get_db_name_from_model(model_name: str) -> str:
    """根据模型名称获取对应的数据库名称"""
    if "all-MiniLM-L6-v2" in model_name:
        return "financial_terms_minilm"
    elif "all-mpnet-base-v2" in model_name:
        return "financial_terms_mpnet"
    elif "bge-m3" in model_name:
        return "financial_terms_bge_m3"
    else:
        return "financial_terms_custom"

def get_model_info(model_name: str) -> dict:
    """获取模型信息"""
    model_info_map = {
        "sentence-transformers/all-MiniLM-L6-v2": {
            "type": "lightweight",
            "size": "90MB",
            "description": "轻量快速模型"
        },
        "sentence-transformers/all-mpnet-base-v2": {
            "type": "balanced",
            "size": "420MB",
            "description": "平衡性能模型"
        },
        "BAAI/bge-m3": {
            "type": "complete",
            "size": "2.27GB",
            "description": "完整功能模型"
        }
    }
    return model_info_map.get(model_name, {
        "type": "custom",
        "size": "unknown",
        "description": "自定义模型"
    })

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    print("🚀 启动金融术语标准化系统...")
    print("📖 API文档地址: http://localhost:8000/docs")
    print("🔧 API接口地址: http://localhost:8000")
    print(f"🤖 当前嵌入模型: {DEFAULT_EMBEDDING_MODEL}")
    print(f"💾 数据库名称: {get_db_name_from_model(DEFAULT_EMBEDDING_MODEL)}")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
