from __future__ import annotations
import argparse, os, json
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.ensemble import HistGradientBoostingClassifier

import tensorflow as tf
from tensorflow import keras
from typing import Tuple

from utils import read_data, guess_target_column, split_xy, basic_feature_clean, separate_types

def build_small_mlp(input_dim: int, num_classes: int, budget: int = 30000) -> keras.Model:
    best = None
    for h1 in [128, 96, 64, 48, 32]:
        for h2 in [64, 48, 32, 24, 16]:
            params = input_dim*h1 + h1 + h1*h2 + h2 + h2*num_classes + num_classes
            if params <= budget:
                score = h1*h2
                if not best or score > best[0]:
                    best = (score, h1, h2, params)
    if best is None:
        h1, h2 = 32, 16
    else:
        _, h1, h2, params = best
        print(f"[INFO] Chosen MLP: h1={h1}, h2={h2}, ~params={params}")

    inputs = keras.Input(shape=(input_dim,))
    x = keras.layers.Dense(h1, activation="relu")(inputs)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dropout(0.15)(x)
    x = keras.layers.Dense(h2, activation="relu")(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Dropout(0.15)(x)

    outputs = keras.layers.Dense(num_classes, activation="softmax")(x)
    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path or URL to CSV (can be the GitHub raw link).")
    ap.add_argument("--target", default=None, help="Optional target column name if known.")
    ap.add_argument("--test_size", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--model_out", default="models")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--early_stop_patience", type=int, default=8)
    ap.add_argument("--use_mlp", action="store_true", help="Train a compact TensorFlow MLP too.")
    args = ap.parse_args()

    os.makedirs(args.model_out, exist_ok=True)

    df = read_data(args.csv)
    target = guess_target_column(df, args.target)
    print(f"[INFO] Target column: {target}")
    X, y = split_xy(df, target)

    X = basic_feature_clean(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.seed, stratify=y
    )

    num_cols, cat_cols = separate_types(X_train)
    num_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ])
    cat_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    pre = ColumnTransformer([
        ("num", num_pipe, num_cols),
        ("cat", cat_pipe, cat_cols)
    ])

    base_clf = HistGradientBoostingClassifier(
        learning_rate=0.1,
        max_depth=None,
        max_iter=300,
        random_state=args.seed
    )

    base_model = Pipeline([("pre", pre), ("clf", base_clf)])
    base_model.fit(X_train, y_train)
    y_pred = base_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("\n=== Baseline (HGB) ===")
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

    dump(base_model, os.path.join(args.model_out, "hgb_model.joblib"))
    with open(os.path.join(args.model_out, "baseline_metrics.json"), "w") as f:
        json.dump({"accuracy": float(acc)}, f, indent=2)

    if args.use_mlp:
        pre.fit(X_train, y_train)
        Xtr = pre.transform(X_train)
        Xte = pre.transform(X_test)

        classes = np.unique(y_train)
        cls_to_id = {c:i for i,c in enumerate(classes)}
        ytr = np.array([cls_to_id[v] for v in y_train])
        yte = np.array([cls_to_id[v] for v in y_test])

        model = build_small_mlp(Xtr.shape[1], num_classes=len(classes), budget=30000)
        cb = [
            keras.callbacks.EarlyStopping(
                monitor="val_accuracy", patience=args.early_stop_patience,
                mode="max", restore_best_weights=True
            )
        ]
        hist = model.fit(
            Xtr, ytr,
            validation_split=0.15,
            epochs=args.epochs,
            batch_size=256,
            callbacks=cb,
            verbose=1
        )
        mlp_acc = model.evaluate(Xte, yte, verbose=0)[1]
        print("\n=== Compact MLP (<=30k params) ===")
        print(f"Accuracy: {mlp_acc:.4f}")

        model.save(os.path.join(args.model_out, "mlp_model.keras"))
        dump(pre, os.path.join(args.model_out, "preproc.joblib"))
        with open(os.path.join(args.model_out, "labels.json"), "w") as f:
            json.dump({str(int(v)): str(k) for k, v in cls_to_id.items()}, f, indent=2)

        with open(os.path.join(args.model_out, "mlp_metrics.json"), "w") as f:
            json.dump({"accuracy": float(mlp_acc)}, f, indent=2)

if __name__ == "__main__":
    main()
