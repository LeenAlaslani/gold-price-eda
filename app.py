import streamlit as st
import pandas as pd

# here i read the final file because this file already cleaned
# and it already have the new columns i made in the notebook
# so i dont need to repeat all the cleaning again in streamlit

data = pd.read_csv("gold_final.csv")

# when i save data as csv the date usually return as text
# i need it as date again because i want to use it in the line chart

data["Date"] = pd.to_datetime(data["Date"])

st.title("Gold Price EDA")

st.write(
    "This app show gold prices and how the movement was different "
    "with economic events."
)


# i put the filters in the left side
# the user can choose one year or keep all years

st.sidebar.title("Filters")

years = ["All"] + sorted(data["Year"].unique().tolist())

selected_year = st.sidebar.selectbox(
    "Choose the year",
    years
)


# i copy the data first because i dont want to change the original data
# after that if the user choose a year i only keep this year

filtered_data = data.copy()

if selected_year != "All":
    filtered_data = filtered_data[
        filtered_data["Year"] == selected_year
    ]


# this second filter let the user see all days
# or only days with events or days without events

event_choice = st.sidebar.selectbox(
    "Choose event days",
    ["All days", "Event days", "No event days"]
)

if event_choice == "Event days":
    filtered_data = filtered_data[
        filtered_data["Has_Event"] == True
    ]

elif event_choice == "No event days":
    filtered_data = filtered_data[
        filtered_data["Has_Event"] == False
    ]


# maybe the user choose filters and there is no rows
# so i stop the page instead of showing error

if filtered_data.empty:
    st.warning("There is no data for this filter.")
    st.stop()


# here i show some simple numbers from the filtered data
# the numbers will change when the user change the filters

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Price",
    round(filtered_data["Price"].mean(), 2)
)

col2.metric(
    "Highest Price",
    round(filtered_data["Price"].max(), 2)
)

col3.metric(
    "Average Movement",
    round(filtered_data["Abs_Change"].mean(), 2)
)


# i sort the date because the chart need to start from old to new
# then i use Date as the index so streamlit know it is the x axis

st.subheader("Gold Price Over Time")

price_chart = (
    filtered_data
    .sort_values("Date")
    .set_index("Date")[["Price"]]
)

st.line_chart(price_chart)


# here i calculate the average movement for every event group
# this is the same idea i checked before in the notebook
# but now the chart change when the filter change

st.subheader("Gold Movement by Event Group")

event_chart = (
    filtered_data
    .groupby("Event_Group")["Abs_Change"]
    .mean()
)

st.bar_chart(event_chart)


# finally i show the days that had the biggest movement
# nlargest choose the highest 10 values from Abs_Change

st.subheader("Biggest Gold Movement Days")

top_days = filtered_data.nlargest(
    10,
    "Abs_Change"
)[
    [
        "Date",
        "Change_percent",
        "Abs_Change",
        "Event_Count",
        "Event_Group"
    ]
]

st.table(top_days)
