import pandas as pd
from io import StringIO
import os
import re
class SaveToFile():
    def __init__(self):
        pass
    def save(self, text_to_save):
        cleaned_text = re.sub(r'[^a-zA-Z0-9| ]', '', text_to_save)

        df = pd.read_csv(StringIO(cleaned_text),
                         sep='|',
                         header=None,
                         names=['teamA', 'nationalityA', 'rankA', 'teamB', 'nationalityB', 'rankB', 'score', 'year'],
                         decimal=',')

        file_path = f'../SEASONS20052023.csv'
        df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)