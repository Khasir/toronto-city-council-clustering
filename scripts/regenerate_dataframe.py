"""
Run this script to update the dataframe used by the app for councillor visualization.
See the cluster_councillors notebook for more details.
"""

import csv
import os

import pandas as pd
from tqdm.notebook import tqdm


def regenerate():
    records = sorted(os.listdir('./data/'))
    records = [os.path.join('./data/', record) for record in records if record.endswith('.csv')]

    # Read each file
    rows = {}  # Councillor[str] -> Votes[list]
    indices = {}  # Voting item[str] -> Index[int]
    next_index = 0

    # First pass: Obtain set of Agenda Items
    for filename in tqdm(records, desc='Loading Agenda Items', position=0):
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in tqdm(reader, position=1):
                assert row['Agenda Item #'], row
                if row['Agenda Item #'] not in indices:
                    indices[row['Agenda Item #']] = next_index
                    next_index += 1
    print("Found", len(indices), "unique Agenda Items.")

    # Second pass: Obtain councillor votes
    for filename in tqdm(records, desc='Loading Councillor Votes', position=0):
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in tqdm(reader, position=1):

                assert row['First Name'], row
                assert row['Last Name'], row
                assert row['Vote'], row

                name = f"{row['First Name'].strip()} {row['Last Name'].strip()}"
                index = indices[row['Agenda Item #']]

                # Merge Michelle Berardinetti into Michelle Holland
                if name == 'Michelle Berardinetti':
                    name = 'Michelle Holland'

                # Initialize councillor
                """
                Method 1:
                    Yes: 1.0
                    No: 0.0
                    Absent: -1.0
                    N/A: -1.0 (similar results with -2)

                Method 2:
                    Yes: 1.0
                    No: 0.0
                    Absent: 0.5
                    N/A: -1.0

                Method 3:
                    Yes: 1.0
                    No: 0.0
                    Absent: 0.5
                    N/A: 0.5
                """
                if name not in rows:
                    # Use -1 like 'Absent'
                    rows[name] = [-1. for __ in range(len(indices))]  # Tested with -2, and results are almost exactly the same

                # Store vote
                if row['Vote'] == 'Yes':
                    rows[name][index] = 1.
                elif row['Vote'] == 'No':
                    rows[name][index] = 0.
                elif row['Vote'] == 'Absent':
                    rows[name][index] = -1.
                else:
                    raise ValueError(f"Invalid vote type: {row['Vote']}")

    # Correct encoding issue with Ana Bailão
    rows['Ana Bailão'] = rows['Ana BailÃ£o']
    del rows['Ana BailÃ£o']

    # Convert to DataFrame
    councillor_df = pd.DataFrame(
        [rows[name] for name in rows],
        columns=[agenda_item for agenda_item in indices],
        index=[name for name in rows]
    )
    councillor_df.to_csv('./webapp/raw_councillor_df.csv')


if __name__ == "__main__":
    regenerate()
