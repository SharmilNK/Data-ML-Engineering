import yaml
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
# from src.data_loader import load_data
# from src.preprocessing import preprocess_data

# 这里的 import 稍微处理一下，以便直接运行脚本
import sys
sys.path.append('.') 
from src.data_loader import load_data
from src.preprocessing import preprocess_data

def train_model():
    # 1. 加载配置
    config_path = "config/config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # 2. 加载数据
    df = load_data(config_path)

    # 3. 预处理
    X_train, X_test, y_train, y_test = preprocess_data(df, config)

    # 4. 初始化模型
    print("开始训练模型...")
    n_estimators = config['train']['n_estimators']
    max_depth = config['train']['max_depth']
    
    model = RandomForestClassifier(
        n_estimators=n_estimators, 
        max_depth=max_depth, 
        random_state=config['data']['random_state']
    )

    # 5. 训练
    model.fit(X_train, y_train)

    # 6. 评估
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"模型准确率: {acc:.4f}")
    print("分类报告:\n", classification_report(y_test, y_pred))

    # TODO: 在这里添加 MLFlow 或 Weights & Biases 记录代码
    # import wandb
    # wandb.init(project="my-ml-project")
    # wandb.log({"accuracy": acc})

    # 7. 保存模型
    save_path = config['train']['model_save_path']
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)
    print(f"模型已保存至: {save_path}")

if __name__ == "__main__":
    train_model()