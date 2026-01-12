from pathlib import Path
import json

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def save_json(obj: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def stratified_downsample(df, target_col: str, n: int, random_state: int):
    if n is None or n <= 0 or n >= len(df):
        return df
    return (
        df.groupby(target_col, group_keys=False)
          .apply(lambda g: g.sample(
              n=max(1, int(round(n * len(g) / len(df)))),
              random_state=random_state
          ))
          .sample(frac=1.0, random_state=random_state)
          .reset_index(drop=True)
    )
