import re
import pandas as pd

_variant_mapping = {
    "single nucleotide variant": "SNV",
    "Deletion": "Deletion",
    "Insertion": "Indel",
    "Indel": "Indel",
    "Duplication": "Indel",
    "copy number gain": "CNV",
    "copy number loss": "CNV",
    "Microsatellite": "Other",
    "Variation": "Other",
    "Complex": "Other",
    "Translocation": "Other",
    "Inversion": "Other",
    "fusion": "Other",
    "protein only": "Other",
    "Tandem duplication": "Other",
}

_gene_mapping = {
    "TTN": "structural",
    "BRCA2": "tumor_suppressor",
    "ATM": "tumor_suppressor",
    "APC": "tumor_suppressor",
    "NF1": "tumor_suppressor",
    "BRCA1": "tumor_suppressor", "TP53": "tumor_suppressor",
    "PTEN": "tumor_suppressor", "VHL": "tumor_suppressor",
    "RB1": "tumor_suppressor", "MLH1": "tumor_suppressor",
    "MSH2": "tumor_suppressor", "MSH6": "tumor_suppressor",
    "PMS2": "tumor_suppressor", "PALB2": "tumor_suppressor",
    "APOE": "metabolism", "LDLR": "metabolism", "GBA": "metabolism",
    "PAH": "metabolism", "HFE": "metabolism",
    "CFTR": "channel_protein", "SCN5A": "channel_protein",
    "SCN1A": "channel_protein", "KCNQ1": "channel_protein",
    "FBN1": "structural", "COL1A1": "structural", "COL1A2": "structural",
    "MYH7": "structural", "MYBPC3": "structural",
    "RNASEL": "dna_repair", "MUTYH": "dna_repair",
}

_stop_pattern = re.compile(r"\(p\.[A-Za-z]{3}\d+(ter|\*)\)", re.IGNORECASE)

def _is_stopgain(name) -> bool:
    if pd.isna(name):
        return False
    s = str(name)
    if _stop_pattern.search(s):
        return True
    s_low = s.lower()
    indicators = ["nonsense mutation", "stop-gain", "stop_gain", "stopgained"]
    return any(x in s_low for x in indicators)

def _clean_chromosome(chrom_value) -> str:
    chrom_str = str(chrom_value).strip()
    if chrom_str in ["X", "Y"]:
        return "sex_chr"
    if chrom_str == "MT":
        return "mitochondrial"
    if chrom_str.lower() in ["na", "un", "nan"]:
        return "unknown"
    return "autosome"

def _count_diseases(pheno_list) -> int:
    if pd.isna(pheno_list) or pheno_list == "-":
        return 0
    return len(str(pheno_list).split(";"))

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    features = pd.DataFrame(index=df.index)

    features["VariantType"] = df["Type"].map(_variant_mapping).fillna("Other")

    variant_length = (df["Stop"] - df["Start"] + 1).clip(lower=1)
    features["LengthChange_bin"] = pd.cut(
        variant_length,
        bins=[-1, 1, 20, float("inf")],
        labels=["SNV", "small_indel", "large_indel"],
    )

    ref_len = df["ReferenceAllele"].astype(str).str.len()
    alt_len = df["AlternateAllele"].astype(str).str.len()
    length_change = alt_len - ref_len
    frameshift = (length_change % 3 != 0) & df["Type"].isin(["Deletion", "Insertion", "Indel"])
    features["Frameshift"] = frameshift.astype(int)

    features["StopGain"] = df["Name"].apply(_is_stopgain).astype(int)

    features["GeneGroup"] = df["GeneSymbol"].map(_gene_mapping).fillna("other")

    features["Chromosome_clean"] = df["Chromosome"].apply(_clean_chromosome)

    features["PositionBin"] = pd.qcut(df["Start"], q=3, labels=["low", "mid", "high"], duplicates="drop")

    disease_counts = df["PhenotypeList"].apply(_count_diseases)
    features["PhenotypeCount_bin"] = pd.cut(
        disease_counts,
        bins=[-1, 0, 2, 5, float("inf")],
        labels=["none", "few", "moderate", "many"],
    )

    features["ClinSigSimple_num"] = df["ClinSigSimple"].astype(int)

    return features
