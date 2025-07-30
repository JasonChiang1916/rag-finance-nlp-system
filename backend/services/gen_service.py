from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, List
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenService:
    """
    金融文本生成服务
    提供金融报告、投资分析和风险评估等金融文本的生成功能
    """
    def __init__(self):
        pass
        
    def _get_llm(self, llm_options: dict):
        """
        根据配置获取语言模型实例
        
        Args:
            llm_options: 语言模型配置选项
            
        Returns:
            配置好的语言模型实例
            
        Raises:
            ValueError: 当提供不支持的模型提供商时
        """
        provider = llm_options.get("provider", "ollama")
        model = llm_options.get("model", "llama3.1:8b")
        
        if provider == "ollama":
            return Ollama(model=model)
        elif provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=0.7,  # 稍微提高温度以获得更有创意的输出
                api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def generate_financial_report(self,
                            company_info: Dict,
                            financial_data: List[str],
                            analysis_type: str,
                            recommendations: str,
                            llm_options: dict) -> Dict:
        """
        生成结构化的金融报告

        Args:
            company_info: 公司信息
            financial_data: 财务数据列表
            analysis_type: 分析类型
            recommendations: 建议
            llm_options: 语言模型配置选项

        Returns:
            包含输入信息和生成的金融报告的字典
        """
        llm = self._get_llm(llm_options)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional financial analyst.
            Generate a detailed financial report in a structured format including:
            1. Executive Summary
            2. Company Overview
            3. Financial Performance Analysis
            4. Key Metrics and Ratios
            5. Recommendations and Outlook

            Use financial terminology appropriately and maintain a professional tone."""),
            ("human", """
            Company Information:
            {company_info}

            Financial Data:
            {financial_data}

            Analysis Type:
            {analysis_type}

            Recommendations:
            {recommendations}
            """)
        ])
        
        chain = prompt | llm
        result = chain.invoke({
            "company_info": str(company_info),
            "financial_data": "\n".join(financial_data),
            "analysis_type": analysis_type,
            "recommendations": recommendations
        })

        return {
            "input": {
                "company_info": company_info,
                "financial_data": financial_data,
                "analysis_type": analysis_type,
                "recommendations": recommendations
            },
            "output": result.content if hasattr(result, 'content') else str(result)
        }

    def generate_investment_analysis(self,
                                      market_data: List[str],
                                      llm_options: dict) -> Dict:
        """
        根据市场数据生成投资分析

        Args:
            market_data: 市场数据列表
            llm_options: 语言模型配置选项

        Returns:
            包含输入数据和生成的投资分析的字典
        """
        llm = self._get_llm(llm_options)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial investment expert.
            Generate a comprehensive investment analysis based on the provided market data.
            For each investment opportunity, provide:
            1. The investment type/asset
            2. Risk assessment
            3. Potential returns
            4. Market outlook

            Order the recommendations from most attractive to least attractive."""),
            ("human", "Market Data:\n{market_data}")
        ])

        chain = prompt | llm
        result = chain.invoke({
            "market_data": "\n".join(market_data)
        })

        return {
            "input": {
                "market_data": market_data
            },
            "output": result.content if hasattr(result, 'content') else str(result)
        }

    def generate_risk_assessment(self,
                              portfolio_info: str,
                              market_conditions: Dict,
                              llm_options: dict) -> Dict:
        """
        生成详细的风险评估报告

        Args:
            portfolio_info: 投资组合信息
            market_conditions: 市场条件
            llm_options: 语言模型配置选项

        Returns:
            包含输入信息和生成的风险评估的字典
        """
        llm = self._get_llm(llm_options)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial risk management expert.
            Generate a comprehensive risk assessment that includes:
            1. Market risk analysis
            2. Credit risk evaluation
            3. Liquidity risk assessment
            4. Operational risk factors
            5. Risk mitigation strategies

            Consider the portfolio composition and current market conditions in your analysis."""),
            ("human", """
            Portfolio Information: {portfolio_info}
            Market Conditions: {market_conditions}
            """)
        ])

        chain = prompt | llm
        result = chain.invoke({
            "portfolio_info": portfolio_info,
            "market_conditions": str(market_conditions)
        })

        return {
            "input": {
                "portfolio_info": portfolio_info,
                "market_conditions": market_conditions
            },
            "output": result.content if hasattr(result, 'content') else str(result)
        }