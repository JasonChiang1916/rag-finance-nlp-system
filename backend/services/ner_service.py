from transformers import pipeline
import torch
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NERService:
    """
    金融术语命名实体识别服务
    使用适合金融领域的NER模型进行金融文本的实体识别
    """
    def __init__(self):
        # 初始化 NER 模型，使用 GPU 如果可用
        # 首先尝试使用金融领域的模型，如果不存在则使用通用模型
        try:
            # 尝试使用金融领域的模型
            import os
            local_model_path = "models/Financial-NER"
            if os.path.exists(local_model_path):
                logger.info(f"使用本地金融模型: {local_model_path}")
                self.pipe = pipeline("token-classification",
                                   model=local_model_path,
                                   aggregation_strategy='simple',
                                   device=0 if torch.cuda.is_available() else -1)
            else:
                # 尝试使用本地下载的通用NER模型
                local_bert_large = "../models/bert-large-cased-finetuned-conll03-english"
                if os.path.exists(local_bert_large):
                    logger.info(f"使用本地模型: {local_bert_large}")
                    self.pipe = pipeline("token-classification",
                                       model=local_bert_large,
                                       aggregation_strategy='simple',
                                       device=0 if torch.cuda.is_available() else -1)
                else:
                    # 使用通用的多语言NER模型，可以识别组织、人名、地点等
                    logger.info("使用通用模型: dbmdz/bert-large-cased-finetuned-conll03-english")
                    self.pipe = pipeline("token-classification",
                                       model="dbmdz/bert-large-cased-finetuned-conll03-english",
                                       aggregation_strategy='simple',
                                       device=0 if torch.cuda.is_available() else -1)
        except Exception as e:
            # 如果主模型失败，使用备用的通用 NER 模型
            logger.warning(f"主模型加载失败: {e}")
            try:
                # 尝试使用本地下载的备用模型
                local_bert_base = "../models/bert-base-NER"
                if os.path.exists(local_bert_base):
                    logger.info(f"使用本地备用模型: {local_bert_base}")
                    self.pipe = pipeline("token-classification",
                                       model=local_bert_base,
                                       aggregation_strategy='simple',
                                       device=0 if torch.cuda.is_available() else -1)
                else:
                    logger.info("使用备用模型: dslim/bert-base-NER")
                    self.pipe = pipeline("token-classification",
                                       model="dslim/bert-base-NER",
                                       aggregation_strategy='simple',
                                       device=0 if torch.cuda.is_available() else -1)
            except Exception as e2:
                logger.error(f"所有模型加载失败: {e2}")
                raise e2
  
    def process(self, text, options, term_types):
        """
        处理输入文本，识别金融术语实体

        Args:
            text: 输入文本
            options: 处理选项，如是否合并相关实体
            term_types: 需要识别的术语类型

        Returns:
            包含识别出的实体和原始文本的字典
        """
        # 使用模型进行实体识别
        result = self.pipe(text)
        
        # 确保结果是实体列表
        if isinstance(result, dict):
            result = result.get('entities', [])
        
        # 合并相关实体（如生物结构和症状）
        combined_result = self._combine_entities(result, text, options)
        
        # 移除重叠实体
        non_overlapping_result = self._remove_overlapping_entities(combined_result)
        
        # 根据术语类型过滤实体
        filtered_result = self._filter_entities(non_overlapping_result, term_types)
        
        return {
            "text": text,
            "entities": filtered_result
        }

    def _combine_entities(self, result, text, options):
        """
        合并相关的实体，如金融机构和金融产品
        """
        combined_result = []
        i = 0
        while i < len(result):
            entity = result[i]
            entity['score'] = float(entity['score'])

            if options.get('combineFinancialEntities', False) and entity['entity_group'] in ['ORG', 'MONEY', 'PERCENT']:
                # 检查并合并金融实体
                combined_entity = self._try_combine_with_financial_entity(result, i, text)
                if combined_entity:
                    combined_result.append(combined_entity)
                    i += 1
                    continue
            combined_result.append(entity)
            i += 1
        return combined_result

    def _try_combine_with_financial_entity(self, result, i, text):
        """
        尝试将当前实体与金融实体合并
        """
        # 检查前一个实体
        if i > 0 and result[i-1]['entity_group'] in ['ORG', 'ORGANIZATION']:
            return self._create_combined_entity(result[i-1], result[i], text)
        # 检查后一个实体
        elif i < len(result) - 1 and result[i+1]['entity_group'] in ['ORG', 'ORGANIZATION']:
            return self._create_combined_entity(result[i], result[i+1], text)
        return None

    def _create_combined_entity(self, entity1, entity2, text):
        """
        创建合并后的实体
        """
        start = min(entity1['start'], entity2['start'])
        end = max(entity1['end'], entity2['end'])
        word = text[start:end]
        return {
            'entity_group': 'COMBINED_FINANCIAL',
            'word': word,
            'start': start,
            'end': end,
            'score': (entity1['score'] + entity2['score']) / 2,
            'original_entities': [entity1, entity2]
        }

    def _remove_overlapping_entities(self, entities):
        """
        移除重叠的实体，保留得分最高的实体
        """
        # 按开始位置、结束位置（降序）和得分（降序）排序
        sorted_entities = sorted(entities, key=lambda x: (x['start'], -x['end'], -x['score']))
        non_overlapping = []
        last_end = -1

        i = 0
        while i < len(sorted_entities):
            current = sorted_entities[i]
            
            # 如果当前实体与之前的实体不重叠，直接添加
            if current['start'] >= last_end:
                non_overlapping.append(current)
                last_end = current['end']
                i += 1
            else:
                # 处理重叠实体
                same_span = [current]
                j = i + 1
                while j < len(sorted_entities) and sorted_entities[j]['start'] == current['start'] and sorted_entities[j]['end'] == current['end']:
                    same_span.append(sorted_entities[j])
                    j += 1
                
                # 选择得分最高的实体
                best_entity = max(same_span, key=lambda x: x['score'])
                if best_entity['end'] > last_end:
                    non_overlapping.append(best_entity)
                    last_end = best_entity['end']
                
                i = j

        return non_overlapping

    def _filter_entities(self, entities, term_types):
        """
        根据术语类型过滤实体
        """
        filtered_result = []
        for entity in entities:
            if term_types.get('allFinancialTerms', False):
                filtered_result.append(entity)
            elif (term_types.get('company', False) and entity['entity_group'] in ['ORG', 'ORGANIZATION']) or \
                 (term_types.get('product', False) and entity['entity_group'] in ['PRODUCT', 'MISC']) or \
                 (term_types.get('transaction', False) and entity['entity_group'] in ['MONEY', 'PERCENT']):
                filtered_result.append(entity)
        return filtered_result




