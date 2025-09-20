import streamlit as st
import pandas as pd
import plotly.express as px
import time

# PAGE CONFIGURATION
st.set_page_config(page_title="Interactive Visualizations", layout="wide")

st.title("Stories Through Data: Debt and Health in Lebanon -- Ali's Interactive Visualizations with Streamlit")
st.markdown(
    """
    AT ITS CORE, data is more than just numbers. It's about people and their stories, their jobs and countries, their struggles and their resilience.
    In this dashboard, we look at two very different but deeply human dimensions of Lebanon's story:
    1. **Total Debt Service in Lebanon (1970-2022)**
    2. **Hepatitis Cases in Lebanon (2015-2018)**  

    Play with the filters to see how each story changes. Different years = different views = new insights!
    """
)

# ---------
# 1. DEBT SERVICE VISUALIZATION
# ---------
st.header("💰 Total Debt Service Over Time (Public & Publicly Guaranteed)")

st.markdown(
    """
    **Context:**  
    Debt service refers to the annual payments a country makes on its debt—both the interest owed and the repayment of the borrowed principal.  
    In Lebanon's case, this means the money the government must set aside each year to honor its loans.  

    The chart shows how these payments have grown over time.  
    What looks like a rising line is really the story of reconstruction borrowing after the war, the accumulation of public debt,  
    and the mounting burden of paying creditors—until the sharp collapse after 2020, when Lebanon defaulted for the first time.  
    """
)

# Load the dataset from the provided URL
DATA_URL = "https://linked.aub.edu.lb/pkgcube/data/ec45e2c5e9fdf38846d3459363b0e691_20240909_232106.csv"
df_debt = pd.read_csv(DATA_URL)

# Filter the relevant indicator
df_debt = df_debt[df_debt["Indicator Code"] == "DT.TDS.DPPG.CD"]

# Clean & sort the data
df_debt = df_debt.sort_values("refPeriod")

# Interactive control: select the years
min_year = int(df_debt["refPeriod"].min())
max_year = int(df_debt["refPeriod"].max())

year_range = st.slider(
    "Choose range of years to display:",
    min_year,
    max_year,
    (1970, max_year)
)

df_debt_filtered = df_debt[
    (df_debt["refPeriod"] >= year_range[0]) &
    (df_debt["refPeriod"] <= year_range[1])
]

# Plot
fig_debt = px.line(
    df_debt_filtered,
    x="refPeriod",
    y="Value",
    title="Debt Service (Public & Publicly Guaranteed) - Selected Years",
    labels={"refPeriod": "Year", "Value": "Debt Service in USD"}
)

st.plotly_chart(fig_debt, use_container_width=True)

# Insights
st.markdown(
    """
    **What stands out here?**  
    - In the early years, debt service looks almost harmless—barely noticeable on the chart.  
    - Then, as Lebanon moved into the 2000s, the line shoots up, as the country was leaning harder and harder on borrowed money.  
    - If you slide through the years, you'll see how some spikes match moments of crisis—global downturns, political turmoil, and finally the crash after 2020.  
    - What's striking is not just the numbers, but the story behind them: a country buying time with borrowed dollars, until the clock finally ran out.
    """
)

# ---------
# 2. HEPATITIS CASES VISUALIZATION
# ---------
st.header("🦠 Hepatitis Cases in Lebanon (2015-2018)")

st.markdown(
    """
    **Context:**  
    This bar chart presents reported hepatitis cases in Lebanon between 2015 and 2018.  
    Hepatitis is a liver infection, often linked to sanitation, vaccination coverage, and public health interventions.  

    Each bar represents reported cases over time, offering insights into patterns of outbreaks, improvements in surveillance systems,  
    and the effectiveness of health responses across different years.  
    """
)

# Load dataset directly from the provided URL
DATA_URL = "https://linked.aub.edu.lb/pkgcube/data/06ba9548b68a7efd5caf9e6f1e899ae6_20240909_184811.csv"
df_hepatitis = pd.read_csv(DATA_URL)

# Extract month-year (e.g. 01-2015) from refPeriod
df_hepatitis["refPeriod"] = df_hepatitis["refPeriod"].str.extract(r"(\d{2}-\d{4})")

# Convert to datetime format
df_hepatitis["Date"] = pd.to_datetime(df_hepatitis["refPeriod"], format="%m-%Y", errors="coerce")

# Drop rows without valid date
df_hepatitis = df_hepatitis.dropna(subset=["Date"])

# Extract year as a string for coloring/filtering
df_hepatitis["Year"] = df_hepatitis["Date"].dt.year.astype(str)

# Aggregate number of cases by Date and Year
cases_over_time = df_hepatitis.groupby(["Date", "Year"])["Number of cases"].sum().reset_index()

# ---------
# Interactive Features
# ---------

# Year selector (multi)
years_available = sorted(cases_over_time["Year"].unique())
years_selected = st.multiselect(
    "Select which years to display:",
    years_available,
    default=years_available
)

cases_filtered = cases_over_time[cases_over_time["Year"].isin(years_selected)]

# Aggregation toggle
aggregation = st.radio(
    "View data as:",
    ["Monthly Cases", "Yearly Totals"]
)

# ---------
# Plotting
# ---------
if aggregation == "Yearly Totals":
    yearly_cases = cases_filtered.groupby("Year")["Number of cases"].sum().reset_index()
    fig = px.bar(
        yearly_cases,
        x="Year",
        y="Number of cases",
        color="Year",
        title="Total Hepatitis Cases per Year",
        labels={"Number of cases": "Reported Cases"}
    )
else:
    fig = px.bar(
        cases_filtered,
        x="Date",
        y="Number of cases",
        color="Year",
        title="Monthly Hepatitis Cases in Lebanon",
        labels={"Date": "Month-Year", "Number of cases": "Reported Cases"}
    )
    fig.update_xaxes(dtick="M3", tickformat="%b %Y")  # tick every 3 months

st.plotly_chart(fig, use_container_width=True)

# ---------
# Insights
# ---------
st.markdown(
    """
    **What catches the eye here?**  
    - In 2015, there are noticeable peaks; this suggests possible outbreaks or better reporting that year.  
    - Later years feel calmer, but toggling to yearly totals shows that the burden didn't just vanish; it fluctuated in quieter ways.  
    - Switching between *monthly* and *yearly* views helps reveal patterns: sudden seasonal spikes, or how yearly sums mask the month-to-month drama.  
    - Behind these numbers are human stories: stronger health systems, changing awareness, and the realities of disease surveillance.  
    """
)

# ---------
# END
# ---------
if st.button("Reveal closing message"):
    placeholder = st.empty()
    message = "From debt to disease, I hope you learned something new! :)"
    
    words = message.split()
    text = ""
    for word in words:
        text += word + " "
        placeholder.success(text)
        time.sleep(0.15)
