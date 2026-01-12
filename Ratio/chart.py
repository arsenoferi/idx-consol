import pandas as pd
import plotly.express as px

class Chart:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def trends_chart(self, start, normal_balance='debit',judul='trend chartå'):
        data = self.data[self.data['LV 1'].str.startswith(start)].copy()
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