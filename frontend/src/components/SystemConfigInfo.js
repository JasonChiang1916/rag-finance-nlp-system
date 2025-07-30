import React from 'react';
import { Info, Cpu, Database, Settings } from 'lucide-react';

/**
 * 系统配置信息显示组件
 * 显示当前后端配置信息，让用户了解系统状态
 */
const SystemConfigInfo = ({ config, embeddingOptions, className = "" }) => {
  if (!config) {
    return (
      <div className={`bg-gray-50 border border-gray-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center">
          <Settings className="w-5 h-5 text-gray-400 mr-2 animate-spin" />
          <span className="text-gray-600">正在加载系统配置...</span>
        </div>
      </div>
    );
  }

  const modelInfo = config.model_info || {};
  const getStatusColor = (type) => {
    switch (type) {
      case 'lightweight':
        return 'text-green-700 bg-green-50 border-green-200';
      case 'balanced':
        return 'text-blue-700 bg-blue-50 border-blue-200';
      case 'complete':
        return 'text-purple-700 bg-purple-50 border-purple-200';
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  const getTypeLabel = (type) => {
    switch (type) {
      case 'lightweight':
        return '轻量模式';
      case 'balanced':
        return '平衡模式';
      case 'complete':
        return '完整模式';
      default:
        return '自定义模式';
    }
  };

  return (
    <div className={`border rounded-lg p-4 ${getStatusColor(modelInfo.type)} ${className}`}>
      <div className="flex items-center mb-3">
        <Info className="w-5 h-5 mr-2" />
        <span className="font-semibold">当前系统配置</span>
        <span className={`ml-2 px-2 py-1 text-xs rounded-full font-medium ${
          modelInfo.type === 'lightweight' ? 'bg-green-100 text-green-800' :
          modelInfo.type === 'balanced' ? 'bg-blue-100 text-blue-800' :
          modelInfo.type === 'complete' ? 'bg-purple-100 text-purple-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {getTypeLabel(modelInfo.type)}
        </span>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
        <div className="flex items-center">
          <Cpu className="w-4 h-4 mr-2 opacity-70" />
          <div>
            <div className="font-medium">嵌入模型</div>
            <div className="opacity-80">{modelInfo.description || '未知'}</div>
            <div className="text-xs opacity-60">大小: {modelInfo.size || '未知'}</div>
          </div>
        </div>
        
        <div className="flex items-center">
          <Database className="w-4 h-4 mr-2 opacity-70" />
          <div>
            <div className="font-medium">向量数据库</div>
            <div className="opacity-80">{embeddingOptions?.dbName || '未配置'}</div>
            <div className="text-xs opacity-60">集合: {embeddingOptions?.collectionName || '未配置'}</div>
          </div>
        </div>
        
        <div className="flex items-center">
          <Settings className="w-4 h-4 mr-2 opacity-70" />
          <div>
            <div className="font-medium">提供商</div>
            <div className="opacity-80">{embeddingOptions?.provider || '未配置'}</div>
            <div className="text-xs opacity-60">
              状态: <span className="text-green-600">●</span> 已连接
            </div>
          </div>
        </div>
      </div>
      
      {/* 性能提示 */}
      <div className="mt-3 pt-3 border-t border-current border-opacity-20">
        <div className="text-xs opacity-75">
          {modelInfo.type === 'lightweight' && (
            <span>💡 轻量模式：启动快速，适合开发测试</span>
          )}
          {modelInfo.type === 'balanced' && (
            <span>⚖️ 平衡模式：性能与速度兼顾，推荐生产使用</span>
          )}
          {modelInfo.type === 'complete' && (
            <span>🚀 完整模式：最佳精度，适合高要求场景</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default SystemConfigInfo;
