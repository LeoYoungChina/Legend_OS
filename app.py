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
        
        # 使用ollama大模型平台与AI模型进行对话（非流式）
        response = ollama.chat(
             model="qwen:7b-chat",
             messages=st.session_state["msgs"],
             stream=False,
         )
        
        # 解析并显示助手的回复内容
        msg = response["message"]["content"]
        st.markdown(msg)
        
        # 更新对话记录以包含助手的回复
        st.session_state["msgs"].append({"role": "assistant", "content": msg})