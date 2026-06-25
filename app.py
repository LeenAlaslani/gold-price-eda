import streamlit as st
import pandas as pd
import plotly.express as px


# i make the page wide because i want to put two charts beside each other
# this make the app look more like dashboard and not one very long page

st.set_page_config(
    page_title="Gold Price EDA",
    page_icon="📊",
    layout="wide"
)


# these colors will be used in the full app
# i used gold colors because the project is about gold
# green will mean up and red will mean down
# gray will be used for days that dont have events

GOLD = "#D4A017"
LIGHT_GOLD = "#F2D675"
DARK_GOLD = "#8A6914"
CHARCOAL = "#30343F"
SOFT_GRAY = "#CBD1DA"
GREEN = "#3A8D63"
RED = "#C45156"
BLUE = "#4776B4"


# this only change small things in the streamlit page
# i wanted the quick numbers to look like small cards
# the css part is only for the look and it does not change the data

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stMetric"] {
        background-color: #FAF7EF;
        border: 1px solid #E6D8AF;
        border-radius: 12px;
        padding: 18px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 15px;
    }

    [data-testid="stMetricValue"] {
        color: #8A6914;
    }

    div[data-testid="stSidebar"] {
        background-color: #F7F4EC;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# i read gold_final because this is the final data after cleaning
# it already have the new columns that i made in the notebook
# like Abs_Change Event_Group Year and Month
# so i dont need to repeat the cleaning inside the app

data = pd.read_csv("gold_final.csv")


# after saving as csv the date return as text
# charts need a real date so i change it again here

data["Date"] = pd.to_datetime(data["Date"])


# i make sure year and month are numbers
# this will help when the user choose the year from the filter

data["Year"] = data["Year"].astype(int)
data["Month"] = data["Month"].astype(int)


# sometimes true and false may return from csv like text
# here i make sure Has_Event is real True or False

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


# if Direction was not saved for any reason
# i make it again using Change_percent
# positive values become Up and negative values become Down

if "Direction" not in data.columns:

    data["Direction"] = "Down"

    data.loc[
        data["Change_percent"] > 0,
        "Direction"
    ] = "Up"


# this new name is only for the pie chart
# it is easier to understand than showing True and False

data["Event_Label"] = data["Has_Event"].map({
    True: "Event Days",
    False: "No Event Days"
})


# i make month names because Mar is easier than only seeing number 3

data["Month_Name"] = data["Date"].dt.strftime("%b")


# main title and simple explain about the app

st.title("Gold Price EDA Dashboard")

st.write(
    "This app show gold prices and make it more easy to compare "
    "gold movement in economic event days and normal days."
)


# --------------------------------------------------
# filters
# --------------------------------------------------

st.sidebar.title("Filters")

st.sidebar.write(
    "The charts and numbers will change when i select different options."
)


# i collect the years from the data and put them in order
# All mean dont remove any year from the data

years = sorted(
    data["Year"]
    .dropna()
    .unique()
    .tolist()
)

selected_year = st.sidebar.selectbox(
    "Choose the year",
    ["All"] + years
)


# this filter can keep all days
# or only event days
# or only days that did not have economic event

event_choice = st.sidebar.selectbox(
    "Choose event days",
    [
        "All days",
        "Event days",
        "No event days"
    ]
)


# this filter checks if gold went up or down
# this give the user one more simple thing to explore

direction_choice = st.sidebar.selectbox(
    "Choose gold direction",
    [
        "All directions",
        "Up",
        "Down"
    ]
)


# i copy the data because i will remove some rows using the filters
# i dont want the original data itself to change

filtered_data = data.copy()


# applying the year filter

if selected_year != "All":

    filtered_data = filtered_data[
        filtered_data["Year"] == selected_year
    ]


# applying the event filter

if event_choice == "Event days":

    filtered_data = filtered_data[
        filtered_data["Has_Event"] == True
    ]

elif event_choice == "No event days":

    filtered_data = filtered_data[
        filtered_data["Has_Event"] == False
    ]


# applying the direction filter

if direction_choice != "All directions":

    filtered_data = filtered_data[
        filtered_data["Direction"] == direction_choice
    ]


# maybe some filter choices have no rows
# if this happen i show a message instead of getting error in the charts

if filtered_data.empty:

    st.warning("There is no data for these filters.")

    st.stop()


# --------------------------------------------------
# quick numbers
# --------------------------------------------------

st.subheader("Quick Numbers")


# four columns will show four simple numbers
# all numbers change when the user change the filters

col1, col2, col3, col4 = st.columns(4)


# average gold price in the selected data

col1.metric(
    "Average Price",
    f'{filtered_data["Price"].mean():,.2f}'
)


# highest gold price in the selected data

col2.metric(
    "Highest Price",
    f'{filtered_data["Price"].max():,.2f}'
)


# Abs_Change show movement size
# it does not care if the value was positive or negative

col3.metric(
    "Average Movement",
    f'{filtered_data["Abs_Change"].mean():.2f}%'
)


# this just tell how many days is still inside the selected data

col4.metric(
    "Days Shown",
    f'{len(filtered_data):,}'
)


# this function will be used for all charts
# because i dont want to repeat the same design lines many times

def clean_chart(fig, height=390):

    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=25,
            b=20
        ),
        font=dict(
            family="Arial",
            size=13,
            color=CHARCOAL
        ),
        legend_title_text="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white"
    )

    return fig


