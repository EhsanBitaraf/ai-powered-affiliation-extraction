import json
from src.affiliation import parse_affiliation
from src.dataset import load_dataset_mie
from src.config import OUTPUT_DIR, DATA_DIR

def simple_export():
    data = load_dataset_mie()
    n = 0 
    limit = 0

    print(f"{len(data)} Records found")

    row = ""
    for d in data:
        if limit !=0:
            if n > limit:
                break
        if 'structural_affiliations' in d:
            n = n + 1
            for sa in d['structural_affiliations']:
                if 'universityf' in sa:
                    if sa['universityf'] is None:
                        unif = sa['university']
                    else:
                        unif = sa['universityf']
                else:
                    unif = sa['university']
                row = row + f"{d['pmid']},{sa['country']},\"{sa['institute']}\",\"{sa['department']}\",\"{sa['university']}\",\"{sa['city']}\",\"{unif}\",{sa['Status']}" + "\n"
            
    with open("co.csv", 'w', encoding="utf-8") as f:
        f.write(row)