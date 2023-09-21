import os
import joblib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error



main_path = os.getcwd()

data_path = os.path.join(main_path, "2022-rappler-articles-submission.csv")


# assert expected values
# note for pytest to work, function must start with test_
def test_data(
    df=None,
    data_path=data_path,
):
    # read data
    if df is None:
        df = pd.read_csv(data_path)
    
    cols = [
        'AFRAID', 'AMUSED', 'ANGRY', 'ANNOYED',
        'DONT_CARE', 'HAPPY', 'INSPIRED', 'SAD'
    ]
    
    for col in cols:
        assert (df[col] >= 0).all()
        assert (df[col] <= 1).all()

    assert df[cols].sum(axis=1).apply(lambda x: np.isclose(x, 1)).all()
    
    assert df['title.rendered'].apply(lambda x: isinstance(x, str)).all()
    assert df['content.rendered'].apply(lambda x: isinstance(x, str)).all()
    try:
        pd.to_datetime(df['date'], errors='raise')
    except ValueError as e:
        raise AssertionError(f"Error: {e}. Values in the date column cannot be casted to datetime.")
    print('Data passed all tests.')


