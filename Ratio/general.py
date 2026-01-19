import pandas as pd
import streamlit as st
from typing import Union

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import JsCode

class General:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def comparative_balance(self,beg_account_code,normal_balance='debit'):
        data = self.data
        data = data[data['LV 1'].str.startswith(beg_account_code)]
        
        if normal_balance == 'credit':
            data['Balance'] = data['Balance'] * -1
        
        data = data.pivot_table(
            index='FSLI', 
            columns='Date', 
            values='Balance', 
            aggfunc='sum'
        )

        # Sort columns by date descending (newest to oldest)
        data = data.sort_index(axis=1, ascending=False)
        
        # Convert column names to datetime
        data.columns = pd.to_datetime(data.columns)        
        columns = list(data.columns)

        #selsish antar periode dalam bentuk decimal
        for i in range(len(columns)):
            if i < len(columns) - 1:
                # columns[i] is newer, columns[i+1] is older
                label = columns[i].strftime("%B %Y")

                # Selisih Absolut
                abs_change_col = f"{label} (Δ Abs)"
                data[abs_change_col] = data[columns[i]] - data[columns[i+1]]
                
                # Selisih Persentase
                pct_change_col = f"{label} (Δ %)"
                data[pct_change_col] = (data[columns[i]] - data[columns[i+1]]) / data[columns[i+1]]
        
        # Reorder columns to interleave date and change columns
        final_columns = []
        for i in range(len(columns)):
            final_columns.append(columns[i])
            if i < len(columns) - 1:
                label = columns[i].strftime("%B %Y")
                final_columns.append(f"{label} (Δ Abs)")
                final_columns.append(f"{label} (Δ %)")

        data = data[final_columns]
        
        # Format date columns with thousand separators, keep delta columns as decimals
        for col in data.columns:
            if isinstance(col, str) and'(Δ %)' in col:
                # Kalikan dengan 100 untuk konversi ke persentase
                data[col] = data[col] * 100
            elif isinstance(col, str) and '(Δ Abs)' in col:
                # Format value absolut dengan separator koma
                data[col] = data[col].round(0)
            else:
                data[col] = data[col].round(0)

        # ===== Format Date di Header Table =====
        data = data.rename(
            columns=lambda c: c.strftime("%B %Y") if isinstance(c, pd.Timestamp) else c
        )

        return data

    def extends_dataframe(self, df):

        df = df.reset_index()

        # Hitung panjang text kolom FSLI
        if 'FSLI' in df.columns:
            max_len = df['FSLI'].astype(str).map(len).max()
            width = max(100, min(max_len * 10, 400))  # perkiraan 10 px per karakter
        else:
            width = 120

        gb = GridOptionsBuilder.from_dataframe(df)

        # Default column behaviour
        gb.configure_default_column(
            sortable=True,
            filter=True,
            resizable=True,
            width=120,
            cellStyle={"textAlign": "right"},
            flex=1,
        )

        # ===== JS FORMATTER =====

        # Indonesia Currency
        id_number_formatter = JsCode("""
            function(params) {
                if (params.value === null || params.value === undefined) return '';
                return params.value.toLocaleString('id-ID');
            }
        """)

        # US percent: 12.34%
        id_percent_formatter = JsCode("""
            function(params) {
                if (params.value === null || params.value === undefined) return '';
                return params.value.toLocaleString(
                    'us-US',
                    {minimumFractionDigits: 2, maximumFractionDigits: 2}
                ) + '%';
            }
        """)

        # Delta Color Styling
        delta_color = JsCode("""
            function(params) {
                if (params.value > 0) {
                    return {color: 'green'};
                }
                if (params.value < 0) {
                    return {color: 'red'};
                }
            }
        """)

        # ===== COLUMN CONFIG =====
        for col in df.columns:
            if isinstance(col, str) and '(Δ %)' in col:
                gb.configure_column(
                    col,
                    type=["numericColumn"],
                    valueFormatter=id_percent_formatter,
                    cellStyle=delta_color,
                )

            elif isinstance(col, str) and '(Δ Abs)' in col:
                gb.configure_column(
                    col,
                    type=["numericColumn"],
                    valueFormatter=id_number_formatter,
                    cellStyle=delta_color,
                )

            elif col != 'FSLI':
                gb.configure_column(
                    col,
                    type=["numericColumn"],
                    valueFormatter=id_number_formatter,
                )

            else:
                gb.configure_column(
                    col,
                    pinned="left",
                    width=width,
                    cellStyle={"textAlign": "left"},
                    flex=0,
                )

        grid_options = gb.build()

        # ===== AUTO SIZE JS =====
        #auto_size_js = JsCode("""
        #    function(params) {
        #        params.columnApi.autoSizeColumns(['FSLI']);  // kolom yang ingin auto-fit
        #    }
        #""")

        AgGrid(
            df,
            gridOptions=grid_options,
            fit_columns_on_grid_load=True,
            height=450,
            width='100%',
            allow_unsafe_jscode=True,
            theme="alpine",
            #custom_js=auto_size_js,
            custom_css={
                ".ag-header-cell-label": {
                    "font-weight": "normal"
                }
            }
        )
