import numpy as np

def mae(y_true, y_pred): 
    return float(np.mean(np.abs(y_true - y_pred)))

def rmse(y_true, y_pred): 
    return float(np.sqrt(np.mean((y_true - y_pred)**2)))

def mape(y_true, y_pred):
    denom = np.clip(np.abs(y_true), 1e-8, None)
    return float(np.mean(np.abs((y_true - y_pred)/denom)) * 100)

def direction_acc(y_true, y_pred):
    y_true_dir = np.sign(np.diff(y_true, prepend=y_true[0]))
    y_pred_dir = np.sign(np.diff(y_pred, prepend=y_pred[0]))
    return float(np.mean(y_true_dir == y_pred_dir))
