# Import Libraries
import streamlit as st
import pandas as pd
import os
from Ratio.ratio import FinancialAnalyst
from Ratio.general import General
from Ratio.chart import Chart


#COMPANY

company = ""

# Set Page Configuration & Design
st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    #initial_sidebar_state="expanded",
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

#Load CSS
def load_css(path):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("asset/style.css")

#Container 1: Financial Overview As of 2023-12-31

# START Container Main Filter
filtered_data = data_loader()
with st.container(border=True, key="filter-style"):
    col_logo,col_bursa= st.columns([1,15], gap="small")
    with col_logo:
        st.image("Asset/Favicion.png", width=50)
    with col_bursa:
        st.markdown(
            "<h2 style='margin:0; text-align:left;'>Financial Dashboard<br></h2>",
            unsafe_allow_html=True
        )
    col_title, col1, col2 = st.columns([0.4, 2, 2])

    # ---- Main Filter text ----
    with col_title:
        st.markdown(
            "<div class='filter-title'>Main Filter:</div>",
            unsafe_allow_html=True
        )

    # ---- Company filter ----
    with col1:
        company_list = data_loader()['Company'].unique().tolist() 
        option = st.selectbox(
            "Companies",
            ["All Companies"] + sorted(company_list,reverse=True),
            label_visibility="collapsed"
        )

        # Apply company filter
        if option != "All Companies":
            filtered_data = data_loader()[data_loader()["Company"] == option]

    # ---- Year filter ----
    with col2:
        years = filtered_data["Year"].unique().tolist()
        selected_years = st.selectbox(
            "Year",
            ["All Years"] + sorted(years, reverse=True),
            label_visibility="collapsed"
        )

# END Container Main Filter

