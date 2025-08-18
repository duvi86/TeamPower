import pandas as pd
import numpy as np

def get_dummy_data():
    np.random.seed(42)
    months = pd.date_range('2025-01-01', periods=8, freq='M')
    df = pd.DataFrame({
        'Date': np.random.choice(months, 50),
        'Cost Center Project': np.random.choice(['CCP1', 'CCP2', 'CCP3'], 50),
        'Cost Center SOW': np.random.choice(['CCS1', 'CCS2'], 50),
        'SOW Number': np.random.randint(1000, 1100, 50),
        'PO': np.random.randint(2000, 2100, 50),
        'Amount': np.random.randint(1000, 10000, 50),
        'Category': np.random.choice(['Budget', 'Planned', 'Consumed'], 50),
        'Type': np.random.choice(['OPEX', 'CAPEX'], 50)
    })
    return df
