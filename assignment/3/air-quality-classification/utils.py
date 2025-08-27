from __future__ import annotations
import re
import numpy as np
import pandas as pd
from typing import Tuple, List, Optional

TARGET_GUESSES = [
    "target", "label", "class", "category", "aqi_bucket", "aqi_category",
    "aqi_level", "pollution_level", "pollution_category", "y"
]

def read_data(path_or_url: str) -> pd.DataFrame:
    df = pd.read_csv(path_or_url)
    df.columns = [re.sub(r"\s+", "_", c.strip().lower()) for c in df.columns]
    return df

def guess_target_column(df: pd.DataFrame, user_target: Optional[str]=None) -> str:
    if user_target:
        t = user_target.strip().lower()
        if t in df.columns:
            return t
        raise ValueError(f"--target '{user_target}' not found. Available: {list(df.columns)}")

    non_num = [c for c in df.columns if not np.issubdtype(df[c].dtype, np.number)]
    if non_num:
        small_cats = sorted(non_num, key=lambda c: df[c].nunique())
        for c in small_cats:
            nunq = df[c].nunique(dropna=True)
            if 1 < nunq < max(100, int(0.1*len(df))):
                return c
        return non_num[0]

    for cand in TARGET_GUESSES:
        if cand in df.columns:
            return cand

    return df.columns[-1]

def split_xy(df: pd.DataFrame, target: str) -> Tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[target])
    y = df[target]
    return X, y

def basic_feature_clean(X: pd.DataFrame) -> pd.DataFrame:
    nunq = X.nunique()
    keep = nunq[nunq > 1].index.tolist()
    X = X[keep]

    timeish = [c for c in X.columns if "time" in c or "date" in c]
    for c in timeish:
        try:
            dt = pd.to_datetime(X[c], errors="raise", infer_datetime_format=True)
            X[f"{c}_hour"] = dt.dt.hour
            X[f"{c}_dow"] = dt.dt.dayofweek
            X[f"{c}_month"] = dt.dt.month
            X = X.drop(columns=[c])
        except Exception:
            pass
    return X

def separate_types(X: pd.DataFrame) -> Tuple[List[str], List[str]]:
    num_cols = [c for c in X.columns if np.issubdtype(X[c].dtype, np.number)]
    cat_cols = [c for c in X.columns if c not in num_cols]
    return num_cols, cat_cols
