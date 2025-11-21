import joblib
import yaml
import pandas as pd
import os

class ModelService:
    def __init__(self, config_path="config/config.yaml", model_path=None):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        if model_path is None:
            self.model_path = self.config['train']['model_save_path']
        else:
            self.model_path = model_path
            
        self.model = self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"模型文件未找到: {self.model_path}，请先运行 src/train.py")
        return joblib.load(self.model_path)

    def predict(self, input_data):
        """
        input_data: list or dict matching feature names
        """
        # 确保输入是 DataFrame 格式以便模型处理
        if isinstance(input_data, list):
            # 这里的列名需要根据实际数据集调整
            columns = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
            df = pd.DataFrame([input_data], columns=columns)
        elif isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        else:
            df = input_data
            
        prediction = self.model.predict(df)
        return prediction[0]