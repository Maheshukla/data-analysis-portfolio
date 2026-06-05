import pandas as pd

files = [
    "data/ODI_Match_Data.csv",
    "data/ODI_Match_info.csv",
    "data/matchwise_data.csv",
    "data/matches_updated_ipl_upto_2025.csv"
]

for file in files:
    try:
        df = pd.read_csv(file)
        print("\n" + "="*80)
        print(file)
        print("="*80)
        print(df.columns.tolist())
    except Exception as e:
        print(f"{file} -> {e}")