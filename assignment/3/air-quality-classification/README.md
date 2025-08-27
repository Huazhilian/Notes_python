# Air Quality Classification (Compact ML + MLP <=30k params)

## Quickstart

1. Create virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.\.venv\Scripts\activate    # Windows PowerShell
pip install -r requirements.txt
```

2. Run training (provide CSV path or raw GitHub raw URL):
```bash
python train.py --csv data/updated_pollution_dataset.csv --use_mlp --epochs 60
```

3. Run inference:
```bash
python infer.py --csv data/updated_pollution_dataset.csv --use_mlp
```

## Docker
Build and run:
```bash
docker build -t air-quality-clf:latest .
docker run --rm -v %cd%:/app air-quality-clf:latest \
  python train.py --csv data/updated_pollution_dataset.csv --use_mlp --epochs 60
```

## Notes
- The training script auto-detects the target column if you don't pass `--target`.
- Place the dataset at `data/updated_pollution_dataset.csv` or pass the raw GitHub raw URL.