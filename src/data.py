import pandas as pd

def load_variant_summary(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", compression="gzip", low_memory=False)
    return df

def clean_variants(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df[df["ClinSigSimple"].isin([0, 1])].copy()

    required = ["Type", "Chromosome", "Start", "Stop", "GeneSymbol"]
    df = df.dropna(subset=required).copy()

    df["Start"] = pd.to_numeric(df["Start"], errors="coerce")
    df["Stop"] = pd.to_numeric(df["Stop"], errors="coerce")
    df = df.dropna(subset=["Start", "Stop"]).copy()

    df["Start"] = df["Start"].astype(int)
    df["Stop"] = df["Stop"].astype(int)

    return df
