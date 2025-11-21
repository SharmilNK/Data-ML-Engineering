from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# 添加项目根目录到 path，确保能导入 src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import ModelService

app = FastAPI(title="ML Project API", version="1.0")

# 初始化模型服务
# 注意：Docker 运行时路径可能需要调整，这里假设在根目录下运行
model_service = None

@app.on_event("startup")
def load_model():
    global model_service
    try:
        model_service = ModelService()
        print("模型加载成功")
    except Exception as e:
        print(f"模型加载失败: {e}")

class PredictionRequest(BaseModel):
    # 定义输入数据格式 (基于 Iris 数据集)
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML API"}

@app.post("/predict")
def predict(request: PredictionRequest):
    if not model_service:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # 将输入转换为列表或字典
        input_data = {
            'sepal length (cm)': request.sepal_length,
            'sepal width (cm)': request.sepal_width,
            'petal length (cm)': request.petal_length,
            'petal width (cm)': request.petal_width
        }
        result = model_service.predict(input_data)
        
        # Iris target mapping (0: setosa, 1: versicolor, 2: virginica)
        target_names = ['setosa', 'versicolor', 'virginica']
        class_name = target_names[int(result)]
        
        return {"prediction": int(result), "class_name": class_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))