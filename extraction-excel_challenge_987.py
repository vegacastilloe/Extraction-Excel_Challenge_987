import pandas as pd
import re

df_raw = pd.read_excel(input_table, header=0, sheet_name= 'Sheet1')
df_input = df_raw['Data'].dropna(how='all').copy()

extraction_config = {
    'Code': {
        'pattern': re.compile(r'(?:INV-|ORD:|SHIP:|INV=|ORD=|SHIP=|TRX:INV-)([A-Z0-9-]+)(?:[#/|$@])'),
        'converter': lambda m: m.group(1) if m else None
    },
    'Quantity': {
        'pattern': re.compile(r'[Q#](\d+(?:\.\d+)?)'),
        'converter': lambda m: float(m.group(1)) if m else None
    },
    'Value': {
        'pattern': re.compile(r'[$V](\d+\.?\d*)'),
        'converter': lambda m: float(m.group(1)) if m else None
    },
    'Status': { # MODIFIED REGEX to be more specific (after @)
        'pattern': re.compile(r'@(ACT|PEND|CMP)'),
        'converter': lambda m: m.group(1) if m else None
    },
    'Priority': { # MODIFIED REGEX to be more specific (after #P)
        'pattern': re.compile(r'#P(\d)'),
        'converter': lambda m: int(m.group(1)) if m else None
    }
}

# Create a new DataFrame from df_input to store the extracted features
df_result = pd.DataFrame(df_input).rename(columns={'Data': 'OriginalData'})

# Apply the extraction configurations
for col_name, config in extraction_config.items():
    pattern = config['pattern']
    converter = config['converter']
    df_result[col_name] = df_result['OriginalData'].apply(lambda x: converter(pattern.search(x)))

def format_numeric_for_join(value):
    if pd.isna(value):
        return ''
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

# MODIFIED LOGIC: Combine Status and Priority directly without a hyphen between them
def combine_row_data(row):
    code = format_numeric_for_join(row['Code'])
    quantity = format_numeric_for_join(row['Quantity'])
    value = format_numeric_for_join(row['Value'])
    status = format_numeric_for_join(row['Status'])
    priority = format_numeric_for_join(row['Priority'])

    # Combine Status and Priority directly (e.g., ACT2)
    status_priority = f"{status}{priority}"

    parts = [code, quantity, value, status_priority]
    return '-'.join(parts)

df_result['CombinedExtracted'] = df_result.apply(combine_row_data, axis=1)

expected = df_raw['AnswerExpected'].dropna(how='all').copy()
print(f'Match expected: 🐍✅ #{df_result['CombinedExtracted'].equals(expected)}') #True si todo coincide ...
