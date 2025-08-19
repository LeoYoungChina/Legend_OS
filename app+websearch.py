from textwrap import dedent
import streamlit as st
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.thinking import ThinkingTools
from agno.tools.tavily import TavilyTools
from agno.tools.reasoning import ReasoningTools

def initialize_app():
    """初始化应用程序界面和状态"""
    # 设置应用标题
    st.title("Legend OS智能私人助理")
    
    # 设置侧边栏
    st.sidebar.title("设置")
    think_mode = st.sidebar.checkbox("开启Think模式", value=True)
    
    # 初始化会话状态
    if "msgs" not in st.session_state:
        st.session_state["msgs"] = []
    
    return think_mode

def setup_agent(think_mode):
    """初始化并配置AI助手"""
    agent = Agent(
        model=Ollama(id="qwen3:1.7b"),
        markdown=True,
        tools=[
        ThinkingTools(think=True,add_instructions=True),
        ReasoningTools(add_instructions=True),
        TavilyTools(api_key="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",),
    ],
        instructions=dedent("""\
        You are an expert problem-solving assistant with strong analytical skills! 🧠

        Your approach to problems:
        1. First, break down complex questions into component parts
        2. Clearly state your assumptions
        3. Develop a structured reasoning path
        4. Consider multiple perspectives
        5. Evaluate evidence and counter-arguments
        6. Draw well-justified conclusions

        When solving problems:
        - Use explicit step-by-step reasoning
        - Identify key variables and constraints
        - Explore alternative scenarios
        - Highlight areas of uncertainty
        - Explain your thought process clearly
        - Consider both short and long-term implications
        - Evaluate trade-offs explicitly

        For quantitative problems:
        - Show your calculations
        - Explain the significance of numbers
        - Consider confidence intervals when appropriate
        - Identify source data reliability

        For qualitative reasoning:
        - Assess how different factors interact
        - Consider psychological and social dynamics
        - Evaluate practical constraints
        - Address value considerations
        \
    """),
        show_tool_calls=True,
    )

    agent.think = think_mode
    return agent

def display_chat_history():
    """
    显示历史对话记录。
    
    从会话状态中读取消息列表，并按照消息的角色（如用户或助手）和内容格式化为聊天界面。
    每条消息会以对应的角色样式显示，并使用Markdown渲染内容。
    
    作用范围：
    - 导出的函数，供其他模块调用。
    """
    """显示历史对话记录"""
    for msg in st.session_state["msgs"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def prepare_messages(think_mode):
    """准备发送给模型的消息列表"""
    messages = []
    for i, msg in enumerate(st.session_state["msgs"]):
        content = msg["content"]
        # 如果是最后一条用户消息且Think模式关闭，添加/no_think指令
        if (i == len(st.session_state["msgs"]) - 1 and 
            msg["role"] == "user" and not think_mode):
            content = f"/no_think {content}"
        
        messages.append({"role": msg["role"], "content": content})
    return messages

def process_assistant_response(agent, messages):
    """处理助手回复并显示"""
    message_placeholder = st.empty()
    full_response = ""
    
    # 流式获取回复
    run_response = agent.run(messages=messages, stream=True)
    for chunk in run_response:
        if chunk.content:
            full_response += chunk.content
            # 显示打字效果
            message_placeholder.markdown(full_response + "|")
    
    # 显示最终回复
    message_placeholder.markdown(full_response)
    return full_response

def main():
    """主程序入口"""
    # 初始化应用
    think_mode = initialize_app()
    agent = setup_agent(think_mode)
    
    # 显示历史对话
    display_chat_history()
    
    # 获取用户输入
    prompt = st.chat_input("请输入您的问题")
    
    # 处理用户输入
    if prompt:
        # 添加用户消息到历史记录
        st.session_state["msgs"].append({"role": "user", "content": prompt})
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成并显示助手回复
        with st.chat_message("assistant"):
            messages = prepare_messages(think_mode)
            full_response = process_assistant_response(agent, messages)
            
            # 保存助手回复到历史记录
            st.session_state["msgs"].append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
