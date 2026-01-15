import pandas as pd

class FinancialAnalyst:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def data_summary(self):
        return self.data.describe()
    
    def pivot_data(self,based_index):
        return self.data.pivot_table(index=based_index, columns='Date', values='Balance', aggfunc='sum')
    
    def asset(self):
        asset = self.data
        asset['LV 1'] = asset['LV 1'].astype(str)
        asset = asset[asset['LV 1'].str.startswith("10")]
        asset['Date'] = pd.to_datetime(asset['Date'])
        asset = asset.pivot_table(index='Date', values='Balance', aggfunc='sum')
        asset = asset.sort_values(by='Date',ascending=True)
        
        #kalkulasi
        asset['Growth (%)'] = asset['Balance'].pct_change() * 100
        last_valid_value = asset['Balance'].dropna().iloc[-1]
        last_valid_growth = asset['Growth (%)'].iloc[-1]
        return [asset,last_valid_value,last_valid_growth]
    
    def liabilitas(self):
        liabilitas = self.data
        liabilitas['LV 1'] = liabilitas['LV 1'].astype(str)
        liabilitas = liabilitas[liabilitas['LV 1'].str.startswith("20")]
        liabilitas['Date'] = pd.to_datetime(liabilitas['Date'])
        liabilitas = liabilitas.pivot_table(index='Date', values='Balance', aggfunc='sum')
        liabilitas = liabilitas.sort_values(by='Date',ascending=True)
        liabilitas = liabilitas * -1
        
        #kalkulasi
        liabilitas['Growth (%)'] = liabilitas['Balance'].pct_change() * 100
        last_valid_value = liabilitas['Balance'].dropna().iloc[-1]
        last_valid_growth = liabilitas['Growth (%)'].iloc[-1]
        return [liabilitas,last_valid_value,last_valid_growth]
    
    def ekuitas(self):
        ekuitas = self.data
        ekuitas['LV 1'] = ekuitas['LV 1'].astype(str)
        ekuitas = ekuitas[ekuitas['LV 1'].str.startswith("30")]
        ekuitas['Date'] = pd.to_datetime(ekuitas['Date'])
        ekuitas = ekuitas.pivot_table(index='Date', values='Balance', aggfunc='sum')
        ekuitas = ekuitas.sort_values(by='Date',ascending=True)
        ekuitas = ekuitas * -1
        
        #kalkulasi
        ekuitas['Growth (%)'] = ekuitas['Balance'].pct_change() * 100
        last_valid_value = ekuitas['Balance'].dropna().iloc[-1]
        last_valid_growth = ekuitas['Growth (%)'].iloc[-1]
        return [ekuitas,last_valid_value,last_valid_growth]
    
    def revenue(self):
        revenue = self.data
        revenue['LV 1'] = revenue['LV 1'].astype(str)
        revenue = revenue[revenue['LV 1'].str.startswith("40")]
        revenue['Date'] = pd.to_datetime(revenue['Date'])
        revenue = revenue.pivot_table(index='Date', values='Balance', aggfunc='sum')
        revenue = revenue.sort_values(by='Date',ascending=True)
        revenue = revenue*-1
        # hitung kenaikan 
        revenue['Growth (%)'] = revenue['Balance'].pct_change() * 100
        last_valid_value = revenue['Balance'].dropna().iloc[-1]
        last_valid_growth = revenue['Growth (%)'].iloc[-1]
        return [revenue,last_valid_value,last_valid_growth]

    def expense(self):
        expense = self.data
        expense['LV 1'] = expense['LV 1'].astype(str)
        expense = expense[(expense['LV 1'].str.startswith("50"))|(expense['LV 1'].str.startswith("60"))]
        expense['Date'] = pd.to_datetime(expense['Date'])
        expense = expense.pivot_table(index='Date', values='Balance', aggfunc='sum')
        expense = expense.sort_values(by='Date',ascending=True)
        # hitung kenaikan 
        expense['Growth (%)'] = expense['Balance'].pct_change() * 100
        last_valid_value = expense['Balance'].dropna().iloc[-1]
        last_valid_growth = expense['Growth (%)'].iloc[-1]
        return [expense,last_valid_value,last_valid_growth]
    
    def net_income(self):
        NetIncome = self.data
        NetIncome['LV 1'] = NetIncome['LV 1'].astype(str)
        NetIncome = NetIncome[(NetIncome['LV 1'].str.startswith("40"))|(NetIncome['LV 1'].str.startswith("50"))|(NetIncome['LV 1'].str.startswith("60"))]
        NetIncome['Date'] = pd.to_datetime(NetIncome['Date'])
        NetIncome = NetIncome.pivot_table(index='Date', values='Balance', aggfunc='sum')
        NetIncome = NetIncome.sort_values(by='Date',ascending=True)
        NetIncome = NetIncome*-1
        # hitung kenaikan 
        NetIncome['Growth (%)'] = NetIncome['Balance'].pct_change() * 100
        last_valid_value = NetIncome['Balance'].dropna().iloc[-1]
        last_valid_growth = NetIncome['Growth (%)'].iloc[-1]
        return [NetIncome,last_valid_value,last_valid_growth]

    def debt_to_equity_ratio(self):
        debt = self.liabilitas()[0]
        debt = debt.rename(columns={'Balance':'Liabilitas'})
        debt = debt[['Liabilitas']]
        
        equity = self.ekuitas()[0]
        equity = equity.rename(columns={'Balance':'Ekuitas'})
        equity = equity[['Ekuitas']]
        
        debt_equity = debt.join(equity, how='inner')
        debt_equity['Debt to Equity Ratio'] = debt_equity['Liabilitas'] / debt_equity['Ekuitas']
        last_valid_value = debt_equity['Debt to Equity Ratio'].dropna().iloc[-1]
        
        #last growth debt to equity
        debt_equity['Growth (%)'] = debt_equity['Debt to Equity Ratio'].pct_change() * 100
        last_valid_growth = debt_equity['Growth (%)'].iloc[-1]
        
        return debt_equity,last_valid_value,last_valid_growth
    
    def debt_to_asset_ratio(self):
        debt = self.liabilitas()[0]
        debt = debt.rename(columns={'Balance':'Liabilitas'})
        debt = debt[['Liabilitas']]
        
        asset = self.asset()[0]
        asset = asset.rename(columns={'Balance':'Aset'})
        asset = asset[['Aset']]
        
        debt_asset = debt.join(asset, how='inner')
        debt_asset['Debt to Asset Ratio'] = debt_asset['Liabilitas'] / debt_asset['Aset']
        last_valid_value = debt_asset['Debt to Asset Ratio'].dropna().iloc[-1]
        
        #last growth debt to asset
        debt_asset['Growth (%)'] = debt_asset['Debt to Asset Ratio'].pct_change() * 100
        last_valid_growth = debt_asset['Growth (%)'].iloc[-1]
        
        return debt_asset,last_valid_value,last_valid_growth
    
    def current_ratio(self):
        current_data = self.data
        current_data = current_data[current_data['Header'].isin(['Aset Lancar','Liabilitas Jangka Pendek'])]
        current_data = current_data.pivot_table(index=['Date'], columns='Header', values='Balance', aggfunc='sum')
        current_data['Liabilitas Jangka Pendek'] = current_data['Liabilitas Jangka Pendek'] * -1
        current_data['Current Ratio'] = current_data['Aset Lancar'] / current_data['Liabilitas Jangka Pendek']
        last_valid_value = current_data['Current Ratio'].dropna().iloc[-1]
        
        #last growth current ratio
        current_data['Growth (%)'] = current_data['Current Ratio'].pct_change() * 100
        last_valid_growth = current_data['Growth (%)'].iloc[-1]
        
        return current_data,last_valid_value,last_valid_growth
    
    def net_profit_margin(self):
        net_income = self.data
        net_income = net_income[(net_income['LV 1'].str.startswith("40"))|(net_income['LV 1'].str.startswith("50"))|(net_income['LV 1'].str.startswith("60"))]
        net_income = net_income.pivot_table(index='Date', values='Balance', aggfunc='sum') * -1
        
        revenue = self.data
        revenue = revenue[revenue['LV 1'].str.startswith("40")]
        revenue = revenue.pivot_table(index='Date', values='Balance', aggfunc='sum') * -1
        
        net_profit_margin = net_income.join(revenue, lsuffix='_net_income', rsuffix='_revenue')
        rename_dict = {'Balance_net_income': 'Net Income', 'Balance_revenue': 'Revenue'}
        net_profit_margin = net_profit_margin.rename(columns=rename_dict)
        net_profit_margin['npm (%)'] = net_profit_margin['Net Income'] / net_profit_margin['Revenue']
        last_valid_value = net_profit_margin['npm (%)'].dropna().iloc[-1]
        
        #last growth net profit margin
        net_profit_margin['Growth (%)'] = net_profit_margin['npm (%)'].pct_change() * 100
        last_valid_growth = net_profit_margin['Growth (%)'].iloc[-1]
        
        return net_profit_margin,last_valid_value,last_valid_growth
    
    def return_on_assets(self):
        asset = self.asset()[0]
        asset = asset.rename(columns={'Balance':'Aset'})
        asset = asset[['Aset']]

        net_income = self.net_income()[0]
        net_income = net_income.rename(columns={'Balance':'Net Income'})
        net_income = net_income[['Net Income']]

        return_on_assets = net_income.join(asset, how='inner')
        return_on_assets['Return on Assets'] = return_on_assets['Net Income'] / return_on_assets['Aset']
        last_valid_value = return_on_assets['Return on Assets'].dropna().iloc[-1]

        #last growth return on assets
        return_on_assets['Growth (%)'] = return_on_assets['Return on Assets'].pct_change() * 100
        last_valid_growth = return_on_assets['Growth (%)'].iloc[-1]
        
        return return_on_assets,last_valid_value,last_valid_growth
    
    def return_on_equity(self):
        net_income = self.net_income()[0]
        net_income = net_income.rename(columns={'Balance':'Net Income'})
        net_income = net_income[['Net Income']]

        ekuitas = self.ekuitas()[0]
        ekuitas = ekuitas.rename(columns={'Balance':'Ekuitas'})
        ekuitas = ekuitas[['Ekuitas']]

        roe = net_income.join(ekuitas, how='inner')
        roe['Return on Equity'] = roe['Net Income'] / roe['Ekuitas']
        last_valid_value = roe['Return on Equity'].dropna().iloc[-1]
        
        #last growth return on equity
        roe['Growth (%)'] = roe['Return on Equity'].pct_change() * 100
        last_valid_growth = roe['Growth (%)'].iloc[-1]
        return roe,last_valid_value,last_valid_growth
    
    def cash_ratio(self):
        cash_data = self.data
        cash_data = cash_data[cash_data['FSLI']=='Kas Setara kas']
        cash_data = cash_data.pivot_table(index='Date', values='Balance', aggfunc='sum')
        
        liabilitas_data = self.data
        liabilitas_data = liabilitas_data[liabilitas_data['Header']=='Liabilitas Jangka Pendek']
        liabilitas_data = liabilitas_data.pivot_table(index='Date', values='Balance', aggfunc='sum')
        
        cash_ratio = cash_data.join(liabilitas_data, lsuffix='_cash', rsuffix='_liabilitas')
        cash_ratio['Cash Ratio'] = cash_ratio['Balance_cash'] / cash_ratio['Balance_liabilitas']
        cash_ratio['Cash Ratio'] = cash_ratio['Cash Ratio']*-1
        last_valid_value = cash_ratio['Cash Ratio'].dropna().iloc[-1]

        #last growth cash ratio
        cash_ratio['Growth (%)'] = cash_ratio['Cash Ratio'].pct_change() * 100
        last_valid_growth = cash_ratio['Growth (%)'].iloc[-1]

        return cash_ratio,last_valid_value,last_valid_growth
    
    def total_expense_to_total_revenue_ratio(self):
        revenue = self.data
        revenue = revenue[revenue['LV 1'].str.startswith("40")]
        revenue = revenue.pivot_table(index='Date', values='Balance', aggfunc='sum') * -1
        
        expense = self.data
        expense = expense[(expense['LV 1'].str.startswith("50"))|(expense['LV 1'].str.startswith("60"))]
        expense = expense.pivot_table(index='Date', values='Balance', aggfunc='sum')
        
        ratio = expense.join(revenue, lsuffix='_expense', rsuffix='_revenue')
        ratio['Expense to Revenue Ratio'] = ratio['Balance_expense'] / ratio['Balance_revenue']
        last_valid_value = ratio['Expense to Revenue Ratio'].dropna().iloc[-1]
        
        #last growth expense to revenue ratio
        ratio['Growth (%)'] = ratio['Expense to Revenue Ratio'].pct_change() * 100
        last_valid_growth = ratio['Growth (%)'].iloc[-1]
        
        return ratio,last_valid_value,last_valid_growth

    def expense_to_revenue_ratio(self):
        expense = self.data
        expense = expense[(expense['LV 1'].str.startswith("50"))|(expense['LV 1'].str.startswith("60"))]
        expense = expense.pivot_table(index=['FSLI','Date'], values='Balance', aggfunc='sum')
        
        revenue = self.data
        revenue = revenue[revenue['LV 1'].str.startswith("40")]
        revenue = revenue.pivot_table(index='Date', values='Balance', aggfunc='sum') * -1
        
        
        ratio = expense.join(revenue, on='Date', how='inner', lsuffix='_expense', rsuffix='_revenue')
        ratio['Expense to Revenue Ratio'] = ratio['Balance_expense'] / ratio['Balance_revenue']
            
        ratio = ratio.reset_index()
        revenue = ratio.pivot_table(index='FSLI', columns='Date', values='Expense to Revenue Ratio')
        
        # Sort columns by date descending (newest to oldest)
        revenue = revenue.sort_index(axis=1, ascending=False)
        
        # Pastikan kolom datetime
        revenue.columns = pd.to_datetime(revenue.columns)

        # Add change columns between periods
        columns = revenue.columns.tolist()
        label_map = {}
        new_columns = []
        for i in range(len(columns)):
            new_columns.append(columns[i])
            if i < len(columns) - 1:
                # columns[i] is newer, columns[i+1] is older
                change_col = f"{columns[i+1].strftime('%B %Y')} (Δ)"
                label_map[columns[i+1]] = change_col

                revenue[change_col] = (revenue[columns[i]] - revenue[columns[i+1]]) * 100
        
        # Reorder columns to interleave date and change columns
        final_columns = []
        for i in range(len(columns)):
            final_columns.append(columns[i])
            if i < len(columns) - 1:
                final_columns.append(label_map[columns[i+1]])
        
        revenue = revenue[final_columns]
        
        # Format values - convert to percentage for all columns
        for col in revenue.columns:
            if "(Δ)" in str(col):
                revenue[col] = revenue[col].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else x)
            else:
                revenue[col] = revenue[col].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else x)

        # ===== Format Date di Header Table =====
        revenue = revenue.rename(
            columns=lambda c: c.strftime("%B %Y") if isinstance(c, pd.Timestamp) else c
        )
        
        return revenue
        