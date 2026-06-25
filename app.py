import streamlit as st
import pandas as pd


# this make the page wider
# because i have charts and i dont want them to look very small

st.set_page_config(
    page_title="Gold Price EDA",
    layout="wide"
)


# here i read the final csv file
# i use this file because i already cleaned it in the notebook
# and i already made the new columns like Abs_Change and Event_Group
# so i dont need to repeat the full cleaning again here

data = pd.read_csv("gold_final.csv")


# when i save the data as csv the date return like a text
# but for the line chart i need python to understand it as a real date
# so i change the Date column again

data["Date"] = pd.to_datetime(data["Date"])


# sometimes true and false may come from csv as text
# so here i make sure Has_Event is really boolean
# boolean mean it only have True or False

if data["Has_Event"].dtype != bool:

    data["Has_Event"] = (
        data["Has_Event"]
        .astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False
        })
    )


# this is the main title in the app

st.title("Gold Price EDA")


# this is a small explain about the app
# the app is not predicting the gold price
# it only show the data and let the user explore the results

st.write(
    "This app show gold prices and how the gold movement "
    "was different with economic events."
)


# i put the filters in the sidebar
# sidebar is the part that show in the left side of the page

st.sidebar.title("Filters")


# first i collect all the years from my dataset
# sorted put them in the correct order
# then i add All in the beginning so the user can use all years together

years = sorted(
    data["Year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

year_options = ["All"] + years


# this make a select box for the year
# the user can choose one year or choose All

selected_year = st.sidebar.selectbox(
    "Choose the year",
    year_options
)


# here i copy the full data
# i use a copy because later i will remove some rows based on the filters
# and i dont want to change the original data itself

filtered_data = data.copy()


# if the user choose one year
# i only keep the rows from this year
# but if the user choose All i dont remove anything

if selected_year != "All":

    filtered_data = filtered_data[
        filtered_data["Year"] == selected_year
    ]


# this is the second filter
# All days mean use every row
# Event days mean only rows where Has_Event is True
# No event days mean only rows where Has_Event is False

event_choice = st.sidebar.selectbox(
    "Choose event days",
    [
        "All days",
        "Event days",
        "No event days"
    ]
)


# here i apply the event filter

if event_choice == "Event days":

    filtered_data = filtered_data[
        filtered_data["Has_Event"] == True
    ]


elif event_choice == "No event days":

    filtered_data = filtered_data[
        filtered_data["Has_Event"] == False
    ]


# maybe the user choose a filter and there is no rows
# without this check the charts may give an error
# so i stop the app and show a message instead

if filtered_data.empty:

    st.warning("There is no data for this filter.")

    st.stop()


# now i make three columns beside each other
# these are only quick numbers to summarize the selected data
# they will change every time the user change a filter

col1, col2, col3 = st.columns(3)


# average price mean i add all gold prices in the filtered data
# then divide them by the number of rows
# :,.2f make the number easier to read and keep two decimals

col1.metric(
    "Average Price",
    f'{filtered_data["Price"].mean():,.2f}'
)


# this show the highest gold price inside the selected rows
# for example if the user choose 2020 it only use 2020 prices

col2.metric(
    "Highest Price",
    f'{filtered_data["Price"].max():,.2f}'
)


# Abs_Change is the movement size
# it does not care if gold moved up or down
# for example +2 and -2 both become movement of 2
# i add the percent sign because this value is a percentage

col3.metric(
    "Average Movement",
    f'{filtered_data["Abs_Change"].mean():.2f}%'
)


# now i make the first chart
# this chart show how gold price changed with time

st.subheader("Gold Price Over Time")


# first i sort the dates from old to new
# then i put Date as the index
# streamlit will use it automatically as the horizontal axis

price_chart = (
    filtered_data
    .sort_values("Date")
    .set_index("Date")[["Price"]]
)


# this create the line chart

st.line_chart(
    price_chart,
    use_container_width=True
)


# now i make the event group chart
# Event_Group has:
# No Event
# 1-3 Events
# 4+ Events
#
# i calculate the average movement for every group
# if the user choose No event days only one group will show
# this is normal because other event groups was removed by the filter

st.subheader("Gold Movement by Event Group")


event_chart = (
    filtered_data
    .groupby("Event_Group")["Abs_Change"]
    .mean()
)


# this create the bar chart

st.bar_chart(
    event_chart,
    use_container_width=True
)


# now i show the biggest gold movement days
# nlargest choose the highest 10 values from Abs_Change
# so it will show days with the biggest movement
# it can be positive or negative because Abs_Change removed the sign

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
].copy()


# the date was showing 00:00:00
# this time is not useful because the dataset is daily
# so i only keep the year month and day

top_days["Date"] = (
    top_days["Date"]
    .dt.strftime("%Y-%m-%d")
)


# after selecting the largest rows
# the old row numbers was still showing like 962 and 799
# these numbers are only the old index from the dataset
# so i remove them and make a new simple index

top_days = top_days.reset_index(drop=True)


# rename the columns only for the app
# because spaces are easier to read than underscore

top_days = top_days.rename(
    columns={
        "Change_percent": "Change Percent",
        "Abs_Change": "Absolute Change",
        "Event_Count": "Event Count",
        "Event_Group": "Event Group"
    }
)


# show the final table

st.table(top_days)


# this is a final small note
# because the app show relationships in the data
# but it does not prove that economic events caused every gold movement

st.caption(
    "The app shows patterns in the dataset, "
    "but it does not prove that economic events caused every gold change."
)
