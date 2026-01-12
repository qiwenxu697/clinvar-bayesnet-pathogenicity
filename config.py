from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    repo_root: Path = Path(__file__).resolve().parents[1]
    data_raw: Path = repo_root / "data" / "raw"
    data_processed: Path = repo_root / "data" / "processed"
    results: Path = repo_root / "results"
    figures: Path = results / "figures"

@dataclass(frozen=True)
class ModelConfig:
    target: str = "ClinSigSimple_num"
    test_size: float = 0.2
    random_state: int = 42
    max_indegree: int = 4
