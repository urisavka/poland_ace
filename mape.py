def mape(y_pred, y_true):
    res = 0
    for i in range(len(y_true)):
        res += abs((y_pred[i] - y_true[i])/y_true[i])
    return res[0]/len(y_true) * 100