import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# i make the page wide because this is a dashboard
# the charts will have more space and not look very small

st.set_page_config(
    page_title="Gold Price EDA Dashboard",
    page_icon="✨",
    layout="wide"
)


# --------------------------------------------------
# colors
# --------------------------------------------------

# i save the colors here because i will use them many times
# black and gold is the main style because the project is about gold

GOLD = "#D9A514"
LIGHT_GOLD = "#F3CE69"
DARK_GOLD = "#8E6B0C"

BLACK = "#090A0D"
CARD = "#15171C"
CARD_2 = "#1B1D23"

WHITE = "#F7F3E8"
GRAY = "#A5A8B0"
SOFT_GRAY = "#C7CBD3"

GREEN = "#4FA879"
RED = "#D56767"
BLUE = "#557DBE"


# --------------------------------------------------
# full page style
# --------------------------------------------------

# this part look long but it only change the design
# i wanted the page to look more premium and not like normal streamlit

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(217,165,20,0.08),
                transparent 27%
            ),
            #090A0D;
        color: #F7F3E8;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1500px;
    }


    /* sidebar */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07080A 0%,
                #111216 52%,
                #18191D 100%
            );
        border-right: 1px solid rgba(217,165,20,0.20);
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #F7F3E8 !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background-color: #191B20;
        color: #F7F3E8;
        border: 1px solid rgba(217,165,20,0.35);
        border-radius: 12px;
        min-height: 46px;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] svg {
        fill: #D9A514;
    }


    /* hero */

    .hero {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(217,165,20,0.24),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #121318 0%,
                #1B1D22 55%,
                #101115 100%
            );

        border: 1px solid rgba(217,165,20,0.30);
        border-radius: 26px;
        padding: 35px;
        margin-bottom: 22px;

        box-shadow:
            0 18px 45px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(217,165,20,0.12);
        color: #F3CE69;
        border: 1px solid rgba(217,165,20,0.42);
        border-radius: 100px;
        padding: 7px 13px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 46px;
        line-height: 1.05;
        font-weight: 900;
        color: #F7F3E8;
        margin-bottom: 12px;
    }

    .hero-gold {
        color: #D9A514;
    }

    .hero-text {
        color: #C7CBD3;
        font-size: 16px;
        line-height: 1.8;
        max-width: 900px;
    }


    /* sidebar cards */

    .side-brand {
        background:
            radial-gradient(
                circle at top right,
                rgba(217,165,20,0.25),
                transparent 40%
            ),
            #15171C;

        border: 1px solid rgba(217,165,20,0.30);
        border-radius: 22px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .side-logo {
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #D9A514;
        margin-bottom: 7px;
    }

    .side-title {
        font-size: 30px;
        font-weight: 900;
        color: #F7F3E8;
        margin-bottom: 8px;
    }

    .side-description {
        font-size: 13px;
        line-height: 1.7;
        color: #B8BBC3;
    }

    .side-hint {
        background: rgba(217,165,20,0.08);
        border: 1px solid rgba(217,165,20,0.25);
        border-radius: 15px;
        padding: 14px;
        margin-top: 20px;
        color: #D7D8DC;
        font-size: 13px;
        line-height: 1.7;
    }


    /* titles */

    .section-label {
        color: #D9A514;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-top: 10px;
    }

    .section-title {
        color: #F7F3E8;
        font-size: 29px;
        font-weight: 900;
        margin-top: 3px;
        margin-bottom: 14px;
    }

    .section-description {
        color: #9FA2AA;
        font-size: 14px;
        line-height: 1.7;
        margin-top: -7px;
        margin-bottom: 17px;
    }


    /* metric cards */

    .metric-card {
        position: relative;
        overflow: hidden;

        background:
            linear-gradient(
                145deg,
                #191B20 0%,
                #121419 100%
            );

        border: 1px solid rgba(217,165,20,0.20);
        border-radius: 20px;
        padding: 21px;

        min-height: 145px;

        box-shadow:
            0 12px 28px rgba(0,0,0,0.22),
            inset 0 1px 0 rgba(255,255,255,0.03);
    }

    .metric-card:after {
        content: "";
        position: absolute;
        right: -22px;
        top: -22px;
        width: 90px;
        height: 90px;
        background: rgba(217,165,20,0.08);
        border-radius: 50%;
    }

    .metric-icon {
        font-size: 22px;
        margin-bottom: 12px;
    }

    .metric-label {
        color: #9DA0A8;
        font-size: 13px;
        margin-bottom: 6px;
    }

    .metric-value {
        color: #F3CE69;
        font-size: 30px;
        font-weight: 900;
        line-height: 1.1;
    }

    .metric-small {
        color: #747780;
        font-size: 11px;
        margin-top: 7px;
    }


    /* story cards */

    .story-card {
        background:
            linear-gradient(
                145deg,
                #181A1F 0%,
                #111318 100%
            );

        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 22px;
        min-height: 180px;

        box-shadow: 0 10px 25px rgba(0,0,0,0.20);
    }

    .story-number {
        display: inline-flex;
        width: 36px;
        height: 36px;
        align-items: center;
        justify-content: center;

        background: #D9A514;
        color: #090A0D;
        border-radius: 11px;

        font-size: 15px;
        font-weight: 900;
        margin-bottom: 13px;
    }

    .story-title {
        color: #F7F3E8;
        font-size: 19px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .story-text {
        color: #9FA2AA;
        font-size: 13px;
        line-height: 1.7;
    }


    /* badges */

    .badge {
        display: inline-block;
        border-radius: 100px;
        padding: 7px 12px;
        margin-right: 6px;
        margin-bottom: 8px;

        font-size: 12px;
        font-weight: 800;
    }

    .badge-gold {
        background: rgba(217,165,20,0.13);
        color: #F3CE69;
        border: 1px solid rgba(217,165,20,0.33);
    }

    .badge-green {
        background: rgba(79,168,121,0.13);
        color: #82D8A8;
        border: 1px solid rgba(79,168,121,0.31);
    }

    .badge-red {
        background: rgba(213,103,103,0.13);
        color: #F09A9A;
        border: 1px solid rgba(213,103,103,0.31);
    }

    .badge-gray {
        background: rgba(165,168,176,0.11);
        color: #CDD0D6;
        border: 1px solid rgba(165,168,176,0.20);
    }


    /* callouts */

    .callout {
        background:
            linear-gradient(
                135deg,
                rgba(217,165,20,0.12),
                rgba(217,165,20,0.04)
            );

        border-left: 4px solid #D9A514;
        border-radius: 14px;
        padding: 17px 19px;
        color: #D9DADD;
        line-height: 1.7;
        font-size: 14px;
        margin-top: 12px;
        margin-bottom: 15px;
    }

    .callout strong {
        color: #F3CE69;
    }


    /* chart container look */

    div[data-testid="stPlotlyChart"] {
        background: #15171C;
        border: 1px solid rgba(255,255,255,0.055);
        border-radius: 18px;
        padding: 5px;

        box-shadow: 0 10px 28px rgba(0,0,0,0.20);
    }


    /* tabs */

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #111318;
        padding: 7px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    .stTabs [data-baseweb="tab"] {
        color: #9FA2AA;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 800;
    }

    .stTabs [aria-selected="true"] {
        color: #090A0D !important;
        background: #D9A514 !important;
    }


    /* dataframe */

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(217,165,20,0.15);
        border-radius: 15px;
        overflow: hidden;
    }


    /* progress bars */

    div[data-testid="stProgress"] > div > div {
        background-color: #D9A514;
    }


    /* normal markdown colors */

    h1, h2, h3 {
        color: #F7F3E8 !important;
    }

    p {
        color: #C7CBD3;
    }

    hr {
        border-color: rgba(255,255,255,0.07);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# reading the data
# --------------------------------------------------

@st.cache_data
def load_data():

    # i use gold_final because it already have the cleaning
    # also it have the new columns that i made in the notebook

    data = pd.read_csv("gold_final.csv")

    data["Date"] = pd.to_datetime(data["Date"])


    # just making sure year and month is numbers

    data["Year"] = data["Year"].astype(int)
    data["Month"] = data["Month"].astype(int)


    # csv can return True and False like text
    # this make them boolean again

    for col in [
        "Has_Event",
        "Inflation_Event",
        "Fed_Event"
    ]:

        if col in data.columns and data[col].dtype != bool:

            data[col] = (
                data[col]
                .astype(str)
                .str.lower()
                .map({
                    "true": True,
                    "false": False,
                    "1": True,
                    "0": False
                })
                .fillna(False)
            )


    # if any new column is missing i make it again
    # this is only to stop the app from breaking

    if "Abs_Change" not in data.columns:

        data["Abs_Change"] = (
            data["Change_percent"]
            .abs()
        )


    if "Has_Event" not in data.columns:

        data["Has_Event"] = (
            data["Event_Count"] > 0
        )


    if "Direction" not in data.columns:

        data["Direction"] = "Down"

        data.loc[
            data["Change_percent"] > 0,
            "Direction"
        ] = "Up"


    if "Event_Group" not in data.columns:

        data["Event_Group"] = "No Event"

        data.loc[
            data["Event_Count"].between(1, 3),
            "Event_Group"
        ] = "1-3 Events"

        data.loc[
            data["Event_Count"] >= 4,
            "Event_Group"
        ] = "4+ Events"


    # this name is only for charts
    # it is easier than showing true and false

    data["Event_Label"] = (
        data["Has_Event"]
        .map({
            True: "Event Days",
            False: "No Event Days"
        })
    )


    # month names is easier than only month numbers

    data["Month_Name"] = (
        data["Date"]
        .dt.strftime("%b")
    )


    # simple movement groups for another visual

    data["Movement_Level"] = pd.cut(
        data["Abs_Change"],
        bins=[
            -0.01,
            0.50,
            1.00,
            float("inf")
        ],
        labels=[
            "Low movement",
            "Medium movement",
            "High movement"
        ]
    )


    return data


data = load_data()


# --------------------------------------------------
# sidebar design and filters
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="side-brand">

            <div class="side-logo">
                GOLD MARKET LAB
            </div>

            <div class="side-title">
                Explore
            </div>

            <div class="side-description">
                Change one filter at a time and see how the story,
                numbers and charts react to your choice.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("### 🗓️ Time")

    years = sorted(
        data["Year"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_year = st.selectbox(
        "Choose the year",
        ["All"] + years
    )


    st.markdown("### ⚡ Economic events")

    event_choice = st.selectbox(
        "Choose event days",
        [
            "All days",
            "Event days",
            "No event days"
        ]
    )


    st.markdown("### 📈 Price direction")

    direction_choice = st.selectbox(
        "Choose gold direction",
        [
            "All directions",
            "Up",
            "Down"
        ]
    )


    st.markdown(
        """
        <div class="side-hint">

            <strong style="color:#F3CE69;">
                💡 Small tip
            </strong>

            <br><br>

            Start with <b>All</b>, then change only one option.
            It will be easier to understand what changed in the dashboard.

        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# apply filters
# --------------------------------------------------

filtered = data.copy()


if selected_year != "All":

    filtered = filtered[
        filtered["Year"] == selected_year
    ]


if event_choice == "Event days":

    filtered = filtered[
        filtered["Has_Event"] == True
    ]


elif event_choice == "No event days":

    filtered = filtered[
        filtered["Has_Event"] == False
    ]


if direction_choice != "All directions":

    filtered = filtered[
        filtered["Direction"] == direction_choice
    ]


if filtered.empty:

    st.warning(
        "There is no data for these filters. "
        "Change one option from the sidebar."
    )

    st.stop()


# --------------------------------------------------
# all calculations
# --------------------------------------------------

filtered = filtered.sort_values("Date").copy()


average_price = filtered["Price"].mean()
highest_price = filtered["Price"].max()
lowest_price = filtered["Price"].min()
average_movement = filtered["Abs_Change"].mean()

days_shown = len(filtered)


start_price = filtered.iloc[0]["Price"]
end_price = filtered.iloc[-1]["Price"]


if start_price != 0:

    full_price_change = (
        (end_price - start_price)
        / start_price
    ) * 100

else:

    full_price_change = 0


event_day_percent = (
    filtered["Has_Event"]
    .mean()
    * 100
)


up_day_percent = (
    (filtered["Direction"] == "Up")
    .mean()
    * 100
)


down_day_percent = 100 - up_day_percent


volume_movement_corr = (
    filtered[
        [
            "Vol_K",
            "Abs_Change"
        ]
    ]
    .corr()
    .iloc[0, 1]
)


if pd.isna(volume_movement_corr):

    volume_movement_corr = 0


year_movement = (
    filtered
    .groupby("Year")["Abs_Change"]
    .mean()
)


best_year = (
    year_movement.idxmax()
    if not year_movement.empty
    else "N/A"
)


month_movement = (
    filtered
    .groupby("Month")["Abs_Change"]
    .mean()
)


best_month = (
    month_movement.idxmax()
    if not month_movement.empty
    else "N/A"
)


event_group_movement = (
    filtered
    .groupby("Event_Group")["Abs_Change"]
    .mean()
)


best_event_group = (
    event_group_movement.idxmax()
    if not event_group_movement.empty
    else "N/A"
)


# --------------------------------------------------
# helper for all plotly charts
# --------------------------------------------------

def luxury_chart(
    fig,
    height=390,
    show_legend=True
):

    # i use the same chart design everywhere
    # because i dont want every chart look like another website

    fig.update_layout(

        template="plotly_dark",

        height=height,

        paper_bgcolor="#15171C",
        plot_bgcolor="#15171C",

        font=dict(
            family="Arial",
            color="#D6D7DA",
            size=12
        ),

        margin=dict(
            l=25,
            r=25,
            t=30,
            b=30
        ),

        legend=dict(
            title="",
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#D6D7DA"
            )
        ),

        showlegend=show_legend,

        hoverlabel=dict(
            bgcolor="#090A0D",
            font_color="#F7F3E8",
            bordercolor="#D9A514"
        )
    )


    fig.update_xaxes(

        showgrid=False,

        linecolor="rgba(255,255,255,0.08)",

        tickfont=dict(
            color="#9FA2AA"
        ),

        title_font=dict(
            color="#9FA2AA"
        )
    )


    fig.update_yaxes(

        gridcolor="rgba(255,255,255,0.055)",

        zerolinecolor="rgba(255,255,255,0.08)",

        tickfont=dict(
            color="#9FA2AA"
        ),

        title_font=dict(
            color="#9FA2AA"
        )
    )


    return fig


# --------------------------------------------------
# hero
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            INTERACTIVE EDA • GOLD MARKET
        </div>

        <div class="hero-title">
            Follow the <span class="hero-gold">Gold Story</span>
        </div>

        <div class="hero-text">

            This dashboard does not only place many charts on one page.
            It walks through the data as a simple story:

            what happened to gold prices, when the strongest movement appeared,
            whether economic events looked different, and what other patterns
            can be noticed from volume and direction.

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# story map
# --------------------------------------------------

st.markdown(
    """
    <div class="section-label">
        Dashboard journey
    </div>

    <div class="section-title">
        The questions this dashboard answers
    </div>
    """,
    unsafe_allow_html=True
)


story1, story2, story3, story4 = st.columns(4)


with story1:

    st.markdown(
        """
        <div class="story-card">

            <div class="story-number">1</div>

            <div class="story-title">
                What happened?
            </div>

            <div class="story-text">
                Follow the price through time and see its general direction,
                distribution and biggest changes.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with story2:

    st.markdown(
        """
        <div class="story-card">

            <div class="story-number">2</div>

            <div class="story-title">
                When was it strongest?
            </div>

            <div class="story-text">
                Compare years and months to find when gold was moving
                more than normal.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with story3:

    st.markdown(
        """
        <div class="story-card">

            <div class="story-number">3</div>

            <div class="story-title">
                Did events matter?
            </div>

            <div class="story-text">
                Compare event days, no-event days, inflation days
                and Fed-related days.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with story4:

    st.markdown(
        """
        <div class="story-card">

            <div class="story-number">4</div>

            <div class="story-title">
                What patterns appeared?
            </div>

            <div class="story-text">
                Explore volume, direction, event groups and the strongest
                movement days.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# metrics
# --------------------------------------------------

st.markdown(
    """
    <div class="section-label">
        Live summary
    </div>

    <div class="section-title">
        Quick numbers from your current filters
    </div>

    <div class="section-description">
        These cards automatically change when any filter is changed.
    </div>
    """,
    unsafe_allow_html=True
)


metric1, metric2, metric3, metric4 = st.columns(4)


with metric1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon">💰</div>

            <div class="metric-label">
                Average Price
            </div>

            <div class="metric-value">
                {average_price:,.2f}
            </div>

            <div class="metric-small">
                Mean price in the selected rows
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with metric2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon">🏆</div>

            <div class="metric-label">
                Highest Price
            </div>

            <div class="metric-value">
                {highest_price:,.2f}
            </div>

            <div class="metric-small">
                Lowest price was {lowest_price:,.2f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with metric3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon">⚡</div>

            <div class="metric-label">
                Average Movement
            </div>

            <div class="metric-value">
                {average_movement:.2f}%
            </div>

            <div class="metric-small">
                Absolute movement, up or down
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with metric4:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon">📅</div>

            <div class="metric-label">
                Days Shown
            </div>

            <div class="metric-value">
                {days_shown:,}
            </div>

            <div class="metric-small">
                Rows remaining after the filters
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# visual progress
# --------------------------------------------------

st.markdown("### Visual snapshot")


progress1, progress2, progress3 = st.columns(3)


with progress1:

    st.markdown(
        f"""
        <span class="badge badge-gold">
            ⚡ Event days: {event_day_percent:.1f}%
        </span>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(
            100,
            max(
                0,
                int(round(event_day_percent))
            )
        )
    )


with progress2:

    st.markdown(
        f"""
        <span class="badge badge-green">
            📈 Up days: {up_day_percent:.1f}%
        </span>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(
            100,
            max(
                0,
                int(round(up_day_percent))
            )
        )
    )


with progress3:

    change_badge = (
        "badge-green"
        if full_price_change >= 0
        else "badge-red"
    )

    change_icon = (
        "↗"
        if full_price_change >= 0
        else "↘"
    )

    st.markdown(
        f"""
        <span class="badge {change_badge}">
            {change_icon} First to last price: {full_price_change:.1f}%
        </span>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(
            100,
            max(
                0,
                int(round(abs(full_price_change)))
            )
        )
    )


# --------------------------------------------------
# tabs as the story
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "① What happened?",
        "② When strongest?",
        "③ Did events matter?",
        "④ Patterns",
        "⑤ Data"
    ]
)


# ==================================================
# tab 1 - what happened
# ==================================================

with tab1:

    st.markdown(
        """
        <div class="section-label">
            Chapter one
        </div>

        <div class="section-title">
            What happened to gold prices?
        </div>

        <div class="section-description">
            First, look at the whole journey before trying to explain any reason.
        </div>
        """,
        unsafe_allow_html=True
    )


    price_col, share_col = st.columns(
        [
            2,
            1
        ]
    )


    with price_col:

        fig_price = px.area(

            filtered,

            x="Date",

            y="Price",

            labels={
                "Date": "Date",
                "Price": "Gold Price"
            }
        )


        fig_price.update_traces(

            line=dict(
                color=GOLD,
                width=2.4
            ),

            fillcolor="rgba(217,165,20,0.16)",

            hovertemplate=(
                "<b>%{x|%Y-%m-%d}</b>"
                "<br>Price: %{y:,.2f}"
                "<extra></extra>"
            )
        )


        luxury_chart(
            fig_price,
            height=440,
            show_legend=False
        )


        st.plotly_chart(
            fig_price,
            use_container_width=True
        )


    with share_col:

        event_share_data = (

            filtered["Event_Label"]

            .value_counts()

            .reset_index()
        )


        event_share_data.columns = [
            "Day Type",
            "Days"
        ]


        fig_share = px.pie(

            event_share_data,

            names="Day Type",

            values="Days",

            hole=0.62,

            color="Day Type",

            color_discrete_map={
                "Event Days": GOLD,
                "No Event Days": "#555A65"
            }
        )


        fig_share.update_traces(

            textposition="inside",

            textinfo="percent",

            hovertemplate=(
                "<b>%{label}</b>"
                "<br>Days: %{value}"
                "<br>Share: %{percent}"
                "<extra></extra>"
            )
        )


        luxury_chart(
            fig_share,
            height=440,
            show_legend=True
        )


        st.plotly_chart(
            fig_share,
            use_container_width=True
        )


    distribution_col, direction_col = st.columns(2)


    with distribution_col:

        st.markdown("### Price distribution")


        fig_distribution = px.histogram(

            filtered,

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


        luxury_chart(
            fig_distribution,
            height=365
        )


        st.plotly_chart(
            fig_distribution,
            use_container_width=True
        )


    with direction_col:

        st.markdown("### Up days vs down days")


        direction_data = (

            filtered["Direction"]

            .value_counts()

            .reset_index()
        )


        direction_data.columns = [
            "Direction",
            "Days"
        ]


        fig_direction = px.pie(

            direction_data,

            names="Direction",

            values="Days",

            hole=0.55,

            color="Direction",

            color_discrete_map={
                "Up": GREEN,
                "Down": RED
            }
        )


        fig_direction.update_traces(
            textinfo="percent+label"
        )


        luxury_chart(
            fig_direction,
            height=365
        )


        st.plotly_chart(
            fig_direction,
            use_container_width=True
        )


    st.markdown(
        f"""
        <div class="callout">

            <strong>📌 What i notice:</strong>

            The first selected price is <strong>{start_price:,.2f}</strong>
            and the last selected price is <strong>{end_price:,.2f}</strong>.

            The change between them is around
            <strong>{full_price_change:.1f}%</strong>.

            This only describes what happened in the selected period.
            It does not tell the reason alone.

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# tab 2 - strongest timing
# ==================================================

with tab2:

    st.markdown(
        """
        <div class="section-label">
            Chapter two
        </div>

        <div class="section-title">
            When was the movement strongest?
        </div>

        <div class="section-description">
            Now the data is divided by year and month to see when the price was moving more.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <span class="badge badge-gold">
            🏆 Strongest year: {best_year}
        </span>

        <span class="badge badge-gold">
            📆 Strongest month number: {best_month}
        </span>
        """,
        unsafe_allow_html=True
    )


    year_col, month_col = st.columns(2)


    with year_col:

        year_data = (

            filtered

            .groupby("Year")["Abs_Change"]

            .mean()

            .reset_index()
        )


        fig_year = px.bar(

            year_data,

            x="Year",

            y="Abs_Change",

            color="Abs_Change",

            text_auto=".2f",

            color_continuous_scale=[
                "#4E5360",
                LIGHT_GOLD,
                GOLD
            ],

            labels={
                "Abs_Change": "Average Movement %"
            }
        )


        fig_year.update_traces(
            textposition="outside"
        )


        luxury_chart(
            fig_year,
            height=390,
            show_legend=False
        )


        fig_year.update_layout(
            coloraxis_showscale=False
        )


        st.plotly_chart(
            fig_year,
            use_container_width=True
        )


    with month_col:

        month_data = (

            filtered

            .groupby(
                [
                    "Month",
                    "Month_Name"
                ]
            )["Abs_Change"]

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
                "#4E5360",
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


        luxury_chart(
            fig_month,
            height=390,
            show_legend=False
        )


        fig_month.update_layout(
            coloraxis_showscale=False
        )


        st.plotly_chart(
            fig_month,
            use_container_width=True
        )


    st.markdown("### Movement heatmap")


    heat_data = filtered.pivot_table(

        index="Year",

        columns="Month",

        values="Abs_Change",

        aggfunc="mean"
    )


    fig_heat = px.imshow(

        heat_data,

        text_auto=".2f",

        aspect="auto",

        color_continuous_scale=[
            [
                0,
                "#23262D"
            ],
            [
                0.5,
                "#9B7611"
            ],
            [
                1,
                "#F3CE69"
            ]
        ],

        labels={
            "x": "Month",
            "y": "Year",
            "color": "Movement"
        }
    )


    luxury_chart(
        fig_heat,
        height=350,
        show_legend=False
    )


    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )


    top_five_time = (

        filtered

        .nlargest(
            5,
            "Abs_Change"
        )

        [
            [
                "Date",
                "Abs_Change",
                "Direction",
                "Event_Group"
            ]
        ]

        .copy()
    )


    top_five_time["Date"] = (
        top_five_time["Date"]
        .dt.strftime("%Y-%m-%d")
    )


    st.markdown(
        f"""
        <div class="callout">

            <strong>🔥 Strong timing result:</strong>

            In the current filters,
            <strong>{best_year}</strong> has the highest yearly average movement,
            while month number <strong>{best_month}</strong> has the highest
            monthly average.

            The heatmap makes it easier to see whether the result came from
            one year only or repeated in different years.

        </div>
        """,
        unsafe_allow_html=True
    )


    st.dataframe(
        top_five_time,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# tab 3 - events
# ==================================================

with tab3:

    st.markdown(
        """
        <div class="section-label">
            Chapter three
        </div>

        <div class="section-title">
            Did economic events look different?
        </div>

        <div class="section-description">
            These charts compare the average movement, but they still do not prove that an event caused the price.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <span class="badge badge-gold">
            ⚡ Highest event group: {best_event_group}
        </span>

        <span class="badge badge-gray">
            📊 Event day share: {event_day_percent:.1f}%
        </span>
        """,
        unsafe_allow_html=True
    )


    group_data = (

        filtered

        .groupby("Event_Group")["Abs_Change"]

        .mean()

        .reset_index()
    )


    group_order = [
        "No Event",
        "1-3 Events",
        "4+ Events"
    ]


    group_data["Event_Group"] = pd.Categorical(

        group_data["Event_Group"],

        categories=group_order,

        ordered=True
    )


    group_data = group_data.sort_values(
        "Event_Group"
    )


    fig_group = px.bar(

        group_data,

        x="Event_Group",

        y="Abs_Change",

        color="Event_Group",

        text_auto=".2f",

        color_discrete_map={
            "No Event": "#555A65",
            "1-3 Events": GOLD,
            "4+ Events": DARK_GOLD
        },

        labels={
            "Event_Group": "Event Group",
            "Abs_Change": "Average Movement %"
        }
    )


    fig_group.update_traces(
        textposition="outside"
    )


    luxury_chart(
        fig_group,
        height=390,
        show_legend=False
    )


    st.plotly_chart(
        fig_group,
        use_container_width=True
    )


    compare1, compare2, compare3 = st.columns(3)


    with compare1:

        event_compare = (

            filtered

            .groupby("Has_Event")["Abs_Change"]

            .mean()

            .reset_index()
        )


        event_compare["Type"] = (
            event_compare["Has_Event"]
            .map({
                True: "Event Days",
                False: "No Event Days"
            })
        )


        fig_event_compare = px.bar(

            event_compare,

            x="Type",

            y="Abs_Change",

            color="Type",

            text_auto=".2f",

            color_discrete_map={
                "Event Days": GOLD,
                "No Event Days": "#555A65"
            }
        )


        fig_event_compare.update_traces(
            textposition="outside"
        )


        luxury_chart(
            fig_event_compare,
            height=330,
            show_legend=False
        )


        st.plotly_chart(
            fig_event_compare,
            use_container_width=True
        )


    with compare2:

        inflation_compare = (

            filtered

            .groupby("Inflation_Event")["Abs_Change"]

            .mean()

            .reset_index()
        )


        inflation_compare["Type"] = (

            inflation_compare["Inflation_Event"]

            .map({
                True: "Inflation Days",
                False: "Other Days"
            })
        )


        fig_inflation = px.bar(

            inflation_compare,

            x="Type",

            y="Abs_Change",

            color="Type",

            text_auto=".2f",

            color_discrete_map={
                "Inflation Days": LIGHT_GOLD,
                "Other Days": "#555A65"
            }
        )


        fig_inflation.update_traces(
            textposition="outside"
        )


        luxury_chart(
            fig_inflation,
            height=330,
            show_legend=False
        )


        st.plotly_chart(
            fig_inflation,
            use_container_width=True
        )


    with compare3:

        fed_compare = (

            filtered

            .groupby("Fed_Event")["Abs_Change"]

            .mean()

            .reset_index()
        )


        fed_compare["Type"] = (

            fed_compare["Fed_Event"]

            .map({
                True: "Fed Days",
                False: "Other Days"
            })
        )


        fig_fed = px.bar(

            fed_compare,

            x="Type",

            y="Abs_Change",

            color="Type",

            text_auto=".2f",

            color_discrete_map={
                "Fed Days": DARK_GOLD,
                "Other Days": "#555A65"
            }
        )


        fig_fed.update_traces(
            textposition="outside"
        )


        luxury_chart(
            fig_fed,
            height=330,
            show_legend=False
        )


        st.plotly_chart(
            fig_fed,
            use_container_width=True
        )


    st.markdown(
        f"""
        <div class="callout">

            <strong>⚠️ How to read this:</strong>

            The group with the highest average movement is
            <strong>{best_event_group}</strong>.

            This means this group looked higher in the selected data.
            It does not mean the events were definitely the reason.

            The event result should be read with the time charts and the
            number of available days, not alone.

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# tab 4 - other patterns
# ==================================================

with tab4:

    st.markdown(
        """
        <div class="section-label">
            Chapter four
        </div>

        <div class="section-title">
            What other patterns appeared?
        </div>

        <div class="section-description">
            This part checks volume, movement strength and whether the relationship looked strong or weak.
        </div>
        """,
        unsafe_allow_html=True
    )


    scatter_col, gauge_col = st.columns(
        [
            2,
            1
        ]
    )


    with scatter_col:

        fig_scatter = px.scatter(

            filtered,

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
                "No Event": "#555A65",
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
                opacity=0.70,
                line=dict(
                    width=0.5,
                    color="#090A0D"
                )
            )
        )


        luxury_chart(
            fig_scatter,
            height=450,
            show_legend=True
        )


        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )


    with gauge_col:

        fig_gauge = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=volume_movement_corr,

                number={
                    "valueformat": ".2f",
                    "font": {
                        "color": "#F3CE69",
                        "size": 42
                    }
                },

                title={
                    "text": (
                        "Volume and Movement"
                        "<br><span style='font-size:13px;color:#9FA2AA'>"
                        "Correlation"
                        "</span>"
                    ),

                    "font": {
                        "color": "#F7F3E8"
                    }
                },

                gauge={

                    "axis": {
                        "range": [
                            -1,
                            1
                        ],

                        "tickcolor": "#9FA2AA"
                    },

                    "bar": {
                        "color": GOLD,
                        "thickness": 0.30
                    },

                    "bgcolor": "#15171C",

                    "borderwidth": 0,

                    "steps": [

                        {
                            "range": [
                                -1,
                                -0.30
                            ],
                            "color": "rgba(213,103,103,0.24)"
                        },

                        {
                            "range": [
                                -0.30,
                                0.30
                            ],
                            "color": "rgba(165,168,176,0.16)"
                        },

                        {
                            "range": [
                                0.30,
                                1
                            ],
                            "color": "rgba(79,168,121,0.20)"
                        }
                    ]
                }
            )
        )


        luxury_chart(
            fig_gauge,
            height=450,
            show_legend=False
        )


        st.plotly_chart(
            fig_gauge,
            use_container_width=True
        )


    movement_level_data = (

        filtered["Movement_Level"]

        .value_counts()

        .reset_index()
    )


    movement_level_data.columns = [
        "Movement Level",
        "Days"
    ]


    fig_levels = px.bar(

        movement_level_data,

        x="Movement Level",

        y="Days",

        color="Movement Level",

        text_auto=True,

        color_discrete_map={
            "Low movement": "#555A65",
            "Medium movement": LIGHT_GOLD,
            "High movement": RED
        }
    )


    luxury_chart(
        fig_levels,
        height=350,
        show_legend=False
    )


    st.plotly_chart(
        fig_levels,
        use_container_width=True
    )


    if volume_movement_corr >= 0.50:

        correlation_text = (
            "The relationship looks positive and fairly strong."
        )


    elif volume_movement_corr >= 0.20:

        correlation_text = (
            "The relationship is positive, but still not very strong."
        )


    elif volume_movement_corr <= -0.20:

        correlation_text = (
            "The relationship is negative, but it does not prove a cause."
        )


    else:

        correlation_text = (
            "The relationship is weak and close to zero."
        )


    st.markdown(
        f"""
        <div class="callout">

            <strong>🔎 Pattern result:</strong>

            The correlation between volume and gold movement is
            <strong>{volume_movement_corr:.2f}</strong>.

            {correlation_text}

            Points are still spread in the scatter plot, so volume alone
            cannot explain every large movement.

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# tab 5 - data table
# ==================================================

with tab5:

    st.markdown(
        """
        <div class="section-label">
            Final chapter
        </div>

        <div class="section-title">
            Inspect the strongest movement days
        </div>

        <div class="section-description">
            The table gives the exact dates and values behind the visual results.
        </div>
        """,
        unsafe_allow_html=True
    )


    top_days = (

        filtered

        .nlargest(
            10,
            "Abs_Change"
        )

        [
            [
                "Date",
                "Price",
                "Change_percent",
                "Abs_Change",
                "Event_Count",
                "Event_Group",
                "Direction"
            ]
        ]

        .copy()
    )


    top_days["Date"] = (
        top_days["Date"]
        .dt.strftime("%Y-%m-%d")
    )


    top_days = (
        top_days

        .reset_index(
            drop=True
        )

        .rename(
            columns={
                "Change_percent": "Change Percent",
                "Abs_Change": "Absolute Change",
                "Event_Count": "Event Count",
                "Event_Group": "Event Group"
            }
        )
    )


    st.dataframe(

        top_days,

        use_container_width=True,

        hide_index=True
    )


    st.markdown(
        """
        <div class="callout">

            <strong>📋 Why this table is here:</strong>

            The charts summarize the data, but this table shows the real
            observations behind the results.

            It can be used to check if the highest movements happened on
            event days, normal days, up days or down days.

        </div>
        """,
        unsafe_allow_html=True
    )


    with st.expander(
        "🔍 Open all filtered rows"
    ):

        full_filtered = filtered.copy()


        full_filtered["Date"] = (

            full_filtered["Date"]

            .dt.strftime("%Y-%m-%d")
        )


        st.dataframe(

            full_filtered,

            use_container_width=True,

            hide_index=True
        )


    csv_file = (

        filtered

        .to_csv(
            index=False
        )

        .encode("utf-8")
    )


    st.download_button(

        label="⬇️ Download the filtered data",

        data=csv_file,

        file_name="filtered_gold_data.csv",

        mime="text/csv"
    )


# --------------------------------------------------
# ending note
# --------------------------------------------------

st.markdown("---")


st.markdown(
    """
    <div class="callout">

        <strong>Final reminder:</strong>

        This dashboard is used to explore patterns, compare groups and make
        the EDA easier to understand.

        It does not prove that an economic event directly caused every gold
        price increase or decrease.

    </div>
    """,
    unsafe_allow_html=True
)
