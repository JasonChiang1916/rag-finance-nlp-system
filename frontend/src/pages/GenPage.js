import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { LLMOptions, TextInput } from '../components/shared/ModelOptions';

const GenPage = () => {
  // 基础状态
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState('');
  
  // 方法选择
  const [method, setMethod] = useState('generate_financial_report');
  const methods = {
    generate_financial_report: '生成金融报告',
    generate_investment_analysis: '生成投资分析',
    generate_risk_assessment: '生成风险评估'
  };

  // 公司信息
  const [companyInfo, setCompanyInfo] = useState({
    name: '',
    sector: '',
    market_cap: '',
    financial_history: ''
  });

  // 财务数据列表
  const [financialData, setFinancialData] = useState('');
  const [analysisType, setAnalysisType] = useState('');
  const [recommendations, setRecommendations] = useState('');

  // LLM 选项
  const [llmOptions, setLlmOptions] = useState({
    provider: 'ollama',
    model: 'qwen2.5:7b'
  });

  const handleCompanyInfoChange = (e) => {
    const { name, value } = e.target;
    setCompanyInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLlmOptionChange = (e) => {
    const { name, value } = e.target;
    setLlmOptions(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFinancialDataChange = (e) => {
    setFinancialData(e.target.value);
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/gen', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          company_info: companyInfo,
          financial_data: financialData.split('\n').filter(s => s.trim()),
          analysis_type: analysisType,
          recommendations,
          method,
          llmOptions
        }),
      });
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('Error:', error);
      setResult('处理请求时发生错误。');
    }
    setIsLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">金融内容生成 💰</h1>

      <div className="grid grid-cols-3 gap-6">
        {/* 左侧面板：输入表单 */}
        <div className="col-span-2 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">公司信息</h2>
          
          {/* 公司基本信息 */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">公司名称</label>
              <input
                type="text"
                name="name"
                value={companyInfo.name}
                onChange={handleCompanyInfoChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                placeholder="请输入公司名称..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">所属行业</label>
              <input
                type="text"
                name="sector"
                value={companyInfo.sector}
                onChange={handleCompanyInfoChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                placeholder="如：科技、金融、制造业..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">市值规模</label>
              <select
                name="market_cap"
                value={companyInfo.market_cap}
                onChange={handleCompanyInfoChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              >
                <option value="">选择市值规模</option>
                <option value="large">大型企业 (&gt;500亿)</option>
                <option value="medium">中型企业 (50-500亿)</option>
                <option value="small">小型企业 (&lt;50亿)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">财务历史</label>
              <input
                type="text"
                name="financial_history"
                value={companyInfo.financial_history}
                onChange={handleCompanyInfoChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                placeholder="如：过去三年业绩表现..."
              />
            </div>
          </div>

          {/* 财务数据输入 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">财务数据（每行一个）</label>
            <TextInput
              value={financialData}
              onChange={handleFinancialDataChange}
              rows={3}
              placeholder="输入财务数据，每行一个，如：营收增长15%、净利润率12%..."
            />
          </div>

          {/* 分析类型和建议（仅在生成金融报告时显示） */}
          {method === 'generate_financial_report' && (
            <>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">分析类型</label>
                <select
                  value={analysisType}
                  onChange={(e) => setAnalysisType(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                >
                  <option value="">选择分析类型</option>
                  <option value="quarterly_analysis">季度分析</option>
                  <option value="annual_analysis">年度分析</option>
                  <option value="comparative_analysis">对比分析</option>
                  <option value="trend_analysis">趋势分析</option>
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">投资建议</label>
                <TextInput
                  value={recommendations}
                  onChange={(e) => setRecommendations(e.target.value)}
                  rows={2}
                  placeholder="输入投资建议和展望..."
                />
              </div>
            </>
          )}

          <button
            onClick={handleSubmit}
            className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 w-full"
            disabled={isLoading}
          >
            {isLoading ? '生成中...' : '生成内容'}
          </button>
        </div>

        {/* 右侧面板：选项 */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">选项</h2>
          
          {/* 方法选择 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">生成方法</label>
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            >
              {Object.entries(methods).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          {/* LLM 选项 */}
          <LLMOptions options={llmOptions} onChange={handleLlmOptionChange} />
        </div>
      </div>

      {/* 结果显示 */}
      {result && (
        <div className="mt-6">
          <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-6" role="alert">
            <p className="font-bold">生成结果：</p>
            <pre className="whitespace-pre-wrap">{result}</pre>
          </div>
        </div>
      )}

      {/* <div className="flex items-center text-yellow-700 bg-yellow-100 p-4 rounded-md mt-6">
        <AlertCircle className="mr-2" />
        <span>这是演示版本, 并非所有功能都可以正常工作。更多功能需要您来增强并实现。</span>
      </div> */}
    </div>
  );
};

export default GenPage; 