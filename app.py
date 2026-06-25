import streamlit as st
import pandas as pd
import plotly.express as px


# making the page wider so charts look better
st.set_page_config(
    page_title="Gold Price EDA",
    layout="wide"
)


# reading the final data
# i use this because i already cleaned it in the notebook
data = pd.read_csv("gold_final.csv")


# date need to be real datetime not text
data["Date"] = pd.to_datetime(data["Date"])


# making sure Has_Event is boolean
if data["Has_Event"].dtype != bool:
    data["Has_Event"] = (
        data["Has_Event"]
        .astype(str)
        .str.lower()
        .map({"true": True, "false": False})
    )


# start title
st.title("Gold Price EDA")

st.write(
    "This app show gold prices and some simple analysis "
    "about gold movement and economic events."
)


# -------------------------
# sidebar filters
# -------------------------

st.sidebar.title("Filters")

years = sorted(
    data["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

year_options = ["All"] + years

selected_year = st.sidebar.selectbox(
    "Choose the year",
    year_options
)

event_choice = st.sidebar.selectbox(
    "Choose event days",
    ["All days", "Event days", "No event days"]
)


# making filtered data
filtered_data = data.copy()

if selected_year != "All":
    filtered_data = filtered_data[
        filtered_data["Year"] == selected_year
    ]

if event_choice == "Event days":
    filtered_data = filtered_data[
        filtered_data["Has_Event"] == True
    ]

elif event_choice == "No event days":
    filtered_data = filtered_data[
        filtered_data["Has_Event"] == False
    ]


# if no rows after filter stop here
if filtered_data.empty:
    st.warning("No data for this filter.")
    st.stop()


# -------------------------
# small numbers
# -------------------------

st.subheader("Quick Numbers")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Price",
    f'{filtered_data["Price"].mean():,.2f}'
)

col2.metric(
    "Highest Price",
    f'{filtered_data["Price"].max():,.2f}'
)

col3.metric(
    "Average Movement",
    f'{filtered_data["Abs_Change"].mean():.2f}%'
)

col4.metric(
    "Average Event Count",
    f'{filtered_data["Event_Count"].mean():.2f}'
)


# -------------------------
# chart 1 line chart
# -------------------------

st.subheader("Gold Price Over Time")

line_df = filtered_data.sort_values("Date")

fig_line = px.line(
    line_df,
    x="Date",
    y="Price",
    title="Gold Price Over Time"
)

st.plotly_chart(fig_line, use_container_width=True)


# -------------------------
# chart 2 histogram
# -------------------------

st.subheader("Distribution of Gold Prices")

fig_hist = px.histogram(
    filtered_data,
    x="Price",
    nbins=30,
    title="Distribution of Gold Prices"
)

st.plotly_chart(fig_hist, use_container_width=True)


# -------------------------
# chart 3 pie chart
# -------------------------

st.subheader("Event Days vs No Event Days")

event_count_df = (
    filtered_data["Has_Event"]
    .value_counts()
    .reset_index()
)

event_count_df.columns = ["Has_Event", "Count"]

event_count_df["Has_Event"] = event_count_df["Has_Event"].map({
    True: "Event Days",
    False: "No Event Days"
})

fig_pie = px.pie(
    event_count_df,
    names="Has_Event",
    values="Count",
    title="Event Days vs No Event Days"
)

st.plotly_chart(fig_pie, use_container_width=True)


# -------------------------
# chart 4 bar event group
# -------------------------

st.subheader("Gold Movement by Event Group")

event_group_df = (
    filtered_data
    .groupby("Event_Group")["Abs_Change"]
    .mean()
    .reset_index()
)

fig_event_group = px.bar(
    event_group_df,
    x="Event_Group",
    y="Abs_Change",
    title="Average Gold Movement by Event Group",
    text_auto=True
)

st.plotly_chart(fig_event_group, use_container_width=True)


# -------------------------
# chart 5 movement by year
# -------------------------

st.subheader("Gold Movement by Year")

year_df = (
    filtered_data
    .groupby("Year")["Abs_Change"]
    .mean()
    .reset_index()
)

fig_year = px.bar(
    year_df,
    x="Year",
    y="Abs_Change",
    title="Average Gold Movement by Year",
    text_auto=True
)

st.plotly_chart(fig_year, use_container_width=True)


# -------------------------
# chart 6 movement by month
# -------------------------

st.subheader("Gold Movement by Month")

month_df = (
    filtered_data
    .groupby("Month")["Abs_Change"]
    .mean()
    .reset_index()
)

fig_month = px.bar(
    month_df,
    x="Month",
    y="Abs_Change",
    title="Average Gold Movement by Month",
    text_auto=True
)

st.plotly_chart(fig_month, use_container_width=True)


# -------------------------
# chart 7 scatter plot
# -------------------------

st.subheader("Volume and Gold Movement")

fig_scatter = px.scatter(
    filtered_data,
    x="Vol_K",
    y="Abs_Change",
    title="Volume vs Gold Movement",
    hover_data=["Date", "Price", "Event_Group"]
)

st.plotly_chart(fig_scatter, use_container_width=True)


# -------------------------
# top 10 table
# -------------------------

st.subheader("Biggest Gold Movement Days")

top_days = filtered_data.nlargest(
    10,
    "Abs_Change"
)[
    [
        "Date",
        "Price",
        "Change_percent",
        "Abs_Change",
        "Event_Count",
        "Event_Group"
    ]
].copy()

top_days["Date"] = top_days["Date"].dt.strftime("%Y-%m-%d")
top_days = top_days.reset_index(drop=True)

top_days = top_days.rename(
    columns={
        "Change_percent": "Change Percent",
        "Abs_Change": "Absolute Change",
        "Event_Count": "Event Count",
        "Event_Group": "Event Group"
    }
)

st.dataframe(top_days, use_container_width=True)


# -------------------------
# raw data
# -------------------------

with st.expander("Show filtered data"):
    show_df = filtered_data.copy()
    show_df["Date"] = show_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(show_df, use_container_width=True)


st.caption(
    "This app show patterns in the data, but it does not prove "
    "that events directly caused every gold price movement."
)