st.markdown("<div id='main-filter-card'>", unsafe_allow_html=True)
with st.container(border=True,key='main-financial-overview'):

    # Title Container 1
    last_year = pd.to_datetime(filtered_data['Date']).max()
    last_year = last_year.date()

    # Format Date to "Month Year"
    formatted_date = last_year.strftime("%B %Y") 

    # Dynamic description text based on company filter

    # Dynamic company text for description
    if option == "All Companies":
            company_text = "across all companies"
    else:
            company_text = f"in {option}"
   
    st.markdown(f"<h1 style='text-align: center;'>Financial Overview As of {formatted_date}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; font-style: italic; text-align: center;'>This dashboard provides an overview of financial performance {company_text}.<br></h4", unsafe_allow_html=True)

    if selected_years != 'All Years':
        filtered_data = filtered_data[filtered_data['Year']<= selected_years]

    # ===== Downstream processing =====
    FinancialRatio = FinancialAnalyst(filtered_data)
    GeneralFunction = General(filtered_data)
    chart = Chart(filtered_data)

    # START Container 1-1 Financial Highlight
    with st.container (border=True, key='financial-highlight'):
        st.markdown(f"<h2 style='text-align: center; font-style: bold;'>Financial Highlight</h2>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center; font-style: italic; text-align: center;'>This section explains the total of each component in the financial statements.<br></h6>", unsafe_allow_html=True)

        col_1,col_2,col_3 = st.columns(3)

        with col_1 :
            with st.container(border=True, key='grid-financial-highlight'):
                data_rev, val_terakhir, growth_terakhir = FinancialRatio.asset()
                st.metric(label="Total Asset", value=f"Rp {val_terakhir/ 1e6:,.0f} M".replace(',','.'),delta=f"{growth_terakhir:.2f}%")

        with col_2 :
            with st.container(border=True, key='grid-financial-highlight-2'):
                data_rev, val_terakhir, growth_terakhir = FinancialRatio.liabilitas()
                st.metric(label="Total Liabilitas", value=f"Rp {val_terakhir/ 1e6:,.0f} M".replace(',','.'),delta=f"{growth_terakhir:.2f}%")

        with col_3 :
            with st.container(border=True, key='grid-financial-highlight-3'):
                data_rev, val_terakhir, growth_terakhir = FinancialRatio.ekuitas()
                st.metric(label="Total ekuitas", value=f"Rp {val_terakhir/ 1e6:,.0f} M".replace(',','.'),delta=f"{growth_terakhir:.2f}%")

        col_4,col_5,col_6 = st.columns(3)

        with col_4 :
            with st.container(border=True, key='grid-financial-highlight-4'):
                data_rev, val_terakhir, growth_terakhir = FinancialRatio.net_income()
                st.metric(label="Total Net Income", value=f"Rp {val_terakhir/ 1e6:,.0f} M".replace(',','.'),delta=f"{growth_terakhir:.2f}%")

        with col_5 :
            with st.container(border=True, key='grid-financial-highlight-5'):
                data_rev, val_terakhir, growth_terakhir = FinancialRatio.revenue()
                st.metric(label="Total Revenue", value=f"Rp {val_terakhir/ 1e6:,.0f} M".replace(',','.'),delta=f"{growth_terakhir:.2f}%")

        with col_6 :
            with st.container(border=True, key='grid-financial-highlight-6'):
                data_rev, val_terakhir, growth_terakhir = FinancialRatio.expense()
                st.metric(label="Total Expense", value=f"Rp {val_terakhir/ 1e6:,.0f} M".replace(',','.'),delta=f"{growth_terakhir:.2f}%")
        
    # END Container 1-1 Financial Highlight

    # START Container 1-2 Trend Chart
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container (border=True, key='financial-highlight-trend'):
        st.markdown(f"<h2 style='text-align: center; font-style: bold;'>Trend Chart</h2>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center; font-style: italic; text-align: center;'>This section explains the annual trends for each component in the financial statements. </h6>", unsafe_allow_html=True)

        tab_bs, tab_pl, tab1, tab2, tab3, tab4, tab5 = st.tabs(["Balance Sheet", "Profit & Loss", "Asset", "Liabilitas", "Ekuitas", "Revenue", "Expense"])    

        with tab_bs: 
            # Chart untuk beberapa akun sekaligus
            st.write(chart.trends_chart_multi(['10','20','30'],'Balance Sheet Trend'))

        with tab_pl:
            # Chart untuk beberapa akun sekaligus
            st.write(chart.trends_chart_multi(['40','50'],'Profit & Loss Trend'))
        
        with tab1:
            # st.plotly_chart(chart.trends_chart('10','debit','Asset Trend Chart'), use_container_width=True)
            st.write(chart.trends_chart('10','debit','Asset Trend Chart'))
            asset = GeneralFunction.comparative_balance('10','debit')
            GeneralFunction.extends_dataframe(asset)

        with tab2:
            st.write(chart.trends_chart('20','credit','Liabilitas Trend Chart'))
            liabilitas = GeneralFunction.comparative_balance('20','credit')
            GeneralFunction.extends_dataframe(liabilitas)
        
        with tab3:
            st.write(chart.trends_chart('30','credit','Ekuitas Trend Chart'))
            ekuitas = GeneralFunction.comparative_balance('30','credit')
            GeneralFunction.extends_dataframe(ekuitas)

        with tab4:
            st.write(chart.trends_chart('40','credit','Revenue Trend Chart'))
            revenue = GeneralFunction.comparative_balance('40','credit')
            GeneralFunction.extends_dataframe(revenue)
            
        with tab5:
            st.write(chart.trends_chart('50','debit','Expense Trend Chart'))
            expense = GeneralFunction.comparative_balance('50','debit')
            GeneralFunction.extends_dataframe(expense)
    
    # END Container 1-2 Trend Chart

    # Container 1-3: Financial Ratio
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True, key='financial-highlight-2'):
        st.markdown(f"<h2 style='text-align: center; font-style: bold;padding-top: 20px;'>Financial Ratio</h2>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center; font-style: italic; text-align: center;'>This section explains the key financial ratios derived from the financial statements.<br></h6>", unsafe_allow_html=True)
        
        col_1,col_2,col_3,col_4 = st.columns(4)

        with col_1 :
            with st.container(border=True, key='grid-financial-ratio'):
                st.metric(label="Current Ratio", value=f"{FinancialRatio.current_ratio()[1]:.2f} x",delta=f"{FinancialRatio.current_ratio()[2]:.2f}%")
                
        with col_2 :
            with st.container(border=True, key='grid-financial-ratio-2'):
                st.metric(label="Debt to Equity Ratio", value=f"{FinancialRatio.debt_to_equity_ratio()[1]:.2f} x",delta=f"{FinancialRatio.debt_to_equity_ratio()[2]:.2f}%")
        
        with col_3 :
            with st.container(border=True, key='grid-financial-ratio-3'):
                st.metric(label="Debt to Asset Ratio", value=f"{FinancialRatio.debt_to_asset_ratio()[1]:.2f} x",delta=f"{FinancialRatio.debt_to_asset_ratio()[2]:.2f}%")
        
        with col_4 :
            with st.container(border=True, key='grid-financial-ratio-4'):
                st.metric(label="Net Profit Margin", value=f"{FinancialRatio.net_profit_margin()[1]:.2f} x",delta=f"{FinancialRatio.net_profit_margin()[2]:.2f}%")
        
        col_5,col_6,col_7,col_8 = st.columns(4)
        
        with col_5 :
            with st.container(border=True, key='grid-financial-ratio-5'):
                st.metric(label="Return on Assets", value=f"{FinancialRatio.return_on_assets()[1]:.2f} x",delta=f"{FinancialRatio.return_on_assets()[2]:.2f}%")
                
        with col_6 :
            with st.container(border=True, key='grid-financial-ratio-6'):
                st.metric(label="Cash Ratio", value=f"{FinancialRatio.cash_ratio()[1]:.4f} x",delta=f"{FinancialRatio.cash_ratio()[2]:.2f}%")
        
        with col_7 :
            with st.container(border=True, key='grid-financial-ratio-7'):
                st.metric(label="Return on Equity", value=f"{FinancialRatio.return_on_equity()[1]:.2f} x",delta=f"{FinancialRatio.return_on_equity()[2]:.2f}%")
        
        with col_8 :
            with st.container(border=True, key='grid-financial-ratio-8'):
                st.metric(label="Cost to Income Ratio", value=f"{FinancialRatio.total_expense_to_total_revenue_ratio()[1]:.2f} x",delta=f"{FinancialRatio.total_expense_to_total_revenue_ratio()[2]:.2f}%")
    # END Container 1-3: Financial Ratio

    # Container 1-4: Expense to Revenue Ratio
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True, key='financial-highlight-expense'):
        st.markdown(f"<h2 style='text-align: center; font-style: bold;'>Expense to Revenue Ratio</h2>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center; font-style: italic; text-align: center;'>This section explains the annual Expense to Revenue Ratio, indicating year-to-year changes in expenses relative to revenue. <br></h6>", unsafe_allow_html=True)
        
        with st.container(border=True, key="grid-financial-highlight-expense"):
            df = FinancialRatio.expense_to_revenue_ratio()

            # Ubah tipe data kolom delta dan non-delta menjadi int/float
            delta_cols = [col for col in df.columns if '(Δ)' in str(col)]
            non_delta_cols = [col for col in df.columns if col not in delta_cols and 'FSLI' not in str(col)]

            for col in delta_cols:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace('%', '', regex=False)
                    .replace(['nan', 'None', '', '-'], pd.NA)
                    .astype(float)
                )
            
            for col in non_delta_cols:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace('%', '', regex=False)
                    .replace(['nan', 'None', '', '-'], pd.NA)
                    .astype(float)
                )

            # Function to apply color styling - hanya untuk kolom delta (Δ)
            def style_delta(val):
                if pd.isna(val):
                    return ''
                if isinstance(val, (int, float)):
                    if val > 0:
                        return 'color: green'
                    elif val < 0:
                        return 'color: red'
                return ''
            
            # Format persen dengan 2 desimal (otomatis rata kanan untuk angka)
            column_config = {}

            # col Δ -> persen, 2 desimal
            for col in delta_cols:
                column_config[col] = st.column_config.NumberColumn(
                    col,
                    format="%.2f%%"
                )

            # non Δ -> angka biasa, 2 desimal
            numeric_cols = df.select_dtypes(include='number').columns
            for col in numeric_cols:
                if col not in delta_cols:
                    column_config[col] = st.column_config.NumberColumn(
                        col,
                        format="%.2f%%"
                    )
                                
            # Membuat dictionary untuk column_config
            st.dataframe(
                df.style.applymap(style_delta, subset=delta_cols),
                column_config=column_config,
                hide_index=True
            )
                
    # END Container 1-4: Expense to Revenue Ratio

