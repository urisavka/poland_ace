def mape(y_pred, y_true):
    res = 0
    for i in range(len(y_true)):
        res += abs((y_pred[i] - y_true[i])/y_true[i])
    if isinstance(res, list):
        return res[0]/len(y_true) * 100
    return res / len(y_true) * 100
