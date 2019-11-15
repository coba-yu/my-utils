import numpy as np
import pandas as pd
from tqdm import tqdm

def process(df: pd.DataFrame, unique_columns: list, ym_column: str, var_column: str,
            n_later: int, n_ago: int):
    df_new = df.sort_values([*unique_columns, ym_column])

    n_unique_columns = len(unique_columns)
    if n_unique_columns == 2:
        uc0_array = df_new[unique_columns[0]].values
        uc0_unique = df_new[unique_columns[0]].unique()
        df_uc0_list = []
        for uc0 in tqdm(uc0_unique, desc='Processing Features'):
            df_uc0 = df_new[uc0_array == uc0]
            uc1_array = df_uc0[unique_columns[1]].values
            uc1_unique = df_uc0[unique_columns[1]].unique()

            col = f'{var_column}_{n_later}M_Later'
            df_uc0[col] = pd.concat([df_uc0.loc[uc1_array == uc1, var_column].shift(-n_later) for uc1 in uc1_unique])

            # Ago
            for i in range(1, n_ago + 1):
                col = f'{var_column}_{i}M_Ago'
                df_uc0[col] = pd.concat([df_uc0.loc[uc1_array == uc1, var_column].shift(i) for uc1 in uc1_unique])

            # Statistics
            for i in range(2, n_ago + 1):
                rollings = [df_uc0.loc[uc1_array == uc1, var_column].rolling(i) for uc1 in uc1_unique]
                col = f'{var_column}_{i}M_Mean'
                df_uc0[col] = pd.concat(list(map(lambda x: x.mean(), rollings)))
                col = f'{var_column}_{i}M_Std'
                df_uc0[col] = pd.concat(list(map(lambda x: x.std(), rollings)))
                col = f'{var_column}_{i}M_Median'
                df_uc0[col] = pd.concat(list(map(lambda x: x.median(), rollings)))
                col = f'{var_column}_{i}M_Max'
                df_uc0[col] = pd.concat(list(map(lambda x: x.max(), rollings)))
                col = f'{var_column}_{i}M_Min'
                df_uc0[col] = pd.concat(list(map(lambda x: x.min(), rollings)))

            # Cumulative Sum
            col = f'{var_column}_Cumsum'
            df_uc0[col] = pd.concat([df_uc0.loc[uc1_array == uc1, var_column].cumsum() for uc1 in uc1_unique])

            df_uc0_list.append(df_uc0)
        df_new = pd.concat(df_uc0_list)

    # Sin Cos
    def month(s):
        s = s.replace('-', '')
        return int(s[4:6])
    df_new = df_new.assign(Month=df_new.Date.map(month))

    x = np.arange(1, 13)
    sin_dic = {y: np.sin(2 * np.pi * y / x.max()) for y in x}
    cos_dic = {y: np.cos(2 * np.pi * y / x.max()) for y in x}
    df_new['Month_Sin'] = list(map(lambda x: sin_dic[x], df_new.Month.values))
    df_new['Month_Cos'] = list(map(lambda x: cos_dic[x], df_new.Month.values))

    return df_new
