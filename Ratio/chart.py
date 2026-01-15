import pandas as pd
import plotly.express as px

class Chart:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def trends_chart(self, start, normal_balance='debit',judul='trend chart'):
        data = self.data[self.data['LV 1'].str.startswith(start)].copy()

        #normal balance adjustment
        if normal_balance == 'credit':
            data['Balance'] = data['Balance'] * -1
        
        # Extract year first, then aggregate by year
        data['Date'] = pd.to_datetime(data['Date']).dt.year
        trend_data = data.groupby('Date')['Balance'].sum().reset_index()
        
        # Create line chart using Plotly
        fig = px.line(trend_data, x='Date', y='Balance', title=judul, markers=True)
        fig.update_layout(xaxis_title='Date', yaxis_title='Balance')
        fig.update_xaxes(type='category', showline=True, linewidth=2, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
        
        return fig
    

    def trends_chart_multi(self, starts, judul='Trend Chart'):
        # Filter semua LV 1 yang dipilih
        data = self.data[self.data['LV 1'].str.startswith(tuple(starts))].copy()

        # Ambil kode LV 1 utama (2 digit pertama)
        data['LV 1'] = data['LV 1'].str[:2]

        # =======================
        # Sesuaikan normal balance otomatis
        # Asset = debit, Liabilities & Equity = credit
        data.loc[data['LV 1'].str.startswith('20'), 'Balance'] *= -1  # Liabilities
        data.loc[data['LV 1'].str.startswith('30'), 'Balance'] *= -1  # Equity
        data.loc[data['LV 1'].str.startswith('40'), 'Balance'] *= -1  # Revenue

        # Aggregate per tahun & LV 1
        data['Date'] = pd.to_datetime(data['Date']).dt.year

        # Mapping LV 1 utama ke nama kategori
        lv_map = {
            '10': 'Asset',
            '20': 'Liabilities',
            '30': 'Equity',
            '40': 'Revenue',
            '50': 'Expense'
        }

        # Buat kolom baru untuk label kategori
        data['Category'] = data['LV 1'].map(lv_map)
        trend_data = data.groupby(['Date','Category'], as_index=False)['Balance'].sum()

        fig = px.line(
            trend_data, 
            x='Date', 
            y='Balance', 
            color='Category',  # tiap LV 1 = 10, 20, 30 jadi garis berbeda
            title=judul,
            markers=True )

        # Styling sumbu sama seperti versi sebelumnya
        fig.update_layout(xaxis_title='Date', yaxis_title='Balance')
        fig.update_xaxes(type='category', showline=True, linewidth=2, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)


        return fig

