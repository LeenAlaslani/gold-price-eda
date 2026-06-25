import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from textwrap import dedent


# --------------------------------------------------
# page settings
# --------------------------------------------------

st.set_page_config(
    page_title="Gold Price EDA Dashboard",
    page_icon="✨",
    layout="wide"
)


# --------------------------------------------------
# colors
# --------------------------------------------------

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


# --------------------------------------------------
# html helper
# --------------------------------------------------

# i use st.html because before the html was showing like normal code
# dedent remove the big spaces from the beginning of the html lines

def show_html(code):
    st.html(dedent(code))


# --------------------------------------------------
# full dashboard css
# --------------------------------------------------

show_html(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(217,165,20,0.09),
                transparent 28%
            ),
            #090A0D;

        color: #F7F3E8;
    }


    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1500px;
    }


    [data-testid="stHeader"] {
        background: rgba(9,10,13,0.92);
        border-bottom: 1px solid rgba(217,165,20,0.12);
    }


    [data-testid="stToolbar"] {
        color: #F7F3E8;
    }


    /* sidebar */

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(
                circle at top left,
                rgba(217,165,20,0.09),
                transparent 30%
            ),
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
        min-height: 48px;
    }


    section[data-testid="stSidebar"]
    div[data-baseweb="select"] svg {
        fill: #D9A514;
    }


    /* sidebar design */

    .side-brand {
        background:
            radial-gradient(
                circle at top right,
                rgba(217,165,20,0.26),
                transparent 40%
            ),
            linear-gradient(
                145deg,
                #191B20,
                #111216
            );

        border: 1px solid rgba(217,165,20,0.30);
        border-radius: 22px;
        padding: 21px;
        margin-bottom: 22px;

        box-shadow:
            0 15px 35px rgba(0,0,0,0.28),
            inset 0 1px 0 rgba(255,255,255,0.03);
    }


    .side-logo {
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #D9A514;
        margin-bottom: 9px;
    }


    .side-title {
        font-size: 30px;
        font-weight: 900;
        color: #F7F3E8;
        margin-bottom: 8px;
    }


    .side-description {
        font-size: 13px;
        line-height: 1.75;
        color: #B8BBC3;
    }


    .side-section {
        color: #F3CE69;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;

        margin-top: 22px;
        margin-bottom: 5px;
    }


    .side-hint {
        background:
            linear-gradient(
                135deg,
                rgba(217,165,20,0.13),
                rgba(217,165,20,0.04)
            );

        border: 1px solid rgba(217,165,20,0.27);
        border-radius: 16px;

        padding: 15px;
        margin-top: 23px;

        color: #D7D8DC;
        font-size: 13px;
        line-height: 1.7;
    }


    /* hero */

    .hero {
        position: relative;
        overflow: hidden;

        background:
            radial-gradient(
                circle at 89% 7%,
                rgba(217,165,20,0.25),
                transparent 29%
            ),
            linear-gradient(
                135deg,
                #121318 0%,
                #1B1D22 58%,
                #101115 100%
            );

        border: 1px solid rgba(217,165,20,0.30);
        border-radius: 28px;

        padding: 38px;
        margin-bottom: 25px;

        box-shadow:
            0 20px 50px rgba(0,0,0,0.38),
            inset 0 1px 0 rgba(255,255,255,0.04);
    }


    .hero-badge {
        display: inline-block;

        background: rgba(217,165,20,0.12);
        color: #F3CE69;

        border: 1px solid rgba(217,165,20,0.42);
        border-radius: 100px;

        padding: 7px 13px;
        margin-bottom: 15px;

        font-size: 11px;
        font-weight: 900;
        letter-spacing: 1.2px;
    }


    .hero-title {
        color: #F7F3E8;

        font-size: 47px;
        line-height: 1.08;
        font-weight: 900;

        margin-bottom: 13px;
    }


    .hero-gold {
        color: #D9A514;
    }


    .hero-text {
        color: #C7CBD3;

        font-size: 16px;
        line-height: 1.85;

        max-width: 930px;
    }


    /* section heading */

    .section-label {
        color: #D9A514;

        font-size: 11px;
        font-weight: 900;
        letter-spacing: 1.5px;
        text-transform: uppercase;

        margin-top: 14px;
    }


    .section-title {
        color: #F7F3E8;

        font-size: 29px;
        font-weight: 900;

        margin-top: 4px;
        margin-bottom: 14px;
    }


    .section-description {
        color: #9FA2AA;

        font-size: 14px;
        line-height: 1.7;

        margin-top: -7px;
        margin-bottom: 18px;
    }


    /* story cards */

    .story-card {
        background:
            radial-gradient(
                circle at top right,
                rgba(217,165,20,0.08),
                transparent 40%
            ),
            linear-gradient(
                145deg,
                #181A1F 0%,
                #111318 100%
            );

        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 21px;

        padding: 22px;
        min-height: 196px;

        box-shadow:
            0 12px 28px rgba(0,0,0,0.23),
            inset 0 1px 0 rgba(255,255,255,0.03);
    }


    .story-number {
        display: flex;
        width: 38px;
        height: 38px;

        align-items: center;
        justify-content: center;

        background: #D9A514;
        color: #090A0D;

        border-radius: 11px;

        font-size: 15px;
        font-weight: 900;

        margin-bottom: 14px;
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
        line-height: 1.75;
    }


    /* metric cards */

    .metric-card {
        position: relative;
        overflow: hidden;

        background:
            radial-gradient(
                circle at top right,
                rgba(217,165,20,0.10),
                transparent 37%
            ),
            linear-gradient(
                145deg,
                #191B20 0%,
                #121419 100%
            );

        border: 1px solid rgba(217,165,20,0.20);
        border-radius: 21px;

        padding: 21px;
        min-height: 154px;

        box-shadow:
            0 14px 30px rgba(0,0,0,0.24),
            inset 0 1px 0 rgba(255,255,255,0.03);
    }


    .metric-icon {
        font-size: 23px;
        margin-bottom: 12px;
    }


    .metric-label {
        color: #9DA0A8;
        font-size: 13px;
        margin-bottom: 7px;
    }


    .metric-value {
        color: #F3CE69;

        font-size: 31px;
        font-weight: 900;
        line-height: 1.1;
    }


    .metric-small {
        color: #747780;

        font-size: 11px;
        margin-top: 8px;
    }


    /* badges */

    .badge {
        display: inline-block;

        border-radius: 100px;
        padding: 7px 12px;

        margin-right: 6px;
        margin-bottom: 9px;

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


    /* custom progress bars */

    .progress-card {
        background: #15171C;

        border: 1px solid rgba(255,255,255,0.055);
        border-radius: 16px;

        padding: 15px;
        margin-top: 7px;

        box-shadow: 0 9px 23px rgba(0,0,0,0.19);
    }


    .progress-title {
        color: #D6D7DA;
        font-size: 13px;
        font-weight: 800;

        margin-bottom: 10px;
    }


    .progress-track {
        width: 100%;
        height: 9px;

        background: #292C33;
        border-radius: 100px;

        overflow: hidden;
    }


    .progress-fill-gold {
        height: 100%;
        background:
            linear-gradient(
                90deg,
                #8E6B0C,
                #F3CE69
            );

        border-radius: 100px;
    }


    .progress-fill-green {
        height: 100%;
        background:
            linear-gradient(
                90deg,
                #286747,
                #73D39E
            );

        border-radius: 100px;
    }


    .progress-fill-red {
        height: 100%;
        background:
            linear-gradient(
                90deg,
                #873E43,
                #EB8282
            );

        border-radius: 100px;
    }


    .progress-value {
        color: #92959D;
        font-size: 11px;
        margin-top: 7px;
    }


    /* callout */

    .callout {
        background:
            linear-gradient(
                135deg,
                rgba(217,165,20,0.12),
                rgba(217,165,20,0.04)
            );

        border-left: 4px solid #D9A514;
        border-radius: 15px;

        padding: 18px 20px;
        margin-top: 13px;
        margin-bottom: 17px;

        color: #D9DADD;
        font-size: 14px;
        line-height: 1.75;
    }


    .callout strong {
        color: #F3CE69;
    }


    /* chart boxes */

    div[data-testid="stPlotlyChart"] {
        background: #15171C;

        border: 1px solid rgba(255,255,255,0.055);
        border-radius: 18px;

        padding: 5px;

        box-shadow:
            0 12px 30px rgba(0,0,0,0.22);
    }


    /* tabs */

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;

        background: #111318;

        padding: 7px;
        border-radius: 16px;

        border: 1px solid rgba(255,255,255,0.05);
    }


    .stTabs [data-baseweb="tab"] {
        color: #9FA2AA;

        border-radius: 11px;
        padding: 10px 17px;

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
    """
)


# --------------------------------------------------
# reading data
# --------------------------------------------------

@st.cache_data
def load_data():

    # i read the final cleaned file from the notebook

    data = pd.read_csv("gold_final.csv")

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )


    # remove rows only if date was not working

    data = data.dropna(
        subset=["Date"]
    ).copy()


    # making sure year and month is numbers

    if "Year" not in data.columns:
        data["Year"] = data["Date"].dt.year

    if "Month" not in data.columns:
        data["Month"] = data["Date"].dt.month


    data["Year"] = data["Year"].astype(int)
    data["Month"] = data["Month"].astype(int)


    # make the boolean columns true and false again

    boolean_columns = [
        "Has_Event",
        "Inflation_Event",
        "Fed_Event"
    ]


    for col in boolean_columns:

        if col in data.columns:

            data[col] = (
                data[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({
                    "true": True,
                    "false": False,
                    "1": True,
                    "0": False
                })
                .fillna(False)
                .astype(bool)
            )


    # if these columns was missing i make them again

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


    if "Inflation_Event" not in data.columns:
        data["Inflation_Event"] = False


    if "Fed_Event" not in data.columns:
        data["Fed_Event"] = False


    # easier names for the charts

    data["Event_Label"] = (
        data["Has_Event"]
        .map({
            True: "Event Days",
            False: "No Event Days"
        })
    )


    data["Month_Name"] = (
        data["Date"]
        .dt.strftime("%b")
    )


    # i separate movement to simple groups
    # this is only for the visual chart

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
# sidebar
# --------------------------------------------------

with st.sidebar:

    show_html(
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
        """
    )


    show_html(
        """
        <div class="side-section">
            🗓 Time
        </div>
        """
    )


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


    show_html(
        """
        <div class="side-section">
            ⚡ Economic events
        </div>
        """
    )


    event_choice = st.selectbox(
        "Choose event days",
        [
            "All days",
            "Event days",
            "No event days"
        ]
    )


    show_html(
        """
        <div class="side-section">
            📈 Price direction
        </div>
        """
    )


    direction_choice = st.selectbox(
        "Choose gold direction",
        [
            "All directions",
            "Up",
            "Down"
        ]
    )


    show_html(
        """
        <div class="side-hint">

            <strong style="color:#F3CE69;">
                💡 Small tip
            </strong>

            <br><br>

            Start with <b>All</b>, then change only one option.
            This will make the difference more easy to notice.

        </div>
        """
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


filtered = (
    filtered
    .sort_values("Date")
    .copy()
)


# --------------------------------------------------
# calculations
# --------------------------------------------------

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


month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


best_month_name = (
    month_names.get(
        int(best_month),
        str(best_month)
    )
    if best_month != "N/A"
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


event_progress = max(
    0,
    min(
        100,
        event_day_percent
    )
)


up_progress = max(
    0,
    min(
        100,
        up_day_percent
    )
)


corr_progress = max(
    0,
    min(
        100,
        abs(volume_movement_corr) * 100
    )
)


# --------------------------------------------------
# plotly design helper
# --------------------------------------------------

def luxury_chart(
    fig,
    height=390,
    show_legend=True
):

    # same style for all the charts
    # so the app look like one dashboard

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
            t=25,
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


def show_plot(
    fig,
    height=390,
    show_legend=True
):

    luxury_chart(
        fig,
        height=height,
        show_legend=show_legend
    )


    st.plotly_chart(
        fig,
        width="stretch",
        theme=None,
        config={
            "displaylogo": False,
            "responsive": True
        }
    )


# --------------------------------------------------
# hero
# --------------------------------------------------

show_html(
    """
    <div class="hero">

        <div class="hero-badge">
            INTERACTIVE EDA • GOLD MARKET
        </div>

        <div class="hero-title">
            Follow the <span class="hero-gold">Gold Story</span>
        </div>

        <div class="hero-text">

            This dashboard does not only put many charts on one page.
            It walks through the gold data like a simple story:

            what happened to gold prices, when the strongest movement appeared,
            whether economic events looked different, and what other patterns
            appeared from volume and price direction.

        </div>

    </div>
    """
)


# --------------------------------------------------
# journey cards
# --------------------------------------------------

show_html(
    """
    <div class="section-label">
        Dashboard journey
    </div>

    <div class="section-title">
        The questions this dashboard answers
    </div>
    """
)


story1, story2, story3, story4 = st.columns(4)


with story1:

    show_html(
        """
        <div class="story-card">

            <div class="story-number">
                1
            </div>

            <div class="story-title">
                What happened?
            </div>

            <div class="story-text">
                Follow the gold price through time and see its general
                direction, distribution and biggest changes.
            </div>

        </div>
        """
    )


with story2:

    show_html(
        """
        <div class="story-card">

            <div class="story-number">
                2
            </div>

            <div class="story-title">
                When was it strongest?
            </div>

            <div class="story-text">
                Compare the years and months to find when gold was
                moving more than normal.
            </div>

        </div>
        """
    )


with story3:

    show_html(
        """
        <div class="story-card">

            <div class="story-number">
                3
            </div>

            <div class="story-title">
                Did events matter?
            </div>

            <div class="story-text">
                Compare event days, normal days, inflation days
                and Fed related event days.
            </div>

        </div>
        """
    )


with story4:

    show_html(
        """
        <div class="story-card">

            <div class="story-number">
                4
            </div>

            <div class="story-title">
                What patterns appeared?
            </div>

            <div class="story-text">
                Explore volume, direction, movement level and the
                strongest days in the data.
            </div>

        </div>
        """
    )


# --------------------------------------------------
# metric cards
# --------------------------------------------------

show_html(
    """
    <div class="section-label">
        Live summary
    </div>

    <div class="section-title">
        Quick numbers from your filters
    </div>

    <div class="section-description">
        These cards change automatically when the filters change.
    </div>
    """
)


metric1, metric2, metric3, metric4 = st.columns(4)


with metric1:

    show_html(
        f"""
        <div class="metric-card">

            <div class="metric-icon">
                💰
            </div>

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
        """
    )


with metric2:

    show_html(
        f"""
        <div class="metric-card">

            <div class="metric-icon">
                🏆
            </div>

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
        """
    )


with metric3:

    show_html(
        f"""
        <div class="metric-card">

            <div class="metric-icon">
                ⚡
            </div>

            <div class="metric-label">
                Average Movement
            </div>

            <div class="metric-value">
                {average_movement:.2f}%
            </div>

            <div class="metric-small">
                Movement size, up or down
            </div>

        </div>
        """
    )


with metric4:

    show_html(
        f"""
        <div class="metric-card">

            <div class="metric-icon">
                📅
            </div>

            <div class="metric-label">
                Days Shown
            </div>

            <div class="metric-value">
                {days_shown:,}
            </div>

            <div class="metric-small">
                Rows remaining after filters
            </div>

        </div>
        """
    )


# --------------------------------------------------
# custom visual progress bars
# --------------------------------------------------

show_html(
    """
    <div class="section-label">
        Visual snapshot
    </div>

    <div class="section-title">
        A fast look before opening the story
    </div>
    """
)


progress1, progress2, progress3 = st.columns(3)


with progress1:

    show_html(
        f"""
        <div class="progress-card">

            <div class="progress-title">
                ⚡ Event days
            </div>

            <div class="progress-track">
                <div
                    class="progress-fill-gold"
                    style="width:{event_progress:.1f}%;">
                </div>
            </div>

            <div class="progress-value">
                {event_day_percent:.1f}% of selected days had events
            </div>

        </div>
        """
    )


with progress2:

    show_html(
        f"""
        <div class="progress-card">

            <div class="progress-title">
                📈 Up days
            </div>

            <div class="progress-track">
                <div
                    class="progress-fill-green"
                    style="width:{up_progress:.1f}%;">
                </div>
            </div>

            <div class="progress-value">
                {up_day_percent:.1f}% up and {down_day_percent:.1f}% down
            </div>

        </div>
        """
    )


with progress3:

    show_html(
        f"""
        <div class="progress-card">

            <div class="progress-title">
                🔗 Volume relation strength
            </div>

            <div class="progress-track">
                <div
                    class="progress-fill-gold"
                    style="width:{corr_progress:.1f}%;">
                </div>
            </div>

            <div class="progress-value">
                Absolute correlation strength: {abs(volume_movement_corr):.2f}
            </div>

        </div>
        """
    )


# --------------------------------------------------
# storytelling tabs
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "① What happened?",
        "② When strongest?",
        "③ Did events matter?",
        "④ Other patterns",
        "⑤ Detailed data"
    ]
)