# START Container 2: Smart Naratif
with st.container(border=False, key="smart-naratif"):
    with st.expander("Smart Naratif"):
        with st.container(border=True, key="financial-highlight-smart1"):
                st.markdown("#### Kas dan Setara Kas Analysis")
                text ="Kas dan setara kas per 31 December 2024 mengalami penurunan sebesar -Rp466 miliar atau sebesar -25% dibandingkan saldo periode sebelumnya. Persentase penurunan nilai akun Kas dan setara kas ini lebih kecil dibandingkan perubahan rata-rata pada tahun 2021-2023 sebesar 7% (pada tahun 2023, 2022, dan 2021 masing-masing sebesar -4%, -2%, dan 27%). Penurunan nilai akun Kas dan setara kas ini mewakili -69% dari penurunan total aset pada periode yang sama. Secara vertikal, Kas dan setara kas per 31 December 2024 memiliki porsi sebesar 13% dari total aset pada periode yang sama."
                st.write(text)
        with st.container(border=True, key="financial-highlight-smart2"):
                st.markdown("#### Pajak dibayar dimuka Analysis")
                text ="Pajak dibayar dimuka per 31 December 2024 mengalami peningkatan sebesar Rp19,5 miliar atau sebesar 720% dibandingkan saldo periode sebelumnya. Persentase peningkatan nilai akun Pajak dibayar dimuka ini lebih besar dibandingkan perubahan rata-rata pada tahun 2021-2023 sebesar -36% (pada tahun 2023, 2022, dan 2021 masing-masing sebesar -38%, -52%, dan -18%). Peningkatan nilai akun Pajak dibayar dimuka ini mewakili 3% dari penurunan total aset pada periode yang sama. Secara vertikal, Pajak dibayar dimuka per 31 December 2024 memiliki porsi sebesar 0% dari total aset pada periode yang sama."
                st.write(text)
    st.markdown("</div>", unsafe_allow_html=True)

        
    




