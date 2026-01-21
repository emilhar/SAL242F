import pandas as pd
import json
import pprint

fp = 'data/openalex_works.csv'
print('Loading', fp)
df = pd.read_csv(fp, low_memory=False)
print('Loaded shape:', df.shape)

if 'authorships' not in df.columns:
    print('No `authorships` column found in CSV')
else:
    sample = df['authorships'].head(50)
    nonnull = sample.dropna()
    print('Sample size (first 50), non-null count:', len(sample), len(nonnull))
    for i, val in enumerate(sample):
        print('\n--- row', i, 'type:', type(val))
        if pd.isna(val):
            print('  <NA>')
            continue
        s = val
        if isinstance(s, str):
            print('  repr[:200]:', repr(s)[:200])
            try:
                parsed = json.loads(s)
                print('  -> parsed type:', type(parsed))
                if isinstance(parsed, list):
                    print('  -> list len', len(parsed))
                    pprint.pprint(parsed[:2])
                elif isinstance(parsed, dict):
                    pprint.pprint(list(parsed.items())[:5])
            except Exception as e:
                print('  -> not JSON:', e)
        else:
            print('  value (non-str):', type(s))
            pprint.pprint(s)

    # Count institution-containing patterns in first 200 non-null entries
    inst_found = 0
    for v in df['authorships'].dropna().head(200):
        try:
            x = json.loads(v) if isinstance(v, str) else v
        except Exception:
            x = v
        if isinstance(x, list):
            for a in x:
                if isinstance(a, dict) and ('institutions' in a or 'institution' in a):
                    inst_found += 1
                    break
        elif isinstance(x, dict) and ('institutions' in x or 'institution' in x):
            inst_found += 1
    print('\nRows with institution structures (in first 200 non-null authorships):', inst_found)