# --------------------------------------------------
# first row
# price chart and event pie
# --------------------------------------------------

left1, right1 = st.columns([1.7, 1])


with left1:

    st.subheader("Gold Price Over Time")

    line_data = filtered_data.sort_values("Date")

    # this is an area chart
    # the line is gold and there is a light color under it
    # because one price column is one line so it does not need many colors

    fig_line = px.area(
        line_data,
        x="Date",
        y="Price",
        labels={
            "Date": "Date",
            "Price": "Gold Price"
        }
    )

    fig_line.update_traces(
        line=dict(
            color=GOLD,
            width=2
        ),
        fillcolor="rgba(212,160,23,0.18)",
        hovertemplate=(
            "Date: %{x|%Y-%m-%d}"
            "<br>Price: %{y:,.2f}"
            "<extra></extra>"
        )
    )

    clean_chart(fig_line, height=430)

    st.plotly_chart(
        fig_line,
        use_container_width=True
    )


with right1:

    st.subheader("Event Days Share")

    # i count event days and no event days
    # after that i put them in a donut chart

    event_count_data = (
        filtered_data["Event_Label"]
        .value_counts()
        .reset_index()
    )

    event_count_data.columns = [
        "Event Type",
        "Days"
    ]

    fig_pie = px.pie(
        event_count_data,
        names="Event Type",
        values="Days",
        hole=0.55,
        color="Event Type",
        color_discrete_map={
            "Event Days": GOLD,
            "No Event Days": SOFT_GRAY
        }
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "%{label}"
            "<br>Days: %{value}"
            "<br>Percent: %{percent}"
            "<extra></extra>"
        )
    )

    clean_chart(fig_pie, height=430)

    fig_pie.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


# --------------------------------------------------
# second row
# distribution and event group
# --------------------------------------------------

left2, right2 = st.columns(2)


with left2:

    st.subheader("Distribution of Gold Prices")

    # i color the histogram using Up and Down
    # green means the price went up
    # red means the price went down

    fig_hist = px.histogram(
        filtered_data,
        x="Price",
        color="Direction",
        nbins=30,
        barmode="overlay",
        opacity=0.72,
        color_discrete_map={
            "Up": GREEN,
            "Down": RED
        },
        labels={
            "Price": "Gold Price",
            "count": "Number of Days"
        }
    )

    clean_chart(fig_hist)

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )


with right2:

    st.subheader("Movement by Event Group")

    # i calculate average movement for every group
    # i give every group its own color because they mean different things

    event_group_data = (
        filtered_data
        .groupby("Event_Group")["Abs_Change"]
        .mean()
        .reset_index()
    )

    fig_event = px.bar(
        event_group_data,
        x="Event_Group",
        y="Abs_Change",
        color="Event_Group",
        text_auto=".2f",
        color_discrete_map={
            "No Event": SOFT_GRAY,
            "1-3 Events": GOLD,
            "4+ Events": DARK_GOLD
        },
        labels={
            "Event_Group": "Event Group",
            "Abs_Change": "Average Movement %"
        }
    )

    fig_event.update_traces(
        textposition="outside"
    )

    clean_chart(fig_event)

    fig_event.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_event,
        use_container_width=True
    )

    # i write a small result under the chart
    # so the user does not only see bars without understanding them

    highest_event_group = event_group_data.loc[
        event_group_data["Abs_Change"].idxmax(),
        "Event_Group"
    ]

    st.caption(
        f"In the selected data, {highest_event_group} "
        "has the highest average movement."
    )


