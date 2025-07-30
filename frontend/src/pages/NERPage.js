import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { TextInput } from '../components/shared/ModelOptions';

const color_map = {
  'DATE': "#FF9800", // 日期
  'AMOUNT': "#E91E63", // 金额
  'COMPANY': "#FF0000", // 公司名称
  'TIME': "#673AB7", // 时间
  'PERCENTAGE': "#3F51B5", // 百分比
  'FINANCIAL_EVENT': "#2196F3", // 金融事件
  'CURRENCY': "#03A9F4", // 货币
  'FREQUENCY': "#00BCD4", // 频率
  'FINANCIAL_INSTRUMENT': "#009688", // 金融工具
  'MARKET': "#4CAF50", // 市场
  'RATIO': "#8BC34A", // 比率
  'SECTOR': "#CDDC39", // 行业板块
  'REFERENCE': "#FFEB3B", // 引用
  'PRODUCT': "#FFC107", // 金融产品
  'VOLUME': "#FF9800", // 交易量
  'RISK_LEVEL': "#FF5722", // 风险等级
  'FINANCIAL_METRIC': "#795548", // 金融指标
  'INVESTMENT_TYPE': "#00FF00", // 投资类型
  'DURATION': "#607D8B", // 期限
  'PRICE': "#D32F2F", // 价格
  'TRANSACTION': "#C2185B", // 交易
  'REGULATION': "#7B1FA2", // 监管
  'STRATEGY': "#512DA8", // 策略
  'ENTITY': "#303F9F", // 实体
  'HISTORY': "#1976D2", // 历史
  'PERFORMANCE': "#0288D1", // 表现
  'QUANTITATIVE': "#0097A7", // 定量概念
  'RATING': "#00796B", // 评级
  'DESCRIPTION': "#388E3C", // 描述
  'ANALYSIS': "#689F38", // 分析
  'LOCATION': "#AFB42B", // 地点
  'OUTCOME': "#FBC02D", // 结果
  'PERSON': "#FFA000", // 人员
  'STATUS': "#F57C00", // 状态
  'QUALITATIVE': "#E64A19", // 定性概念
  'TERM': "#5D4037", // 术语
  'BACKGROUND': "#616161", // 背景
  'OTHER_ENTITY': "#455A64", // 其他实体
  'OTHER_EVENT': "#C62828", // 其他事件
  'POSITION': "#AD1457", // 职位
  'ROLE': "#880E4F", // 角色
  'COMBINED_FINANCIAL': "#FF4500",  // 合并金融实体
};

const NERPage = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const [coloredResult, setColoredResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [termTypes, setTermTypes] = useState({
    company: false,
    product: false,
    transaction: false,
    allFinancialTerms: false,
  });
  const [options, setOptions] = useState({
    combineFinancialEntities: false,
  });

  const handleTermTypeChange = (e) => {
    const { name, checked } = e.target;
    if (name === 'allFinancialTerms') {
      setTermTypes({
        company: false,
        product: false,
        transaction: false,
        allFinancialTerms: checked,
      });
    } else {
      setTermTypes({ ...termTypes, [name]: checked });
    }
  };

  const handleOptionChange = (e) => {
    setOptions({ ...options, [e.target.name]: e.target.checked });
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/ner', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input, options, termTypes }),
      });
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
      setColoredResult(generateColoredResult(data.text, data.entities));
    } catch (error) {
      console.error('Error:', error);
      setResult('An error occurred while processing the request.');
      setColoredResult('');
    }
    setIsLoading(false);
  };

  const generateColoredResult = (text, entities) => {
    let result = text;
    entities.sort((a, b) => b.start - a.start);
    
    for (const entity of entities) {
      const color = color_map[entity.entity_group] || '#000000';
      let highlightedEntity;
      
      if (entity.entity_group === 'COMBINED_FINANCIAL' && entity.original_entities) {
        const [financialEntity1, financialEntity2] = entity.original_entities;
        highlightedEntity = `<span style="background-color: ${color}; padding: 2px; border-radius: 3px;">
          <span style="border-bottom: 2px solid ${color_map[financialEntity1.entity_group]};">${financialEntity1.word}</span>
          <span style="border-bottom: 2px solid ${color_map[financialEntity2.entity_group]};">${financialEntity2.word}</span>
          <sub>${financialEntity1.entity_group}+${financialEntity2.entity_group}</sub>
        </span>`;
      } else {
        highlightedEntity = `<span style="background-color: ${color}; padding: 2px; border-radius: 3px;">
          ${entity.word}<sub>${entity.entity_group}</sub>
        </span>`;
      }
      
      result = result.slice(0, entity.start) + highlightedEntity + result.slice(entity.end);
    }
    
    return result;
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">金融命名实体识别 💰</h1>
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">输入金融文本</h2>
        <TextInput
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={4}
          placeholder="请输入需要进行命名实体识别的金融文本..."
        />
        
        <h3 className="text-lg font-semibold mb-2">金融术语类型</h3>
        <div className="mb-4">
          <label>
            <input
              type="checkbox"
              name="company"
              checked={termTypes.company}
              onChange={handleTermTypeChange}
            />
            公司
          </label>
          <label className="ml-4">
            <input
              type="checkbox"
              name="product"
              checked={termTypes.product}
              onChange={handleTermTypeChange}
            />
            金融产品
          </label>
          <label className="ml-4">
            <input
              type="checkbox"
              name="transaction"
              checked={termTypes.transaction}
              onChange={handleTermTypeChange}
            />
            交易
          </label>
          <label className="ml-4">
            <input
              type="checkbox"
              name="allFinancialTerms"
              checked={termTypes.allFinancialTerms}
              onChange={handleTermTypeChange}
            />
            所有金融术语
          </label>
        </div>

        <h3 className="text-lg font-semibold mb-2">选项</h3>
        <div className="mb-4">
          <label>
            <input
              type="checkbox"
              name="combineFinancialEntities"
              checked={options.combineFinancialEntities}
              onChange={handleOptionChange}
            />
            合并相关金融实体
          </label>
        </div>

        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className={`bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isLoading ? '处理中...' : '识别实体'}
        </button>
      </div>
      {coloredResult && (
        <div className="bg-white shadow-md rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">识别结果</h2>
          <div 
            dangerouslySetInnerHTML={{ __html: coloredResult }} 
            style={{
              lineHeight: '2',
              wordBreak: 'break-word'
            }}
          />
        </div>
      )}
      {result && (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
          <p className="font-bold">JSON 结果：</p>
          <pre>{result}</pre>
        </div>
      )}
      {/* <div className="flex items-center text-yellow-700 bg-yellow-100 p-4 rounded-md">
        <AlertCircle className="mr-2" />
        <span>这是演示版本, 并非所有功能都可以正常工作。更多功能需要您来增强并实现。</span>
      </div> */}
    </div>
  );
};

export default NERPage;