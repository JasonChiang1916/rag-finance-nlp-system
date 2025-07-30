# 金融术语标准化系统

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

**🏦 智能金融文档处理 • 💰 术语标准化 • 🤖 AI驱动**

[快速开始](#快速开始-) • [功能特性](#主要功能) • [API文档](#api接口) • [部署指南](#环境部署)

</div>

---

## 🚀 快速开始

### ⚡ 一键部署
```bash
# 1. 克隆项目
git clone <repository-url>
cd rag-project02-finance-nlp-box

# 2. 一键启动 (macOS)
python3 start_macos.py

# 📁 注意: 项目已包含必要的本地模型文件
# 无需额外下载即可直接使用英文NER功能
```

### 🎯 立即体验
- **前端界面**: http://localhost:3000
- **API文档**: http://localhost:8000/docs
- **英文示例**: "JPMorgan Chase reports ROE increased to 15%, investment banking revenue grew 20%"
- **中文示例**: "摩根大通报告显示ROE提升至15%，投资银行业务收入增长20%" (需要中文模型)

### ⚠️ 重要提示
**当前系统使用英文NER模型 (`dbmdz/bert-large-cased-finetuned-conll03-english`)，建议使用英文文本进行测试以获得最佳效果。如需处理中文文本，请参考[模型下载与配置](#模型下载与配置)部分。**

---

## 📋 项目概述

本项目已从医疗术语标准化系统成功改造为**金融术语标准化系统**，提供全面的金融文档处理和术语标准化功能。

### 📊 项目统计
- 🏦 **15,886** 条金融标准术语
- 🤖 **5** 大核心功能模块
- 🎯 **90MB** 轻量模型选项
- ⚡ **<30秒** 快速启动
- 🍎 **100%** macOS 兼容

## 📋 目录

- [📋 项目概述](#项目概述)
- [🚨 当前项目状态](#当前项目状态)
- [🎯 主要功能](#主要功能)
- [🏗️ 技术架构](#技术架构)
- [📁 项目结构](#项目结构)
- [🔧 环境部署](#环境部署)
- [📖 使用方法](#使用方法)
- [🤖 模型下载与配置](#模型下载与配置)
- [🔌 API接口](#api接口)
- [🛠️ 故障排除](#故障排除)
- [📈 性能优化](#性能优化)
- [🚀 开发指南](#开发指南)
- [💬 技术支持](#技术支持)
- [📝 更新日志](#更新日志)
- [📄 许可证](#许可证)

## 🚨 当前项目状态

### 📊 已安装依赖版本
- **FastAPI**: 0.104.1
- **PyTorch**: 2.2.2 (CPU版本)
- **Transformers**: 4.46.3
- **Sentence Transformers**: 3.2.1
- **LangChain**: 0.2.17
- **Milvus**: 2.5.14
- **Python**: 3.8+

### 🌐 语言支持状态
- ✅ **英文**: 完全支持，使用 `dbmdz/bert-large-cased-finetuned-conll03-english` 模型
- ⚠️ **中文**: 需要额外配置中文NER模型 (详见[模型下载与配置](#模型下载与配置))
- 🔧 **推荐测试方式**:
  - 英文文本: "Goldman Sachs investment banking revenue increased 15%"
  - 中文文本: 需要先配置中文模型

### 🎯 最佳实践
1. **首次使用**: 建议使用英文金融文本进行测试
2. **生产环境**: 根据需要配置对应语言的NER模型
3. **性能优化**: 使用轻量模型 (all-MiniLM-L6-v2) 进行快速测试

## 🎯 主要功能

### 1. 金融命名实体识别 (NER)
- 识别金融文档中的关键实体
- 支持公司名称、金融产品、交易类型等实体识别
- **当前使用英文NER模型**: `dbmdz/bert-large-cased-finetuned-conll03-english`
- **推荐使用英文文本测试**: 如 "JPMorgan Chase", "Goldman Sachs", "investment banking"
- **中文支持**: 需要配置中文NER模型 (详见配置说明)

### 2. 金融术语标准化
- 基于万条金融标准术语数据库
- 使用向量相似度搜索进行术语标准化
- 支持多种嵌入模型（BGE-M3等）

### 3. 金融缩写展开
- 自动识别和展开金融文档中的缩写
- 支持上下文相关的缩写解释
- 集成LLM进行智能缩写扩展

### 4. 金融文档纠错
- 自动检测和纠正金融文档中的错误
- 支持拼写检查和语法纠正
- 保持金融术语的专业性

### 5. 金融内容生成
- 生成金融报告
- 投资分析报告生成
- 风险评估报告生成

## 🏗️ 技术架构

### 后端 (FastAPI)
- **API接口**: RESTful API设计
- **数据库**: Milvus向量数据库存储金融术语
- **模型**:
  - 嵌入模型: sentence-transformers/all-MiniLM-L6-v2 (默认轻量模型)
  - NER模型: dbmdz/bert-large-cased-finetuned-conll03-english (英文模型)
  - LLM: 支持Ollama和OpenAI模型
- **语言支持**:
  - 主要支持英文文本处理
  - 中文支持需要额外配置中文模型

### 前端 (React)
- **界面**: 现代化响应式设计
- **组件**: 模块化组件设计
- **主题**: 金融主题UI设计

### 数据
- **金融术语库**: 万条金融标准术语.csv (15,886条术语)
- **向量数据库**: financial_terms_minilm.db (默认轻量模型)
- **集合名称**: financial_terms
- **支持的数据库**:
  - financial_terms_minilm.db (90MB, 轻量快速)
  - financial_terms_mpnet.db (420MB, 平衡性能)
  - financial_terms_bge_m3.db (2.27GB, 最佳效果)


## 📁 项目结构

```
金融术语标准化系统/
├── backend/
│   ├── main.py                 # 主API服务器
│   ├── services/
│   │   ├── std_service.py      # 金融术语标准化服务
│   │   ├── ner_service.py      # 金融实体识别服务
│   │   ├── gen_service.py      # 金融内容生成服务
│   │   ├── abbr_service.py     # 金融缩写展开服务
│   │   └── corr_service.py     # 金融文档纠错服务
│   ├── models/                 # 本地模型目录
│   │   ├── all-MiniLM-L6-v2/   # ✅ 轻量嵌入模型 (90MB)
│   │   ├── bert-base-NER/      # ✅ 备用NER模型
│   │   ├── bert-large-cased-finetuned-conll03-english/  # ✅ 当前英文NER模型
│   │   ├── bge-m3/             # ✅ 高性能嵌入模型 (2.27GB)
│   │   └── Financial-NER/      # ❌ 金融专用NER模型 (需下载)
│   ├── tools/
│   │   ├── create_financial_terms_db.py  # 金融术语数据库创建
│   │   └── create_milvus_db.py           # 更新的数据库创建脚本
│   ├── utils/
│   │   ├── embedding_factory.py         # 嵌入模型工厂
│   │   └── embedding_config.py          # 嵌入配置
│   ├── config/
│   │   └── macos_config.py              # macOS专用配置
│   └── db/
│       ├── financial_terms_minilm.db    # 轻量模型数据库 (默认)
│       ├── financial_terms_mpnet.db     # 平衡模型数据库
│       └── financial_terms_bge_m3.db    # 高性能模型数据库
├── frontend/
│   ├── src/
│   │   ├── App.js              # 主应用组件
│   │   ├── components/
│   │   │   ├── Sidebar.js      # 导航侧边栏
│   │   │   └── shared/         # 共享组件
│   │   ├── hooks/
│   │   │   └── useSystemConfig.js      # 系统配置Hook
│   │   └── pages/
│   │       ├── NERPage.js      # 金融实体识别页面
│   │       ├── StdPage.js      # 金融术语标准化页面
│   │       ├── AbbrPage.js     # 金融缩写展开页面
│   │       ├── CorrPage.js     # 金融文档纠错页面
│   │       └── GenPage.js      # 金融内容生成页面
│   └── package.json
├── dev-env/                    # Python虚拟环境
├── 万条金融标准术语.csv           # 金融术语数据源 (15,886条)
├── requirements_mac(no GPU).txt  # macOS依赖文件
├── install_dependencies.py    # 依赖安装脚本
├── quick_setup.py              # 快速设置脚本
├── start_macos.py              # macOS启动脚本
├── test_financial_system.py    # 系统测试脚本
└── README.md                   # 本文档
```

## 🔧 环境部署

### 系统要求
- **操作系统**: macOS 10.15+ (支持 Intel 和 Apple Silicon)
- **Python**: 3.8+
- **Node.js**: 16+ (前端)
- **内存**: 最低 4GB，推荐 8GB+
- **存储**: 至少 5GB 可用空间

### 安装步骤

#### 1. 准备环境
**创建虚拟环境 (推荐)**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows
```

**安装 Python 依赖**
```bash
# 方式1: 使用安装脚本 (推荐)
python3 install_dependencies.py

# 方式2: 直接安装
pip install -r "requirements_mac(no GPU).txt"

# 方式3: 分步安装核心依赖 (使用具体版本)
pip install fastapi==0.104.1 uvicorn==0.24.0 torch==2.2.2 transformers==4.46.3 sentence-transformers==3.2.1 pymilvus==2.5.14 pandas==2.0.3
```

#### 2. 数据库初始化

**创建金融术语向量数据库**
```bash
cd backend

# 使用轻量模型 (90MB, 推荐)
python3 tools/create_financial_terms_db.py

# 或使用快速设置选择模型
cd ..
python3 quick_setup.py
```

**验证数据库创建**
```bash
# 检查数据库文件
ls -la backend/db/financial_terms_*.db

# 运行测试
python3 test_financial_system.py
```

#### 3. 启动服务

**启动后端服务**
```bash
cd backend

# 方式1: 使用 uvicorn (推荐)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 方式2: 直接运行
python3 main.py

# 验证后端启动
curl http://localhost:8000/docs
```

**启动前端服务**
```bash
# 新开终端窗口
cd frontend

# 安装依赖 (首次运行)
npm install

# 启动开发服务器
npm start

# 验证前端启动
open http://localhost:3000
```

## 📖 使用方法

#### 1. 访问系统
- **前端界面**: http://localhost:3000
- **API 文档**: http://localhost:8000/docs
- **API 根路径**: http://localhost:8000

#### 2. 功能使用

**金融实体识别**
1. 访问 "金融命名实体识别" 页面
2. 输入金融文本:
   - **英文示例** (推荐): "JPMorgan Chase reports ROE increased to 15%"
   - **中文示例**: "摩根大通报告显示ROE提升至15%" (需要中文模型)
3. 选择术语类型和处理选项
4. 点击 "识别实体" 查看结果

**⚠️ 注意**: 当前使用英文NER模型，建议使用英文文本测试以获得最佳识别效果。

**金融术语标准化**
1. 访问 "金融术语标准化" 页面
2. 输入需要标准化的术语
3. 配置嵌入模型选项
4. 点击 "标准化术语" 获取标准化结果

**其他功能**
- **缩写展开**: 自动展开金融文档中的缩写
- **文档纠错**: 检测和纠正金融文档错误
- **内容生成**: 生成金融报告和分析

#### 3. 配置选项

**模型配置**
```python
# 在 backend/config/model_config.py 中配置
EMBEDDING_MODELS = {
    "lightweight": "sentence-transformers/all-MiniLM-L6-v2",  # 90MB
    "balanced": "sentence-transformers/all-mpnet-base-v2",    # 420MB
    "best": "BAAI/bge-m3"                                     # 2.27GB
}
```

**数据库配置**
```python
# 默认配置 (轻量模型)
{
    "provider": "huggingface",
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "dbName": "financial_terms_minilm",
    "collectionName": "financial_terms"
}
```

## 🤖 模型下载与配置

### ⚠️ 重要说明
**由于模型文件较大，GitHub仓库中不包含模型文件。首次使用需要下载模型。**

### 📁 本地模型目录结构
```
backend/models/
├── all-MiniLM-L6-v2/                    # 轻量嵌入模型 (90MB)
├── bert-base-NER/                       # 备用NER模型 (420MB)
├── bert-large-cased-finetuned-conll03-english/  # 英文NER模型 (1.3GB)
├── bge-m3/                              # 高性能嵌入模型 (2.27GB)
└── Financial-NER/                       # 金融专用NER模型 (可选)
```

### 🔄 模型加载优先级
1. **Financial-NER/** - 金融专用模型 (如果存在，优先使用)
2. **bert-large-cased-finetuned-conll03-english/** - 本地英文模型
3. **在线下载** - 自动从HuggingFace下载默认模型

### 📥 模型下载方式

#### 方式1: 使用自动下载脚本 (推荐)
```bash
# 运行模型下载脚本
python3 download_models.py

# 根据提示选择要下载的模型:
# 1. 基础模型 (必需) - 约2GB
# 2. 中文模型 (可选) - 约400MB
# 3. 高性能模型 (可选) - 约3GB
# 4. 全部模型 - 约6GB
```

#### 方式2: 手动下载

##### 1. 安装 Git LFS
```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt install git-lfs

# 初始化 Git LFS
git lfs install
```

##### 2. 下载基础模型 (必需)
```bash
cd backend/models

# 下载英文NER模型 (必需)
git lfs clone https://huggingface.co/dbmdz/bert-large-cased-finetuned-conll03-english

# 下载轻量嵌入模型 (必需)
git lfs clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

# 下载备用NER模型 (推荐)
git lfs clone https://huggingface.co/dslim/bert-base-NER
```

### � 可选模型下载

#### 中文支持模型
```bash
cd backend/models

# 方法1: 下载中文NER模型
git lfs clone https://huggingface.co/hfl/chinese-bert-wwm-ext
mv chinese-bert-wwm-ext Financial-NER

# 方法2: 下载中文金融专用模型
git lfs clone https://huggingface.co/ckiplab/bert-base-chinese-ner
mv bert-base-chinese-ner Financial-NER
```

#### 高性能嵌入模型
```bash
cd backend/models

# 平衡性能模型 (420MB)
git lfs clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2

# 最佳性能模型 (2.27GB)
git lfs clone https://huggingface.co/BAAI/bge-m3
```

### 🔧 模型配置

#### 使用中文模型
```python
# 在 backend/services/ner_service.py 第38行修改:
self.pipe = pipeline("token-classification",
                   model="hfl/chinese-bert-wwm-ext",  # 或其他中文模型
                   aggregation_strategy='simple',
                   device=0 if torch.cuda.is_available() else -1)
```

#### 使用多语言模型
```python
# 支持中英文的多语言模型
model_name = "bert-base-multilingual-cased"
# 或
model_name = "xlm-roberta-base"
```

### 🚀 快速开始 (无需下载)
如果不想下载模型，系统会自动从HuggingFace在线下载必需的模型：
```bash
# 直接启动，系统会自动下载模型
cd backend
python3 main.py
```

### 🧪 测试示例

#### 英文测试
```json
{
  "text": "JPMorgan Chase reports ROE increased to 15%",
  "options": {"combineFinancialEntities": true},
  "termTypes": {"allFinancialTerms": true}
}
```

#### 中文测试 (需要中文模型)
```json
{
  "text": "中国银行发布季度报告，净利润同比增长8.5%",
  "options": {"combineFinancialEntities": true},
  "termTypes": {"allFinancialTerms": true}
}
```

## 🔌 API接口

### 金融术语标准化
```
POST /api/std
{
  "text": "投资银行业务收入增长20%",
  "options": {"allFinancialTerms": true},
  "embeddingOptions": {
    "provider": "huggingface",
    "model": "BAAI/bge-m3",
    "dbName": "financial_terms_bge_m3",
    "collectionName": "financial_terms"
  }
}
```

### 金融实体识别
```
POST /api/ner
{
  "text": "JPMorgan Chase reports ROE increased to 15%",
  "options": {"combineFinancialEntities": true},
  "termTypes": {"allFinancialTerms": true}
}
```

**中文示例** (需要中文模型):
```
POST /api/ner
{
  "text": "摩根大通报告显示ROE提升至15%",
  "options": {"combineFinancialEntities": true},
  "termTypes": {"allFinancialTerms": true}
}
```

### 金融内容生成
```
POST /api/gen
{
  "method": "generate_financial_report",
  "company_info": {...},
  "financial_data": [...],
  "analysis_type": "quarterly_analysis",
  "recommendations": "..."
}
```

## 🛠️ 故障排除

### 常见问题

#### 1. 依赖安装问题
```bash
# 问题: pip 安装失败
# 解决: 升级 pip 和使用国内镜像
pip install --upgrade pip
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r "requirements_mac(no GPU).txt"

# 问题: PyTorch 安装失败
# 解决: 手动安装 CPU 版本 (使用项目版本)
pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu
```

#### 2. 模型下载问题
```bash
# 问题: 模型下载慢或失败
# 解决1: 设置 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com

# 解决2: 检查网络连接
ping huggingface.co

# 解决3: 参考模型下载章节
# 详见 "🤖 模型下载与配置" 章节
```

#### 3. 数据库创建问题
```bash
# 问题: 数据库创建失败
# 解决: 检查文件和权限
ls -la "万条金融标准术语.csv"
mkdir -p backend/db
python3 backend/tools/create_financial_terms_db.py
```

#### 4. 端口占用问题
```bash
# 问题: 端口 8000 或 3000 被占用
# 解决: 查找并终止占用进程
lsof -ti:8000 | xargs kill -9  # 终止 8000 端口进程
lsof -ti:3000 | xargs kill -9  # 终止 3000 端口进程

# 或使用其他端口
uvicorn main:app --port 8001  # 后端使用 8001
npm start -- --port 3001     # 前端使用 3001
```

#### 5. 内存不足问题
```bash
# 问题: 内存不足导致模型加载失败
# 解决: 使用轻量模型和调整批处理大小
# 在 backend/config/macos_config.py 中调整:
config = {
    "batch_size": 16,  # 减小批处理大小
    "max_length": 256  # 减小序列长度
}
```

## 📈 性能优化

### macOS 优化
```bash
# Apple Silicon (M1/M2) 优化
export PYTORCH_ENABLE_MPS_FALLBACK=1

# 设置线程数
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
```

### 模型选择建议
| 使用场景 | 推荐模型 | 内存占用 | 启动时间 |
|---------|---------|---------|---------|
| 开发测试 | all-MiniLM-L6-v2 | ~500MB | ~30秒 |
| 生产环境 | all-mpnet-base-v2 | ~1.5GB | ~60秒 |
| 高精度需求 | BAAI/bge-m3 | ~3GB | ~120秒 |

### 数据库优化
```python
# 调整搜索参数以提高性能
search_params = {
    "limit": 5,        # 减少返回结果数量
    "nprobe": 10,      # 调整搜索精度
}
```

## 🚀 开发指南

### 添加新的金融术语
1. 编辑 `万条金融标准术语.csv` 文件
2. 重新运行数据库创建脚本
3. 重启后端服务

### 自定义 NER 模型

#### 📁 模型目录结构
```
backend/models/
├── Financial-NER/          # 金融专用NER模型 (最高优先级)
├── bert-large-cased-finetuned-conll03-english/  # 英文通用NER (当前默认)
├── bert-base-NER/          # 备用NER模型
└── [其他模型]/             # 用户自定义模型
```

#### 🔧 自定义模型配置
详细的模型下载和配置方法请参考 **[🤖 模型下载与配置](#模型下载与配置)** 章节。

### API 扩展
1. 在 `backend/main.py` 中添加新的端点
2. 在对应的服务文件中实现业务逻辑
3. 更新前端页面调用新 API

## 💬 技术支持

### 日志查看
```bash
# 后端日志
tail -f backend/logs/app.log

# 前端日志
# 查看浏览器控制台
```

### 系统监控
```bash
# 检查系统资源
top -pid $(pgrep -f "python.*main.py")
top -pid $(pgrep -f "node.*start")

# 检查端口状态
netstat -an | grep :8000
netstat -an | grep :3000
```

### 获取帮助
1. 查看 API 文档: http://localhost:8000/docs
2. 运行测试脚本: `python3 test_financial_system.py`
3. 检查系统状态: `python3 start_macos.py`

## 📝 更新日志

### v1.1.0 (2024-07-30) - 系统修复与优化
🔧 **重要修复**: 解决API连接问题，优化依赖管理

#### 🐛 问题修复
- 🔗 **API连接修复**: 修复前端API地址错误 (172.20.116.213 → localhost)
- 🎯 **NER逻辑优化**: 将医疗术语过滤逻辑改为金融术语逻辑
- 📦 **依赖版本锁定**: 更新为具体版本号，确保环境一致性
- 🌐 **语言支持说明**: 明确标注当前使用英文NER模型

#### 📋 依赖更新
- FastAPI: 0.104.1
- PyTorch: 2.2.2
- Transformers: 4.46.3
- Sentence Transformers: 3.2.1
- LangChain: 0.2.17
- Milvus: 2.5.14

#### 📚 文档完善
- 📖 **语言支持说明**: 详细说明英文/中文模型配置
- 🧪 **测试示例更新**: 提供英文和中文测试用例
- 🔧 **配置指南**: 新增中文模型配置步骤
- 📊 **依赖版本表**: 明确列出所有依赖的具体版本

### 参与贡献

我们欢迎社区贡献！以下是参与方式：

#### 🐛 报告问题
1. 在 GitHub Issues 中创建新问题
2. 详细描述问题和复现步骤
3. 提供系统环境信息
4. 附上相关日志和截图

#### 💡 功能建议
1. 在 Issues 中标记为 "enhancement"
2. 描述功能需求和使用场景
3. 提供设计思路或参考资料

#### 🔧 代码贡献
1. Fork 项目到个人仓库
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -m 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 创建 Pull Request

#### 📝 文档贡献
- 改进 README 和文档
- 添加使用示例和教程
- 翻译文档到其他语言
- 修正错别字和格式问题

### 代码规范
- **Python**: 遵循 PEP 8 规范
- **JavaScript**: 使用 ESLint 和 Prettier
- **提交信息**: 使用语义化提交格式
- **文档**: 保持代码注释和文档同步

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

感谢以下开源项目和贡献者：
- 🤗 **Hugging Face**: Transformers 和模型生态
- 🔍 **Milvus**: 向量数据库支持
- ⚡ **FastAPI**: 现代 Web 框架
- 🔗 **LangChain**: LLM 应用框架
- ⚛️ **React**: 前端框架
- 🍎 **Apple**: macOS 平台支持

## 联系方式

- 💬 **讨论**: GitHub Discussions
- 🐛 **问题**: GitHub Issues
- 📚 **文档**: 项目 Wiki

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**

[🚀 快速开始](#快速开始) • [📖 文档](#环境部署) • [🐛 报告问题](../../issues) • [💡 功能建议](../../issues)

</div>
