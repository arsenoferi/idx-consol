# Import Libraries
import streamlit as st
import pandas as pd
import os
from Ratio.ratio import FinancialAnalyst
from Ratio.general import General
from Ratio.chart import Chart


#COMPANY

company = ""

# Set Page Configuration
st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon = os.path.join(os.getcwd(),"Asset",'Favicion.png')
)


#styling

# Function to apply color styling for comparative balance
def style_balance_changes(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return 'color: green'
        elif val < 0:
            return 'color: red'
    return ''


# Load Data
data_path = os.path.join(os.getcwd(), 'Clean', 'consol_full_data.csv')

@st.cache_data
def data_loader():
    data = pd.read_csv(data_path)
    data['Year']= pd.to_datetime(data['Date']).dt.year
    
    if company != "":
        data = data[data['Company'] == company]
        
    return data

# Dashboard Title (centered)
company_list = data_loader()['Company'].unique().tolist() 

with st.sidebar:
    #filtered Data
    st.header("Filter by Company : ")
    
    #Conditional company selection
    if company == "":
        option = st.sidebar.selectbox(
            "", company_list + ['All Companies'],index=len(company_list)
        )
    else:
        option = st.sidebar.selectbox(
            "", company_list
        )
    
    
    if option != 'All Companies':
        filtered_data = data_loader()[data_loader()['Company'] == option]
    else:
        filtered_data = data_loader()
    
    st.header("Filter by year : ")
    years = filtered_data['Year'].unique().tolist()

    #bisa all years select sorted dari terbaru ke terlama

    selected_years = st.selectbox("",
        options=['All Years'] + sorted(years, reverse=True),
        index=0
    )

    if selected_years != 'All Years':
        filtered_data = filtered_data[filtered_data['Year']<= selected_years]
    
    FinancialRatio = FinancialAnalyst(filtered_data)
    GeneralFunction = General(filtered_data)
    chart = Chart(filtered_data)

if option != 'All Companies':
    st.markdown(f"<h1 style='text-align: center;'>Financial Data Dashboard - {option}</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='text-align: center;'>Financial Data Dashboard - All Companies</h1>", unsafe_allow_html=True)

#last year in filtered data
last_year = pd.to_datetime(filtered_data['Date']).max()
last_year = last_year.date()

st.markdown(f"<h4 style='text-align: center;'>As of {last_year} (in Million)</h2><br>", unsafe_allow_html=True)


#Container 1: Financial Highlight

with st.container(border=True):
    st.markdown(f"<h2>Financial Highlight</h1><br>", unsafe_allow_html=True)
    col_1,col_2,col_3 = st.columns(3)
    
    with col_1 :
        with st.container(border=True):
            data_rev, val_terakhir, growth_terakhir = FinancialRatio.asset()
            st.metric(label="Total Asset", value=f"Rp {val_terakhir/ 1e6:,.0f} M",delta=f"{growth_terakhir:.2f}%")

    with col_2 :
        with st.container(border=True):
            data_rev, val_terakhir, growth_terakhir = FinancialRatio.liabilitas()
            st.metric(label="Total Liabilitas", value=f"Rp {val_terakhir/ 1e6:,.0f} M",delta=f"{growth_terakhir:.2f}%")

    with col_3 :
        with st.container(border=True):
            data_rev, val_terakhir, growth_terakhir = FinancialRatio.ekuitas()
            st.metric(label="Total ekuitas", value=f"Rp {val_terakhir/ 1e6:,.0f} M",delta=f"{growth_terakhir:.2f}%")

    col_4,col_5,col_6 = st.columns(3)

    with col_4 :
        with st.container(border=True):
            data_rev, val_terakhir, growth_terakhir = FinancialRatio.net_income()
            st.metric(label="Total Net Income", value=f"Rp {val_terakhir/ 1e6:,.0f} M",delta=f"{growth_terakhir:.2f}%")

    with col_5 :
        with st.container(border=True):
            data_rev, val_terakhir, growth_terakhir = FinancialRatio.revenue()
            st.metric(label="Total Revenue", value=f"Rp {val_terakhir/ 1e6:,.0f} M",delta=f"{growth_terakhir:.2f}%")

    with col_6 :
        with st.container(border=True):
            data_rev, val_terakhir, growth_terakhir = FinancialRatio.expense()
            st.metric(label="Total Expense", value=f"Rp {val_terakhir/ 1e6:,.0f} M",delta=f"{growth_terakhir:.2f}%")
    
    # buat tab untuk asset, liabilitas, ekuitas, net income, revenue, expense
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Asset", "Liabilitas", "Ekuitas", "Revenue", "Expense"])
        
    with tab1:
        # st.plotly_chart(chart.trends_chart('10','debit','Asset Trend Chart'), use_container_width=True)
        st.write(chart.trends_chart('10','debit','Asset Trend Chart'))
        asset = GeneralFunction.comparative_balance('10','debit')
        styled_balance = asset.style.map(
                style_balance_changes, 
                subset=[col for col in asset.columns if '(Δ)' in str(col)]
            )
        GeneralFunction.extends_dataframe(styled_balance)

    with tab2:
        st.write(chart.trends_chart('20','credit','Liabilitas Trend Chart'))
        liabilitas = GeneralFunction.comparative_balance('20','credit')
        styled_balance = liabilitas.style.map(
                style_balance_changes, 
                subset=[col for col in liabilitas.columns if '(Δ)' in str(col)]
            )
        GeneralFunction.extends_dataframe(styled_balance)
    
    with tab3:
        st.write(chart.trends_chart('30','credit','Ekuitas Trend Chart'))
        ekuitas = GeneralFunction.comparative_balance('30','credit')
        styled_balance = ekuitas.style.map(
                style_balance_changes, 
                subset=[col for col in ekuitas.columns if '(Δ)' in str(col)]
            )
        GeneralFunction.extends_dataframe(styled_balance)

    with tab4:
        st.write(chart.trends_chart('40','credit','Revenue Trend Chart'))
        revenue = GeneralFunction.comparative_balance('40','credit')
        styled_balance = revenue.style.map(
                style_balance_changes, 
                subset=[col for col in revenue.columns if '(Δ)' in str(col)]
            )
        GeneralFunction.extends_dataframe(styled_balance)
        
    with tab5:
        st.write(chart.trends_chart('50','debit','Expense Trend Chart'))
        expense = GeneralFunction.comparative_balance('50','debit')
        styled_balance = expense.style.map(
                style_balance_changes, 
                subset=[col for col in expense.columns if '(Δ)' in str(col)]
            )
        GeneralFunction.extends_dataframe(styled_balance)
        
# Container 2: Financial Ratio

with st.container(border=True):
    st.markdown(f"<h2>Financial Ratio</h1><br>", unsafe_allow_html=True)
    
    col_1,col_2,col_3,col_4 = st.columns(4)

    with col_1 :
        with st.container(border=True):
            st.metric(label="Current Ratio", value=f"{FinancialRatio.current_ratio()[1]:.2f} x",delta=f"{FinancialRatio.current_ratio()[2]:.2f}%")
            
    with col_2 :
        with st.container(border=True):
            st.metric(label="Debt to Equity Ratio", value=f"{FinancialRatio.debt_to_equity_ratio()[1]:.2f} x",delta=f"{FinancialRatio.debt_to_equity_ratio()[2]:.2f}%")
    
    with col_3 :
        with st.container(border=True):
            st.metric(label="Debt to Asset Ratio", value=f"{FinancialRatio.debt_to_asset_ratio()[1]:.2f} x",delta=f"{FinancialRatio.debt_to_asset_ratio()[2]:.2f}%")
    
    with col_4 :
        with st.container(border=True):
            st.metric(label="Net Profit Margin", value=f"{FinancialRatio.net_profit_margin()[1]:.2f} x",delta=f"{FinancialRatio.net_profit_margin()[2]:.2f}%")
    
    col_5,col_6,col_7,col_8 = st.columns(4)
    
    with col_5 :
        with st.container(border=True):
            st.metric(label="Return on Assets", value=f"{FinancialRatio.return_on_assets()[1]:.2f} x",delta=f"{FinancialRatio.return_on_assets()[2]:.2f}%")
            
    with col_6 :
        with st.container(border=True):
            st.metric(label="Cash Ratio", value=f"{FinancialRatio.cash_ratio()[1]:.4f} x",delta=f"{FinancialRatio.cash_ratio()[2]:.2f}%")
    
    with col_7 :
        with st.container(border=True):
            st.metric(label="Return on Equity", value=f"{FinancialRatio.return_on_equity()[1]:.2f} x",delta=f"{FinancialRatio.return_on_equity()[2]:.2f}%")
    
    with col_8 :
        with st.container(border=True):
            st.metric(label="Cost to Income Ratio", value=f"{FinancialRatio.total_expense_to_total_revenue_ratio()[1]:.2f} x",delta=f"{FinancialRatio.total_expense_to_total_revenue_ratio()[2]:.2f}%")

# Container 3: Expense to Revenue Ratio

with st.container(border=True):
    st.markdown(f"<h2>Expense to Revenue Ratio</h1><br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        df = FinancialRatio.expense_to_revenue_ratio()
        
        # Function to apply color styling
        def style_changes(val):
            if isinstance(val, str) and '%' in val:
                try:
                    num_val = float(val.replace('%', ''))
                    if num_val > 0:
                        return 'color: red'
                    elif num_val < 0:
                        return 'color: green'
                except:
                    pass
            return ''
        
        # Apply styling using pandas Styler
        styled_df = df.style.map(style_changes)
        
        st.dataframe(styled_df)
    
    #Smart Naratif
    with st.expander("Smart Naratif"):
        with st.container(border=True):
            st.markdown("#### Kas dan Setara Kas Analysis")
            text ="Kas dan setara kas per 31 December 2024 mengalami penurunan sebesar -Rp466 miliar atau sebesar -25% dibandingkan saldo periode sebelumnya. Persentase penurunan nilai akun Kas dan setara kas ini lebih kecil dibandingkan perubahan rata-rata pada tahun 2021-2023 sebesar 7% (pada tahun 2023, 2022, dan 2021 masing-masing sebesar -4%, -2%, dan 27%). Penurunan nilai akun Kas dan setara kas ini mewakili -69% dari penurunan total aset pada periode yang sama. Secara vertikal, Kas dan setara kas per 31 December 2024 memiliki porsi sebesar 13% dari total aset pada periode yang sama."
            st.write(text)
        with st.container(border=True):
            st.markdown("#### Pajak dibayar dimuka Analysis")
            text ="Pajak dibayar dimuka per 31 December 2024 mengalami peningkatan sebesar Rp19,5 miliar atau sebesar 720% dibandingkan saldo periode sebelumnya. Persentase peningkatan nilai akun Pajak dibayar dimuka ini lebih besar dibandingkan perubahan rata-rata pada tahun 2021-2023 sebesar -36% (pada tahun 2023, 2022, dan 2021 masing-masing sebesar -38%, -52%, dan -18%). Peningkatan nilai akun Pajak dibayar dimuka ini mewakili 3% dari penurunan total aset pada periode yang sama. Secara vertikal, Pajak dibayar dimuka per 31 December 2024 memiliki porsi sebesar 0% dari total aset pada periode yang sama."
            st.write(text)

        
    




