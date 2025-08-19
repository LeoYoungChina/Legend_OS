import ollama
import streamlit as st

# 创建一个Streamlit应用程序标题
st.title("Legend OS智能私人助理")

#初始化对话记录
if "msgs" not in st.session_state:
    st.session_state["msgs"] = []
    
# 显示之前的对话记录
for msg in st.session_state["msgs"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
# 提示用户输入问题
prompt = st.chat_input("请输入您的问题")

# 如果用户输入了问题，则进行对话
if prompt:
    # 将用户输入添加到对话记录中
    st.session_state["msgs"].append({"role": "user", "content": prompt})
    
    # 显示用户的消息
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 生成并显示助手的回复    
    with st.chat_message("assistant"):
        # 创建一个空的消息占位符
        message_placeholder = st.empty()
        full_response = ""
        
        # 使用ollama大模型平台与AI模型进行对话（流式）
        for chunk in ollama.chat(
             model="Qwen3:1.7B",
             messages=st.session_state["msgs"],
             stream=True,
         ):
            # 获取每个响应块的内容并添加到完整响应中
            if "content" in chunk["message"]:
                content_chunk = chunk["message"]["content"]
                full_response += content_chunk
                # 实时更新显示的内容
                message_placeholder.markdown(full_response + "|")
        
        # 显示最终完整的响应（去掉光标）
        message_placeholder.markdown(full_response)
        
        # 更新对话记录以包含助手的完整回复
        st.session_state["msgs"].append({"role": "assistant", "content": full_response})
