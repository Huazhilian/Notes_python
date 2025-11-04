import argparse, json
import numpy as np
import pandas as pd
from joblib import load
from tensorflow import keras

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="CSV with same schema as training (without target).")
    ap.add_argument("--model_dir", default="models")
    ap.add_argument("--use_mlp", action="store_true")
    args = ap.parse_args()

    X = pd.read_csv(args.csv)
    X.columns = [c.strip().lower().replace(" ", "_") for c in X.columns]

    if args.use_mlp:
        pre = load(f"{args.model_dir}/preproc.joblib")
        model = keras.models.load_model(f"{args.model_dir}/mlp_model.keras")
        with open(f"{args.model_dir}/labels.json") as f:
            id2cls = {int(v): k for v, k in json.load(f).items()}
        Xt = pre.transform(X)
        probs = model.predict(Xt, verbose=0)
        y_pred = probs.argmax(axis=1)
        labels = [id2cls[int(i)] for i in y_pred]
        out = X.copy()
        out["prediction"] = labels
        out.to_csv("predictions.csv", index=False)
        print("Saved predictions to predictions.csv")
    else:
        pipe = load(f"{args.model_dir}/hgb_model.joblib")
        y_pred = pipe.predict(X)
        out = X.copy()
        out["prediction"] = y_pred
        out.to_csv("predictions.csv", index=False)
        print("Saved predictions to predictions.csv")

if __name__ == "__main__":
    main()
