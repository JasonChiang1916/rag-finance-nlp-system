import { useState, useEffect } from 'react';

/**
 * 系统配置管理Hook
 * 从后端获取当前配置并提供给前端组件使用
 */
export const useSystemConfig = () => {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 获取系统配置
  const fetchConfig = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/config');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.status === 'success') {
        setConfig(result.data);
        setError(null);
      } else {
        throw new Error(result.message || '获取配置失败');
      }
    } catch (err) {
      console.error('获取系统配置失败:', err);
      setError(err.message);
      
      // 设置默认配置作为fallback
      setConfig({
        embedding: {
          provider: 'huggingface',
          model: 'sentence-transformers/all-MiniLM-L6-v2',
          dbName: 'financial_terms_minilm',
          collectionName: 'financial_terms'
        },
        model_info: {
          type: 'lightweight',
          size: '90MB',
          description: '轻量快速模型'
        }
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConfig();
  }, []);

  // 获取默认的嵌入选项
  const getDefaultEmbeddingOptions = () => {
    if (!config) {
      return {
        provider: 'huggingface',
        model: 'sentence-transformers/all-MiniLM-L6-v2',
        dbName: 'financial_terms_minilm',
        collectionName: 'financial_terms'
      };
    }
    
    return config.embedding;
  };

  // 获取模型信息
  const getModelInfo = () => {
    return config?.model_info || {
      type: 'lightweight',
      size: '90MB',
      description: '轻量快速模型'
    };
  };

  // 获取可用模型列表
  const getAvailableModels = () => {
    return config?.available_models || {};
  };

  // 刷新配置
  const refreshConfig = () => {
    fetchConfig();
  };

  return {
    config,
    loading,
    error,
    getDefaultEmbeddingOptions,
    getModelInfo,
    getAvailableModels,
    refreshConfig
  };
};

export default useSystemConfig;
