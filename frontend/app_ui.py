import streamlit as st
import requests
import json

# 页面配置
st.set_page_config(page_title="Iris Flower Predictor", page_icon="🌸")

st.title("🌸 鸢尾花分类预测")
st.markdown("输入花的特征，AI 模型将告诉你这是哪一种鸢尾花。")

# API 地址 (如果部署到云端，这里需要换成云端 URL)
API_URL = "http://localhost:8000/predict"
# 如果你是在 docker-compose 里运行，且前端后端在不同容器，可能需要用容器名
# API_URL = "http://api:8000/predict"

# 创建输入表单
with st.form("prediction_form"):
    st.subheader("输入特征参数")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sepal_length = st.number_input("花萼长度 (cm)", min_value=0.0, max_value=10.0, value=5.1)
        sepal_width = st.number_input("花萼宽度 (cm)", min_value=0.0, max_value=10.0, value=3.5)
    
    with col2:
        petal_length = st.number_input("花瓣长度 (cm)", min_value=0.0, max_value=10.0, value=1.4)
        petal_width = st.number_input("花瓣宽度 (cm)", min_value=0.0, max_value=10.0, value=0.2)
        
    submit_button = st.form_submit_button("开始预测")

if submit_button:
    # 构造请求数据
    data = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width
    }
    
    with st.spinner("正在请求模型 API..."):
        try:
            response = requests.post(API_URL, json=data)
            
            if response.status_code == 200:
                result = response.json()
                st.success(f"预测结果: {result['class_name']} (类别ID: {result['prediction']})")
                
                # 显示图片 (可选)
                if result['class_name'] == 'setosa':
                    st.image("https://upload.wikimedia.org/wikipedia/commons/5/56/Kosaciec_szczecinkowaty_Iris_setosa.jpg", caption="Iris Setosa", width=300)
                elif result['class_name'] == 'versicolor':
                    st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Iris_versicolor_3.jpg", caption="Iris Versicolor", width=300)
                elif result['class_name'] == 'virginica':
                    st.image("https://upload.wikimedia.org/wikipedia/commons/9/9f/Iris_virginica.jpg", caption="Iris Virginica", width=300)
            else:
                st.error(f"API 请求失败: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("无法连接到 API。请确保后端服务 (FastAPI) 正在运行。")