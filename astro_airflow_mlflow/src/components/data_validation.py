# data_validation.py file

from src.entity.config_entity import DataValidationConfig
from src.utils.common import create_directories
from src import src_logger
from pathlib import Path
import yaml
import pandas as pd
import os


class DataValidation:
    def __init__(self, config: DataValidationConfig) -> None:
        self.config = config
        create_directories([self.config.root_dir])

    @staticmethod
    def _dtype_compatible(observed: str, expected: str) -> bool:
        if observed == expected:
            return True
        # object covers any string-like dtype produced by pd.read_csv.
        if expected == "object" and observed.startswith("object"):
            return True
        # Tolerate widening from int -> float when CSV has trailing .0 values.
        if expected == "float64" and observed in {"int64", "Int64"}:
            return True
        return False

    def validate_columns(self, df: pd.DataFrame, expected: dict) -> tuple[bool, list[str]]:
        observed = set(df.columns)
        missing = [c for c in expected if c not in observed]
        return (len(missing) == 0, missing)

    def validate_dtypes(self, df: pd.DataFrame, expected: dict) -> tuple[bool, list[str]]:
        mismatches: list[str] = []
        for col, want in expected.items():
            if col not in df.columns:
                continue
            got = str(df[col].dtype)
            if not self._dtype_compatible(got, want):
                mismatches.append(f"{col}: expected={want} got={got}")
        return (len(mismatches) == 0, mismatches)

    def validate_data(self) -> bool:
        """Validate every CSV under dataset_path against schema.raw_columns.
        Returns True only when every file has the required columns with
        compatible dtypes.
        """
        src_logger.info("Validating data against schema")
        expected = self.config.raw_columns
        src_logger.info(f"Required raw columns: {list(expected)}")

        files = [f for f in os.listdir(self.config.dataset_path) if f.endswith(".csv")]
        src_logger.info(f"Found {len(files)} CSV files at {self.config.dataset_path}")
        if not files:
            src_logger.error("No CSV files found")
            return False

        all_ok = True
        for fname in files:
            path = os.path.join(self.config.dataset_path, fname)
            try:
                df = pd.read_csv(path)
            except Exception as e:
                src_logger.error(f"Failed to read {fname}: {e}")
                all_ok = False
                continue

            cols_ok, missing = self.validate_columns(df, expected)
            if not cols_ok:
                src_logger.error(f"{fname} missing required columns: {missing}")
                all_ok = False

            dtypes_ok, mismatches = self.validate_dtypes(df, expected)
            if not dtypes_ok:
                src_logger.error(f"{fname} dtype mismatches: {mismatches}")
                all_ok = False

            if cols_ok and dtypes_ok:
                src_logger.info(f"{fname} OK")

        if all_ok:
            src_logger.info("Data validation passed for all CSVs")
        else:
            src_logger.error("Data validation failed for one or more CSVs")
        return all_ok

    def save_validation_status(self, status: bool) -> None:
        status_file_path = self.config.STATUS_FILE
        with open(status_file_path, "w") as f:
            yaml.dump({"Validation": status}, f)
        src_logger.info(f"Validation status saved to {status_file_path}")

    def get_dataset_path(self) -> Path:
        return Path(self.config.dataset_path)
