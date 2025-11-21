import pandas as pd
from sklearn.datasets import load_iris
import yaml
import os

# 模拟云端下载逻辑
def download_data_from_cloud(config):
    print("正在尝试从云端下载数据...")
    # TODO: 这里实现真正的云端下载逻辑
    # 例如使用 google.cloud.storage 或 boto3
    # bucket_name = "my-project-bucket"
    # source_blob_name = "data/iris.csv"
    # destination_file_name = config['data']['raw_data_path']
    pass

def load_data(config_path="config/config.yaml"):
    """
    加载数据。
    为了演示方便，如果本地没有文件，默认加载 Sklearn 的 Iris 数据集。
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    if config['data']['download_from_cloud']:
        download_data_from_cloud(config)

    print("正在加载数据...")
    
    # 这里是为了演示方便，直接用 sklearn 的数据
    # 在实际项目中，你应该使用 pd.read_csv(config['data']['raw_data_path'])
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    
    print(f"数据加载成功，形状: {df.shape}")
    return df