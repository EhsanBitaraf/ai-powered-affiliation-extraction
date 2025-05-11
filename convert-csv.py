import pandas as pd
from src.config import OUTPUT_DIR, DATA_DIR
import json


def normalized_issn(issn):
    """
    Normalizes the ISSN field by splitting it on the comma and returning a list of ISSNs.
    """
    issn_list = []
    if issn.__contains__(','):
        pass
        l = issn.split(',')
        for i in l:
            i= i.strip()
            if len(i) == 8 :
                i = i[:4] + '-' + i[-4:]
                issn_list.append(i)
            else:
                print(i)
    else:
        issn = issn.strip()
        issn = issn[:4] + '-' + issn[-4:]
        issn_list.append(issn)
    return issn_list

def read_enrichment_dataset(datast_filename):
    # Define Variable
    ds_path = DATA_DIR / datast_filename

    # Read Original dataset
    with open(ds_path, "r") as json_file:
        data = json.load(json_file)

    # data = read_repository(ds_path)
    df = pd.DataFrame(data)

    # SCIMago Data Enrichment
    scimago_df = pd.read_csv(DATA_DIR / 'scimagojr 2023.csv',
                            delimiter=";",
                            #   encoding='latin-1',
                            # encoding='utf-8'
                            )

    scimago_df['normal_issn'] = scimago_df['Issn'].apply(normalized_issn)

    # Explode the DataFrame to create new rows for each ISSN
    final_scimago_df = scimago_df.explode('normal_issn')

    # This file use for qlickview
    final_scimago_df.to_csv(DATA_DIR / 'scimagojr 2023_normal_issn.csv',)

    final_scimago_df = final_scimago_df.drop(columns=["H index", "Sourceid" ,"Type", "Issn",
                                        "SJR",
                                        "Total Docs. (2023)",
                                        "Total Docs. (3years)",
                                        "Total Refs.",
                                        "Total Cites (3years)",
                                        "Citable Docs. (3years)",
                                        "Cites / Doc. (2years)",
                                        "Ref. / Doc.",
                                        "%Female",
                                        "Overton",
                                        "SDG",
                                        "Coverage",
                                        "Categories",
                                        "Areas"  
                                        ]
                                        )

    new_df = final_scimago_df.groupby(list(final_scimago_df.columns)).size().reset_index(name='Document_Count')
    new_df = new_df.rename(columns={'Rank': 'journal_rank'})
    new_df = new_df.rename(columns={'Title': 'journal_title'})
    new_df = new_df.rename(columns={'SJR Best Quartile': 'journal_q'})
    new_df = new_df.rename(columns={'Country': 'journal_country'})
    new_df = new_df.rename(columns={'Region': 'journal_region'})
    new_df = new_df.rename(columns={'Publisher': 'journal_publisher'})
    new_df = new_df.drop(columns=[ "Document_Count"])


    df = pd.merge(df, new_df, left_on='journal_issn', right_on='normal_issn', how='left')

    return df

def detect_field_types(df):
    main_fields = []
    one_to_many_fields = []

    for column in df.columns:
        if df[column].apply(lambda x: isinstance(x, list)).all():
            one_to_many_fields.append(column)
        else:
            main_fields.append(column)

    return main_fields, one_to_many_fields

df = read_enrichment_dataset("dataset-mie.json")
main_fields, one_to_many_fields = detect_field_types(df)
df = df.reset_index(drop=True)

print("These are is main fields:")
print(main_fields)

print("These are one to many fields:")
print(one_to_many_fields)

# Create main CSV with explicit ID column
main_df = df[main_fields].copy()
main_df.insert(0, 'id', main_df.index)
main_df.to_csv('main.csv', index=False)
print("-- main.csv saved.")

# Create separate CSV files for one-to-many fields
for field in one_to_many_fields:
    rows = []
    for index, row in df.iterrows():
        for item in row[field]:
            rows.append({'id': index, field: item})
    pd.DataFrame(rows).to_csv(f'main_{field}.csv', index=False)
    print(f"-- main_{field}.csv saved.")

