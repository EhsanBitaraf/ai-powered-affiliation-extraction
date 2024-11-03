import json
from src.affiliation import parse_affiliation
from src.dataset import load_dataset_mie
from src.config import OUTPUT_DIR, DATA_DIR


def run_llm_pipeline(limit = 0):
    """
    This Python function processes a dataset by adding structural dependencies 
    by asking LLM based on the dependencies in the data.

    
    :param limit: The `limit` parameter in the `run_llm_pipeline` function is used to specify the
    maximum number of records to process before stopping and saving the data to a file. If `limit` is
    set to a positive integer value, the function will process up to that number of records and then
    save, defaults to 0 (optional)
    """

    ds_path = DATA_DIR / "dataset-mie.json"

    data = load_dataset_mie()
    n = 0 
    

    print(f"{len(data)} Records found")
    for d in data:
        if limit !=0:
            if n > limit:
                with open(ds_path, 'w', encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                break
        if 'structural_affiliations' in d:
            # For this record, it has already been done, no special action is required
            pass
        else:
            n = n + 1
            if 'affiliations' in  d:
                structural_affiliations = []
                for affiliation in d['affiliations']:
                    print(f"({n}) {affiliation}")
                    r = parse_affiliation(affiliation)
                    structural_affiliations.append(r)
                d['structural_affiliations'] = structural_affiliations

    if limit == 0:
        with open(ds_path, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)
