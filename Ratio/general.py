import pandas as pd
import streamlit as st
from typing import Union

class General:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def comparative_balance(self,beg_account_code,normal_balance='debit'):
        data = self.data
        data = data[data['LV 1'].str.startswith(beg_account_code)]
        
        if normal_balance == 'credit':
            data['Balance'] = data['Balance'] * -1
        
        data = data.pivot_table(index='FSLI', columns='Date', values='Balance', aggfunc='sum')
        
        # Sort columns by date descending (newest to oldest)
        data = data.sort_index(axis=1, ascending=False)
        
        #selsish antar periode dalam bentuk decimal
        columns = data.columns.tolist()
        new_columns = []
        for i in range(len(columns)):
            new_columns.append(columns[i])
            if i < len(columns) - 1:
                # columns[i] is newer, columns[i+1] is older
                # Selisih Absolut
                abs_change_col = f"{columns[i]} (Δ Abs)"
                data[abs_change_col] = data[columns[i]] - data[columns[i+1]]
                
                # Selisih Persentase
                pct_change_col = f"{columns[i]} (Δ %)"
                data[pct_change_col] = (data[columns[i]] - data[columns[i+1]]) / data[columns[i+1]]
        
        # Reorder columns to interleave date and change columns
        final_columns = []
        for i in range(len(columns)):
            final_columns.append(columns[i])
            if i < len(columns) - 1:
                final_columns.append(f"{columns[i]} (Δ Abs)")
                final_columns.append(f"{columns[i]} (Δ %)")
        
        data = data[final_columns]
        
        # Format date columns with thousand separators, keep delta columns as decimals
        for col in data.columns:
            if '(Δ %)' in col:
                # Kalikan dengan 100 untuk konversi ke persentase
                data[col] = data[col] * 100
            elif '(Δ Abs)' in col:
                # Format value absolut dengan separator koma
                data[col] = data[col].round(0).apply(lambda x: f"{int(x):,}" if pd.notna(x) else x)
            else:
                data[col] = data[col].round(0).apply(lambda x: f"{int(x):,}" if pd.notna(x) else x)
        
        return data

    def extends_dataframe(self, df):
        # Fungsi untuk styling dataframe - hijau jika positif, merah jika negatif
        def style_balance_changes(val):
            if isinstance(val, str):
                try:
                    # Hapus komma dan konversi ke float untuk cek nilai
                    num_val = float(val.replace('%', '').replace(',', ''))
                    if num_val > 0:
                        return 'color: green'
                    elif num_val < 0:
                        return 'color: red'
                except:
                    return ''
            elif isinstance(val, (int, float)):
                if val > 0:
                    return 'color: green'
                elif val < 0:
                    return 'color: red'
            return ''
        
        # Membuat dictionary untuk column_config
        column_config = {}
        
        for col in df.columns:
            if '(Δ %)' in col:
                # Format kolom dengan (Δ %) sebagai persentase
                column_config[col] = st.column_config.NumberColumn(
                    col,
                    format="%.2f%%",
                )
        
        # Dapatkan kolom dengan delta
        delta_cols = [col for col in df.columns if '(Δ' in col]
        
        # Apply styling pada kolom dengan delta
        styled_df = df.style.applymap(style_balance_changes, subset=delta_cols)
        
        # Menampilkan dataframe dengan konfigurasi kolom dan styling
        st.dataframe(styled_df, column_config=column_config, use_container_width=True)