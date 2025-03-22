from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport


def run_eda():
    data_file = Path(__file__).parents[1] / "data" / "cocktail_dataset.json"
    cocktail_df = pd.read_json(data_file)
    dataset_profile = ProfileReport(cocktail_df, title = "Cocktail dataset report")

    reports_dir = Path(__file__).parents[1] / "reports"
    reports_dir.mkdir(exist_ok=True)

    report_path = reports_dir / "cocktail_dataset_report.html"
    dataset_profile.to_file(report_path, silent=True)


def run():
    data_file = Path(__file__).parents[1] / "data" / "cocktail_dataset.json"
    cocktail_df = pd.read_json(data_file)
    print(cocktail_df.head(5))


if __name__ == "__main__":
    run_eda()
    run()
