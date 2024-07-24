import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

def prepare_features(df1, df2):
    """
    Prepare features for KNN model from the historical data of two stocks.

    Parameters:
    df1 (pd.DataFrame): DataFrame containing historical data for stock 1.
    df2 (pd.DataFrame): DataFrame containing historical data for stock 2.

    Returns:
    np.ndarray: Feature matrix for KNN.
    np.ndarray: Labels for KNN.
    """
    df1['spread'] = df1['close_price'] - df2['close_price']
    df1['spread_shift'] = df1['spread'].shift(-1)
    df1['spread_diff'] = df1['spread'].diff()
    df1.dropna(inplace=True)

    X = df1[['spread', 'spread_diff']].values
    y = (df1['spread_shift'] > df1['spread']).astype(int).values
    
    return X, y

def train_knn(X, y, n_neighbors=5):
    """
    Train KNN model on the feature matrix and labels.

    Parameters:
    X (np.ndarray): Feature matrix for KNN.
    y (np.ndarray): Labels for KNN.
    n_neighbors (int): Number of neighbors for KNN.

    Returns:
    KNeighborsClassifier: Trained KNN model.
    """
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X, y)
    return knn

def predict_knn(model, X):
    """
    Predict the direction of the spread using the trained KNN model.

    Parameters:
    model (KNeighborsClassifier): Trained KNN model.
    X (np.ndarray): Feature matrix for prediction.

    Returns:
    np.ndarray: Predicted labels.
    """
    return model.predict(X)
