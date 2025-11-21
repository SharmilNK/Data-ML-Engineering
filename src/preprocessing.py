from sklearn.model_selection import train_test_split

def preprocess_data(df, config):
    """
    简单的数据清洗和切分
    """
    print("正在进行数据预处理...")
    
    # 1. 分离特征和标签
    # 假设最后一列是 target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    # 2. 划分训练集和测试集
    test_size = config['data']['test_size']
    random_state = config['data']['random_state']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"训练集大小: {X_train.shape}, 测试集大小: {X_test.shape}")
    return X_train, X_test, y_train, y_test