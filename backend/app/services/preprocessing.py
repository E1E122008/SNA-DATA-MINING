import pandas as pd
from io import StringIO

def handle_upload(file, columns):
    content = file.file.read().decode('utf-8')
    if file.filename.endswith('.csv'):
        df = pd.read_csv(StringIO(content))
    elif file.filename.endswith('.json'):
        df = pd.read_json(StringIO(content))
    else:
        raise ValueError("Unsupported file type")
    selected_cols = [col.strip() for col in columns.split(',')]
    df = df[selected_cols]
    df = df.drop_duplicates().dropna()
    for col in df.columns:
        if col.lower() in ['hashtags', 'mentions', 'tagged_users']:
            df[col] = df[col].apply(lambda x: [u.strip() for u in str(x).split(';')] if isinstance(x, str) and x else [])
    # Pastikan kolom likes numerik
    if 'likes' in df.columns:
        df['likes'] = pd.to_numeric(df['likes'], errors='coerce')
    df.columns = [c.lower() for c in df.columns]
    return df 