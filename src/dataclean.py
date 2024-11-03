import json
from src.calculator import CoOccurrenceCalculator
from src.config import DATA_DIR
from src.dataset import load_dataset_mie
import pandas as pd
import re

csv_path = DATA_DIR / "university-clean-list.csv"
df = pd.read_csv(csv_path)


def find_university(uni_name):
    if uni_name is None:
        return None
    if isinstance(uni_name,list):
        return None
    result = df.loc[df['oname'] == uni_name, 'name'].values

    # Check if result found
    if result.size > 0:
        return result[0]
    else:
        return None

if __name__ == "__main__":
    main_data = load_dataset_mie()

    for d in main_data:
        for saf in d['structural_affiliations']:
            uni = saf['university']
            formal_uni_name = find_university(uni)
            
            if formal_uni_name is not None:
                saf['universityf'] = formal_uni_name
            else:
                saf['universityf'] = None

            if uni == "University":
                saf['universityf'] = None

    ds_path = DATA_DIR / "dataset-mie.json"

    with open(ds_path, 'w', encoding="utf-8") as f:
        json.dump(main_data, f, indent=4)