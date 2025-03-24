import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import structlog
from tabulate import tabulate
from ydata_profiling import ProfileReport

logger: structlog.stdlib.BoundLogger = structlog.get_logger()


def _parse_data(file_path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Loads the cocktail dataset extracting cocktails and ingredients."""
    logger.info(f"Loading data from {file_path}")
    cocktail_df = pd.read_json(Path(file_path).resolve())

    with open(Path(file_path).resolve()) as file:
        data = json.load(file)

    ingredients_df = pd.json_normalize(data, 'ingredients')

    return cocktail_df, ingredients_df


def _calculate_missing_percentage(df_column: pd.DataFrame) -> float:
    return (df_column.isna().sum() / len(df_column) * 100).round(2)


def _explore_cocktail_data(cocktail_df: pd.DataFrame) -> None:
    """Basic exploration of the given dataset."""
    logger.info("Starting cocktail dataset exploration")
    print("\n\n=== Cocktail Dataset Exploration ===")

    print(f"Number of cocktails: {len(cocktail_df.id.unique())}")

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

    logger.info("Finished dataset exploration")


def _explore_ingredients_data(ingredients_df: pd.DataFrame) -> None:
    """Basic exploration of the given dataset."""
    logger.info("Starting ingredients dataset exploration")
    print("\n\n=== Ingredients Dataset Exploration ===")

    print(f"Number of cocktails: {len(ingredients_df.id.unique())}")

    print("\nColumns info:")
    cols_info = pd.DataFrame({
        "Column": col,
        'Data Type': ingredients_df[col].dtype,
        'Missing Values': ingredients_df[col].isna().sum(),
        'Missing Percentage': _calculate_missing_percentage(ingredients_df[col]),
    } for col in ingredients_df.columns)
    print(tabulate(cols_info, headers=cols_info.keys()))

    header = "Alcoholic ingredient type distribution"
    print(f"\n{header}")
    print(f"{"-" * len(header)}")
    alcoholic_distribution = ingredients_df["alcohol"].value_counts()
    print(alcoholic_distribution)

    header = "Ingredient type distribution"
    print(f"\n{header}")
    print(f"{"-" * len(header)}")
    type_distribution = ingredients_df["type"].value_counts()
    print(type_distribution)

    header = "Alcohol percentage distribution"
    print(f"\n{header}")
    print(f"{"-" * len(header)}")
    percentage_distribution = ingredients_df["percentage"].value_counts()
    print(percentage_distribution)

    logger.info("Finished dataset exploration")


def _run_ydata_profiling(
    dataset_df: pd.DataFrame,
    report_path: str | Path,
    title: str
) -> None:
    logger.info("Creating a dataset report using ydata-profiling library")
    dataset_profile = ProfileReport(dataset_df, title = title)
    dataset_profile.to_file(report_path, silent=True)


if __name__ == "__main__":
    dataset_path = Path(__file__).parents[1] / "data" / "cocktail_dataset.json"
    cocktail_df, ingredients_df = _parse_data(dataset_path)

    _explore_cocktail_data(cocktail_df)
    _explore_ingredients_data(ingredients_df)

    reports_dir = Path(__file__).parents[1] / "reports"
    reports_dir.mkdir(exist_ok=True)

    _run_ydata_profiling(
        cocktail_df,
        report_path=reports_dir / "cocktails_eda.html",
        title="Cocktail dataset report"
    )
    _run_ydata_profiling(
        ingredients_df,
        report_path=reports_dir / "ingredients_eda.html",
        title="Ingredients dataset report"
    )
