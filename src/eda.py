from pathlib import Path

import pandas as pd
import structlog
from tabulate import tabulate
from ydata_profiling import ProfileReport

logger: structlog.stdlib.BoundLogger = structlog.get_logger()


def load_data(file_path: str | Path) -> pd.DataFrame:
    """Loads the cocktail dataset from the JSON file (OS agnostic file path)."""
    logger.info(f"Loading data from {file_path}")
    cocktail_df = pd.read_json(Path(file_path).resolve())
    logger.info(f"Loaded dataset with shape: {cocktail_df.shape}")
    return cocktail_df


def _calculate_missing_percentage(df_column: pd.DataFrame) -> float:
    return (df_column.isna().sum() / len(df_column) * 100).round(2)


def explore_data(cocktail_df: pd.DataFrame) -> None:
    """Basic exploration of the given dataset."""
    logger.info("Starting dataset exploration")
    print("\n\n=== Dataset Exploration ===")

    print(f"Number of cocktails: {len(cocktail_df)}")

    print("\nColumns info:")
    cols_info = pd.DataFrame({
        "Column": col,
        'Data Type': cocktail_df[col].dtype,
        'Missing Values': cocktail_df[col].isna().sum(),
        'Missing Percentage': _calculate_missing_percentage(cocktail_df[col]),
    } for col in cocktail_df.columns)
    print(tabulate(cols_info, headers=cols_info.keys()))

    header = "Category distribution"
    print(f"\n{header}")
    print(f"{"-" * len(header)}")
    category_distribution = cocktail_df["category"].value_counts()
    print(category_distribution)

    header = "Glass type distribution"
    print(f"\n{header}")
    print(f"{"-" * len(header)}")
    glass_distribution = cocktail_df["glass"].value_counts()
    print(glass_distribution)

    header = "Alcoholic drink type distribution"
    print(f"\n{header}")
    print(f"{"-" * len(header)}")
    alcoholic_distribution = cocktail_df["alcoholic"].value_counts()
    print(alcoholic_distribution)

    print("\n\n=== Category-Glass correlation ===")
    contingency_table = pd.crosstab(cocktail_df["category"], cocktail_df["glass"])
    print(f"Contingency table shape: {contingency_table.shape}")
    print(f"Contingency table:\n {contingency_table}")

    logger.info("Finished dataset exploration")


def run_ydata_profiling(cocktail_df: pd.DataFrame, report_path: str | Path) -> None:
    logger.info("Creating a dataset report using ydata-profiling library")
    dataset_profile = ProfileReport(cocktail_df, title = "Cocktail dataset report")
    dataset_profile.to_file(report_path, silent=True)


if __name__ == "__main__":
    file_path = Path(__file__).parents[1] / "data" / "cocktail_dataset.json"
    cocktail_df = load_data(file_path)
    explore_data(cocktail_df)
    reports_dir = Path(__file__).parents[1] / "reports"
    reports_dir.mkdir(exist_ok=True)
    report_path = reports_dir / "cocktail_dataset_report.html"
    run_ydata_profiling(cocktail_df, report_path)
