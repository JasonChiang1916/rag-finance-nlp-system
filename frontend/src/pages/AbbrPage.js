import React, { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';
import { LLMOptions, EmbeddingOptions, TextInput } from '../components/shared/ModelOptions';
import { useSystemConfig } from '../hooks/useSystemConfig';
import SystemConfigInfo from '../components/SystemConfigInfo';

const AbbrPage = () => {
  const [input, setInput] = useState('');
  const [context, setContext] = useState('');
  const [result, setResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // 获取系统配置
  const { config, loading: configLoading, getDefaultEmbeddingOptions, getModelInfo } = useSystemConfig();
  
  // Method selection
  const [method, setMethod] = useState('simple_ollama');
  const methods = {
    simple_ollama: '简单大语言模型展开（快速）',
    llm_rank_query_db: '大语言模型展开 + 数据库标准化（更准确）'
  };

  // LLM options
  const [llmOptions, setLlmOptions] = useState({
    provider: 'ollama',
    model: 'qwen2.5:7b'
  });

  // 使用系统配置初始化嵌入选项
  const [embeddingOptions, setEmbeddingOptions] = useState(() => getDefaultEmbeddingOptions());

  // 当系统配置加载完成后，更新嵌入选项
  useEffect(() => {
    if (config) {
      setEmbeddingOptions(getDefaultEmbeddingOptions());
    }
  }, [config]);

  const handleLlmOptionChange = (e) => {
    const { name, value } = e.target;
    setLlmOptions(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleEmbeddingOptionChange = (e) => {
    const { name, value } = e.target;
    setEmbeddingOptions(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/abbr', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: input,
          context,
          method,
          llmOptions,
          embeddingOptions
        }),
      });
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('Error:', error);
      setResult('An error occurred while processing the request.');
    }
    setIsLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">金融缩写展开 📝</h1>

      {/* 系统配置信息显示 */}
      <SystemConfigInfo
        config={config}
        embeddingOptions={embeddingOptions}
        className="mb-6"
      />

      <div className="grid grid-cols-3 gap-6">
        {/* Left panel: Text inputs */}
        <div className="col-span-2 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">输入金融文档</h2>
          <TextInput
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="请输入包含缩写的金融文档..."
          />

          {method !== 'simple_ollama' && (
            <TextInput
              value={context}
              onChange={(e) => setContext(e.target.value)}
              rows={2}
              placeholder="输入上下文以获得更好的缩写展开效果..."
            />
          )}

          <button
            onClick={handleSubmit}
            className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 w-full"
            disabled={isLoading}
          >
            {isLoading ? '处理中...' : '展开缩写'}
          </button>
        </div>

        {/* Right panel: Options */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">选项</h2>
          
          {/* Method Selection */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">展开方法</label>
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

          {/* LLM Options */}
          <LLMOptions options={llmOptions} onChange={handleLlmOptionChange} />

          {/* Vector DB Options */}
          {method !== 'simple_ollama' && (
            <EmbeddingOptions options={embeddingOptions} onChange={handleEmbeddingOptionChange} />
          )}
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="mt-6">
          <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-6" role="alert">
            <p className="font-bold">结果：</p>
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

export default AbbrPage; 