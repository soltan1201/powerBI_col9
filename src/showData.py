
import pandas as pd

# this function get the % change for any column by year and specified
def get_per_year_change(col,df,metric):
    grp_years = df.groupby('year')[col].agg([metric])[metric]
    grp_years = grp_years.pct_change() * 100
    grp_years.fillna(0, inplace=True)
    grp_years = grp_years.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else 'NaN')

    return grp_years

def load_data():
    df = pd.read_csv('dbase/Superstore2023.csv')
    print(df.head())
    print("colunas \n ", df.columns)
    # print(df['Ship Date'].head())
    # get the year and store as a new column
    df['Order Date'] = pd.to_datetime(df['Order Date'], format= "%d/%m/%Y %H:%M:%S")
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format= "%d/%m/%Y")
    df['year'] = df['Order Date'].dt.year
    # get the difference of Shipped date and order date
    df['days to ship'] = abs(df['Ship Date']- df['Order Date']).dt.days

    # get the % change of sales, profit and orders over the years
    grp_years_sales = get_per_year_change('Sales',df,'sum')
    grp_year_profit = get_per_year_change('Profit',df,'sum')
    grp_year_orders = get_per_year_change('Order ID',df,'count')

    return df, grp_years_sales, grp_year_profit,grp_year_orders






# load cached data
df_original , grp_years_sales, grp_year_profit, grp_year_orders = load_data()

print(df_original.head())