# --------------------------------------------------
# third row
# year and month
# --------------------------------------------------

left3, right3 = st.columns(2)


with left3:

    st.subheader("Gold Movement by Year")

    year_data = (
        filtered_data
        .groupby("Year")["Abs_Change"]
        .mean()
        .reset_index()
    )

    # the bar color gets darker when the movement is higher
    # this help the user find the highest year quickly

    fig_year = px.bar(
        year_data,
        x="Year",
        y="Abs_Change",
        color="Abs_Change",
        text_auto=".2f",
        color_continuous_scale=[
            "#F7EBC4",
            GOLD,
            DARK_GOLD
        ],
        labels={
            "Year": "Year",
            "Abs_Change": "Average Movement %"
        }
    )

    fig_year.update_traces(
        textposition="outside"
    )

    clean_chart(fig_year)

    fig_year.update_layout(
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )


with right3:

    st.subheader("Gold Movement by Month")

    month_data = (
        filtered_data
        .groupby(["Month", "Month_Name"])["Abs_Change"]
        .mean()
        .reset_index()
        .sort_values("Month")
    )

    fig_month = px.bar(
        month_data,
        x="Month_Name",
        y="Abs_Change",
        color="Abs_Change",
        text_auto=".2f",
        color_continuous_scale=[
            "#E5EAF1",
            LIGHT_GOLD,
            GOLD
        ],
        labels={
            "Month_Name": "Month",
            "Abs_Change": "Average Movement %"
        }
    )

    fig_month.update_traces(
        textposition="outside"
    )

    clean_chart(fig_month)

    fig_month.update_layout(
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )


# --------------------------------------------------
# scatter plot
# --------------------------------------------------

st.subheader("Volume and Gold Movement")


# every event group have a different color in the scatter
# when i move the mouse on a point it show more information

fig_scatter = px.scatter(
    filtered_data,
    x="Vol_K",
    y="Abs_Change",
    color="Event_Group",
    hover_data={
        "Date": "|%Y-%m-%d",
        "Price": ":,.2f",
        "Change_percent": ":.2f",
        "Event_Count": True
    },
    color_discrete_map={
        "No Event": SOFT_GRAY,
        "1-3 Events": GOLD,
        "4+ Events": DARK_GOLD
    },
    labels={
        "Vol_K": "Trading Volume",
        "Abs_Change": "Gold Movement %",
        "Event_Group": "Event Group"
    }
)

fig_scatter.update_traces(
    marker=dict(
        size=8,
        opacity=0.65,
        line=dict(
            width=0.5,
            color="white"
        )
    )
)

clean_chart(fig_scatter, height=450)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# --------------------------------------------------
# biggest movement table
# --------------------------------------------------

st.subheader("Biggest Gold Movement Days")


# i select the 10 days with highest Abs_Change
# after this i only keep the useful columns

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
        "Event_Group",
        "Direction"
    ]
].copy()


# i remove the time because it was always 00:00:00
# i also reset the index because old row numbers was confusing

top_days["Date"] = (
    top_days["Date"]
    .dt.strftime("%Y-%m-%d")
)

top_days = top_days.reset_index(drop=True)


# i rename the columns so the table is easier to read

top_days = top_days.rename(
    columns={
        "Change_percent": "Change Percent",
        "Abs_Change": "Absolute Change",
        "Event_Count": "Event Count",
        "Event_Group": "Event Group"
    }
)


st.dataframe(
    top_days,
    use_container_width=True,
    hide_index=True
)


# the full filtered data is hidden inside this part
# the user can open it only if they want to see all rows

with st.expander("Show filtered data"):

    full_data = filtered_data.copy()

    full_data["Date"] = (
        full_data["Date"]
        .dt.strftime("%Y-%m-%d")
    )

    st.dataframe(
        full_data,
        use_container_width=True,
        hide_index=True
    )


# final note because the charts only show relationships
# they do not prove the event caused the price change

st.caption(
    "This dashboard shows patterns and comparisons in the dataset. "
    "It does not prove that economic events directly caused every gold movement."
)