# ==================================================
# tab 1
# ==================================================

with tab1:

    show_html(
        """
        <div class="section-label">
            Chapter one
        </div>

        <div class="section-title">
            What happened to gold prices?
        </div>

        <div class="section-description">
            First i look at the full gold journey before trying to explain any reason.
        </div>
        """
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


        show_plot(
            fig_price,
            height=440,
            show_legend=False
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


        show_plot(
            fig_share,
            height=440,
            show_legend=True
        )


    distribution_col, direction_col = st.columns(2)


    with distribution_col:

        st.subheader(
            "Price Distribution"
        )


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


        show_plot(
            fig_distribution,
            height=365
        )


    with direction_col:

        st.subheader(
            "Up Days vs Down Days"
        )


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


        show_plot(
            fig_direction,
            height=365
        )


    show_html(
        f"""
        <div class="callout">

            <strong>📌 What i notice:</strong>

            The first selected price is <strong>{start_price:,.2f}</strong>
            and the last selected price is <strong>{end_price:,.2f}</strong>.

            The full change between them is around
            <strong>{full_price_change:.1f}%</strong>.

            This describes what happened in the period, but the chart
            alone does not tell the exact reason.

        </div>
        """
    )


# ==================================================
# tab 2
# ==================================================

with tab2:

    show_html(
        """
        <div class="section-label">
            Chapter two
        </div>

        <div class="section-title">
            When was the movement strongest?
        </div>

        <div class="section-description">
            Now i split the data by year and month to see when gold was moving more.
        </div>
        """
    )


    show_html(
        f"""
        <span class="badge badge-gold">
            🏆 Strongest year: {best_year}
        </span>

        <span class="badge badge-gold">
            📆 Strongest month: {best_month_name}
        </span>
        """
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


        fig_year.update_layout(
            coloraxis_showscale=False
        )


        show_plot(
            fig_year,
            height=390,
            show_legend=False
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


        fig_month.update_layout(
            coloraxis_showscale=False
        )


        show_plot(
            fig_month,
            height=390,
            show_legend=False
        )


    st.subheader(
        "Movement Heatmap"
    )


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


    show_plot(
        fig_heat,
        height=350,
        show_legend=False
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


    top_five_time = (
        top_five_time
        .reset_index(
            drop=True
        )
    )


    show_html(
        f"""
        <div class="callout">

            <strong>🔥 Strong timing result:</strong>

            In the current filters,
            <strong>{best_year}</strong> has the highest yearly movement,
            while <strong>{best_month_name}</strong> has the highest
            monthly average.

            The heatmap help me check if this result came from one year
            or appeared in more than one year.

        </div>
        """
    )


    st.dataframe(
        top_five_time,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# tab 3
# ==================================================

with tab3:

    show_html(
        """
        <div class="section-label">
            Chapter three
        </div>

        <div class="section-title">
            Did economic events look different?
        </div>

        <div class="section-description">
            These charts compare average movement, but they dont prove an event caused the movement.
        </div>
        """
    )


    show_html(
        f"""
        <span class="badge badge-gold">
            ⚡ Highest event group: {best_event_group}
        </span>

        <span class="badge badge-gray">
            📊 Event day share: {event_day_percent:.1f}%
        </span>
        """
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


    show_plot(
        fig_group,
        height=390,
        show_legend=False
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
            },

            labels={
                "Abs_Change": "Average Movement %"
            }
        )


        fig_event_compare.update_traces(
            textposition="outside"
        )


        show_plot(
            fig_event_compare,
            height=330,
            show_legend=False
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
            },

            labels={
                "Abs_Change": "Average Movement %"
            }
        )


        fig_inflation.update_traces(
            textposition="outside"
        )


        show_plot(
            fig_inflation,
            height=330,
            show_legend=False
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
            },

            labels={
                "Abs_Change": "Average Movement %"
            }
        )


        fig_fed.update_traces(
            textposition="outside"
        )


        show_plot(
            fig_fed,
            height=330,
            show_legend=False
        )


    show_html(
        f"""
        <div class="callout">

            <strong>⚠️ How i read this:</strong>

            The group with the highest average movement is
            <strong>{best_event_group}</strong>.

            It means this group looked higher in this data.
            It does not mean the events was definitely the reason.

            I should read this with the time charts and group sizes,
            not use this result alone.

        </div>
        """
    )


# ==================================================
# tab 4
# ==================================================

with tab4:

    show_html(
        """
        <div class="section-label">
            Chapter four
        </div>

        <div class="section-title">
            What other patterns appeared?
        </div>

        <div class="section-description">
            This part checks volume, movement strength and if the relationship look strong or weak.
        </div>
        """
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


        show_plot(
            fig_scatter,
            height=450,
            show_legend=True
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


        show_plot(
            fig_gauge,
            height=450,
            show_legend=False
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


    movement_order = [
        "Low movement",
        "Medium movement",
        "High movement"
    ]


    movement_level_data["Movement Level"] = pd.Categorical(
        movement_level_data["Movement Level"],
        categories=movement_order,
        ordered=True
    )


    movement_level_data = (
        movement_level_data
        .sort_values("Movement Level")
    )


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


    show_plot(
        fig_levels,
        height=350,
        show_legend=False
    )


    if volume_movement_corr >= 0.50:

        correlation_text = (
            "The relationship look positive and fairly strong."
        )


    elif volume_movement_corr >= 0.20:

        correlation_text = (
            "The relationship is positive, but it is not very strong."
        )


    elif volume_movement_corr <= -0.20:

        correlation_text = (
            "The relationship is negative, but it does not prove a reason."
        )


    else:

        correlation_text = (
            "The relationship is weak and close to zero."
        )


    show_html(
        f"""
        <div class="callout">

            <strong>🔎 Pattern result:</strong>

            The correlation between volume and gold movement is
            <strong>{volume_movement_corr:.2f}</strong>.

            {correlation_text}

            The points is still spread in the scatter chart,
            so volume alone cant explain every large movement.

        </div>
        """
    )


# ==================================================
# tab 5
# ==================================================

with tab5:

    show_html(
        """
        <div class="section-label">
            Final chapter
        </div>

        <div class="section-title">
            Inspect the strongest movement days
        </div>

        <div class="section-description">
            The table shows the real dates and values behind the visual results.
        </div>
        """
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


    show_html(
        """
        <div class="callout">

            <strong>📋 Why this table is here:</strong>

            The charts summarize the data, but this table shows the real
            rows behind the results.

            It help me check if the highest movements happened on event
            days, normal days, up days or down days.

        </div>
        """
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
# final note
# --------------------------------------------------

st.markdown("---")


show_html(
    """
    <div class="callout">

        <strong>Final reminder:</strong>

        This dashboard is used to explore patterns, compare groups
        and make the EDA more easy to understand.

        It does not prove that an economic event directly caused
        every gold price increase or decrease.

    </div>
    """
)
