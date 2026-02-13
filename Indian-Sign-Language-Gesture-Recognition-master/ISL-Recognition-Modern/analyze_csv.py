import pandas as pd
import numpy as np

try:
    df = pd.read_csv('../ISL_Translator-main/model/keypoint_classifier/keypoint.csv')
    print("Columns:", df.columns)
    
    # Extract numeric data (skipping label)
    # The first row in the output above shows 'label' then x1...x21, y1...y21?
    # Wait, the header says x1...x21, y1...y21? No, it says x1,x2...x21,y1...y21
    # But the values are interleaved in the code: pts.extend([x, y])
    # Let's check the values.
    # 144,470, 170,457...
    # x=144, y=470?
    
    # Let's see the max values to guess resolution
    # We need to parse the CSV properly.
    
    # The header in the `head` output seems to be: label, x1...x21, y1...y21?
    # Wait, the header has 43 columns (label + 42 coords).
    # But the code `pts.extend([x, y])` produces x1, y1, x2, y2...
    # The CSV header in the `head` output might be misleading or I misread it.
    # Let's check the first few values.
    
    values = df.iloc[:, 1:].values.flatten()
    print(f"Max value: {values.max()}")
    print(f"Min value: {values.min()}")
    
except Exception as e:
    print(e)
