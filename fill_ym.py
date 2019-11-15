import pandas as pd
from tqdm import tqdm


def fill_ym_pandas(df: pd.DataFrame, unique_columns: list, ym_column: str, fill_value={}) -> pd.DataFrame:
    df_new = df.sort_values([*unique_columns, ym_column])
    df_new[ym_column] = pd.to_datetime(df_new[ym_column])
    df_new.set_index(ym_column, inplace=True)
    flag_column = 'Filled'
    df_new[flag_column] = 0
    fill_value[flag_column] = 1

    n_unique_columns = len(unique_columns)
    if n_unique_columns == 2:
        uc0_array = df_new[unique_columns[0]].values
        uc0_unique = df_new[unique_columns[0]].unique()
        df_list = []
        for uc0 in tqdm(uc0_unique):
            df_uc0 = df_new[uc0_array == uc0]
            uc1_array = df_uc0[unique_columns[1]].values
            uc1_unique = df_uc0[unique_columns[1]].unique()
            df_list.append(pd.concat([df_uc0[uc1_array == uc1].asfreq('MS') for uc1 in uc1_unique]))
        df_new = pd.concat(df_list)
        df_new.fillna(fill_value, inplace=True)
        df_new[unique_columns] = df_new[unique_columns].fillna(method='ffill')
        df_new = df_new.astype({'Filled': int})
        df_new.reset_index(inplace=True)
        df_new[ym_column] = df_new[ym_column].map(lambda x: '-'.join(str(x).split('-')[:2]))

    else:
        raise NotImplementedError

    return df_new


def fill_ym_numpy(df: pd.DataFrame, unique_columns: list, ym_column: str, fill_value=None) -> pd.DataFrame:
    raise NotImplementedError


def fill_ym(df: pd.DataFrame, unique_columns: list, ym_column: str, base: str, fill_value=None) -> pd.DataFrame:
    if base == 'pandas':
        df_new = fill_ym_pandas(df, ['idx', 'area'], 'ym', fill_value)
    elif base == 'numpy':
        df_new = fill_ym_numpy(df, ['idx', 'area'], 'ym', fill_value)
    else:
        raise NotImplementedError

    return df_new


if __name__ == '__main__':
    idx = [0, 0, 0,
           0, 0, 0,
           1, 1, 1]
    area = ['Tokyo', 'Tokyo', 'Tokyo',
            'Osaka', 'Osaka', 'Osaka',
            'Nagasaki', 'Nagasaki', 'Nagasaki']
    ym = ['2019-01', '2019-04', '2019-10',
          '2019-02', '2019-05', '2019-9',
          '2018-02', '2018-05', '2019-04']
    data = ['_'.join([str(i), a, y]) for i, a, y in zip(idx, area, ym)]

    df = pd.DataFrame(dict(idx=idx, area=area, ym=ym, data=data))
    print(df)
    print(fill_ym(df, ['idx', 'area'], 'ym', 'pandas', {'data': 0}))
