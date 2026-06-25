import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# page config
# -----------------------------
st.set_page_config(
    page_title="Gold Price EDA Dashboard",
    page_icon="✨",
    layout="wide"
)

# -----------------------------
# custom css
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: #f7f4ee;
    }

    /* main top spacing شوي */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111111 0%, #1a1a1a 45%, #252525 100%);
        border-right: 1px solid rgba(212, 160, 23, 0.15);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .sidebar-box {
        background: linear-gradient(180deg, rgba(212,160,23,0.13), rgba(255,255,255,0.03));
        border: 1px solid rgba(212,160,23,0.35);
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .sidebar-title {
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
        color: #f1c75b;
    }

    .sidebar-sub {
        font-size: 14px;
        line-height: 1.8;
        color: #f2f2f2;
    }

    .filter-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 14px;
        margin-top: 14px;
    }

    .filter-mini {
        font-size: 12px;
        color: #d4d4d4;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    .hero {
        background: linear-gradient(135deg, #151515 0%, #242424 45%, #2b2b2b 100%);
        border: 1px solid rgba(212, 160, 23, 0.28);
        border-radius: 24px;
        padding: 28px 30px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 10px 22px rgba(0,0,0,0.08);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 900;
        color: #f1c75b;
        margin-bottom: 8px;
    }

    .hero-text {
        font-size: 16px;
        line-height: 1.8;
        color: #f3f3f3;
        max-width: 900px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #1f1f1f;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .metric-card {
        background: #fffdfa;
        border: 1px solid #eadfbf;
        border-radius: 20px;
        padding: 18px 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }

    .metric-title {
        font-size: 14px;
        color: #7a6b4c;
        margin-bottom: 5px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 900;
        color: #7f5a00;
    }

    .metric-note {
        font-size: 12px;
        color: #8e8e8e;
        margin-top: 3px;
    }

    .insight {
        background: linear-gradient(135deg, #fff7df 0%, #fff3cb 100%);
        border: 1px solid #f0d37a;
        border-radius: 16px;
        padding: 15px 16px;
        color: #4b3a10;
        margin-top: 10px;
        line-height: 1.7;
    }

    .soft-box {
        background: white;
        border-radius: 18px;
        padding: 16px;
        border: 1px solid #ebe4d6;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }

    .small-note {
        color: #6d6d6d;
        font-size: 13px;
        line-height: 1.7;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #ece6d7;
        border-radius: 12px;
        padding: 10px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: #d4a017 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("gold_final.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    if "Abs_Change" not in df.columns and "Change_percent" in df.columns:
        df["Abs_Change"] = df["Change_percent"].abs()

    if "Year" not in df.columns:
        df["Year"] = df["Date"].dt.year

    if "Month" not in df.columns:
        df["Month"] = df["Date"].dt.month

    if "Direction" not in df.columns and "Change_percent" in df.columns:
        df["Direction"] = np.where(df["Change_percent"] > 0, "Up", "Down")

    if "Has_Event" not in df.columns and "Event_Count" in df.columns:
        df["Has_Event"] = df["Event_Count"] > 0

    if "Event_Group" not in df.columns and "Event_Count" in df.columns:
        df["Event_Group"] = "No Event"
        df.loc[df["Event_Count"].between(1, 3), "Event_Group"] = "1-3 Events"
        df.loc[df["Event_Count"] >= 4, "Event_Group"] = "4+ Events"

    if "Inflation_Event" not in df.columns:
        df["Inflation_Event"] = False

    if "Fed_Event" not in df.columns:
        df["Fed_Event"] = False

    return df

df = load_data()

# -----------------------------
# sidebar
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-box">
        <div class="sidebar-title">Filters</div>
        <div class="sidebar-sub">
            Use these options to change the dashboard and compare the data in different ways.
            I made the filters here so the page becomes easier and faster to read.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="filter-mini">Year filter</div>', unsafe_allow_html=True)
    year_options = ["All"] + sorted(df["Year"].dropna().unique().tolist())
    selected_year = st.selectbox("Choose the year", year_options, label_visibility="visible")

    st.markdown('<div class="filter-mini">Event day filter</div>', unsafe_allow_html=True)
    event_options = ["All days", "Event days", "No event days"]
    selected_event = st.selectbox("Choose event days", event_options, label_visibility="visible")

    st.markdown('<div class="filter-mini">Direction filter</div>', unsafe_allow_html=True)
    direction_options = ["All directions", "Up only", "Down only"]
    selected_direction = st.selectbox("Choose gold direction", direction_options, label_visibility="visible")

    st.markdown("""
    <div class="filter-card">
        <b style="color:#f1c75b;">Quick hint</b><br>
        If you want to compare the normal days with the event days, keep the year as <b>All</b> first.
        Then try changing one filter only so the difference becomes easier to notice.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# apply filters
# -----------------------------
filtered = df.copy()

if selected_year != "All":
    filtered = filtered[filtered["Year"] == selected_year]

if selected_event == "Event days":
    filtered = filtered[filtered["Has_Event"] == True]
elif selected_event == "No event days":
    filtered = filtered[filtered["Has_Event"] == False]

if selected_direction == "Up only":
    filtered = filtered[filtered["Direction"] == "Up"]
elif selected_direction == "Down only":
    filtered = filtered[filtered["Direction"] == "Down"]

if filtered.empty:
    st.warning("No data found with this filter, so just change one option from the sidebar.")
    st.stop()

# -----------------------------
# summary numbers
# -----------------------------
avg_price = filtered["Price"].mean()
highest_price = filtered["Price"].max()
avg_move = filtered["Abs_Change"].mean()
days_shown = len(filtered)

event_share = filtered["Has_Event"].value_counts(normalize=True) * 100
event_days_pct = event_share.get(True, 0)
no_event_days_pct = event_share.get(False, 0)

avg_event_count = filtered["Event_Count"].mean()

group_avg = filtered.groupby("Event_Group")["Abs_Change"].mean()
top_group = group_avg.sort_values(ascending=False).index[0]

year_peak = filtered.groupby("Year")["Abs_Change"].mean().sort_values(ascending=False)
best_year = year_peak.index[0] if not year_peak.empty else "N/A"

month_peak = filtered.groupby("Month")["Abs_Change"].mean().sort_values(ascending=False)
best_month = month_peak.index[0] if not month_peak.empty else "N/A"

# -----------------------------
# hero
# -----------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-title">Gold Price EDA Dashboard ✨</div>
    <div class="hero-text">
        This app shows gold prices and helps compare gold movement with economic events.
        I added filters, charts, and some simple summary numbers so the patterns become easier to see,
        especially when I want to compare event days, normal days, and the gold direction.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# quick numbers
# -----------------------------
st.markdown('<div class="section-title">Quick Numbers</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Price</div>
        <div class="metric-value">{avg_price:,.2f}</div>
        <div class="metric-note">mean gold price in the selected data</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Highest Price</div>
        <div class="metric-value">{highest_price:,.2f}</div>
        <div class="metric-note">maximum price after the filters</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Movement</div>
        <div class="metric-value">{avg_move:.2f}%</div>
        <div class="metric-note">average absolute daily movement</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Days Shown</div>
        <div class="metric-value">{days_shown:,}</div>
        <div class="metric-note">rows left after the current filters</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Events View",
    "Patterns & Timing",
    "Detailed Data"
])

# ==================================================
# tab 1
# ==================================================
with tab1:
    c1, c2 = st.columns([2.2, 1])

    with c1:
        st.markdown("### Gold Price Over Time")
        fig_line = px.line(
            filtered.sort_values("Date"),
            x="Date",
            y="Price",
            template="plotly_white"
        )
        fig_line.update_traces(
            line=dict(color="#d4a017", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(212,160,23,0.10)"
        )
        fig_line.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Date",
            yaxis_title="Gold Price"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.markdown("### Event Days Share")
        donut_data = pd.DataFrame({
            "Type": ["Event Days", "No Event Days"],
            "Percent": [event_days_pct, no_event_days_pct]
        })

        fig_donut = px.pie(
            donut_data,
            names="Type",
            values="Percent",
            hole=0.58,
            color="Type",
            color_discrete_map={
                "Event Days": "#d4a017",
                "No Event Days": "#c9ced6"
            }
        )
        fig_donut.update_traces(textinfo="percent+label")
        fig_donut.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    a1, a2 = st.columns(2)

    with a1:
        st.markdown("### Distribution of Gold Prices")
        fig_hist = px.histogram(
            filtered,
            x="Price",
            color="Direction",
            opacity=0.6,
            barmode="overlay",
            template="plotly_white",
            color_discrete_map={
                "Up": "#5f9f73",
                "Down": "#c46f6f"
            }
        )
        fig_hist.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Gold Price",
            yaxis_title="Count"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with a2:
        st.markdown("### Movement by Event Group")

        group_move = filtered.groupby("Event_Group", as_index=False)["Abs_Change"].mean()
        order_map = ["1-3 Events", "4+ Events", "No Event"]
        group_move["order"] = group_move["Event_Group"].apply(lambda x: order_map.index(x) if x in order_map else 99)
        group_move = group_move.sort_values("order")

        fig_group = px.bar(
            group_move,
            x="Event_Group",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Event_Group",
            color_discrete_map={
                "1-3 Events": "#d4a017",
                "4+ Events": "#9f7c14",
                "No Event": "#b8bec8"
            }
        )
        fig_group.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_group.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            xaxis_title="Event Group",
            yaxis_title="Average Movement %"
        )
        st.plotly_chart(fig_group, use_container_width=True)

    st.markdown(f"""
    <div class="insight">
        <b>Quick read:</b> in this filtered view, <b>{top_group}</b> has the biggest average gold movement.
        Also the average event count here is <b>{avg_event_count:.2f}</b>.
        This is not proof of causation, but it gives a simple pattern that can be noticed fast.
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# tab 2
# ==================================================
with tab2:
    e1, e2 = st.columns(2)

    with e1:
        st.markdown("### Event vs No Event")
        compare_event = filtered.groupby("Has_Event", as_index=False)["Abs_Change"].mean()
        compare_event["Type"] = compare_event["Has_Event"].map({True: "Event Days", False: "No Event Days"})

        fig_compare = px.bar(
            compare_event,
            x="Type",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Type",
            color_discrete_map={
                "Event Days": "#d4a017",
                "No Event Days": "#b8bec8"
            }
        )
        fig_compare.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_compare.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            xaxis_title="",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_compare, use_container_width=True)

    with e2:
        st.markdown("### Inflation Days vs Other Days")
        inflation_compare = filtered.groupby("Inflation_Event", as_index=False)["Abs_Change"].mean()
        inflation_compare["Type"] = inflation_compare["Inflation_Event"].map({True: "Inflation Days", False: "Other Days"})

        fig_infl = px.bar(
            inflation_compare,
            x="Type",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Type",
            color_discrete_map={
                "Inflation Days": "#f1c75b",
                "Other Days": "#d4d8df"
            }
        )
        fig_infl.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_infl.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            xaxis_title="",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_infl, use_container_width=True)

    e3, e4 = st.columns(2)

    with e3:
        st.markdown("### Fed Days vs Other Days")
        fed_compare = filtered.groupby("Fed_Event", as_index=False)["Abs_Change"].mean()
        fed_compare["Type"] = fed_compare["Fed_Event"].map({True: "Fed Days", False: "Other Days"})

        fig_fed = px.bar(
            fed_compare,
            x="Type",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Type",
            color_discrete_map={
                "Fed Days": "#8e6d11",
                "Other Days": "#d4d8df"
            }
        )
        fig_fed.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_fed.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            xaxis_title="",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_fed, use_container_width=True)

    with e4:
        st.markdown("### Up vs Down Days")
        direction_data = filtered["Direction"].value_counts().reset_index()
        direction_data.columns = ["Direction", "Count"]

        fig_direction = px.pie(
            direction_data,
            names="Direction",
            values="Count",
            hole=0.50,
            color="Direction",
            color_discrete_map={
                "Up": "#5f9f73",
                "Down": "#c46f6f"
            }
        )
        fig_direction.update_traces(textinfo="percent+label")
        fig_direction.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_direction, use_container_width=True)

# ==================================================
# tab 3
# ==================================================
with tab3:
    p1, p2 = st.columns(2)

    with p1:
        st.markdown("### Gold Movement by Year")
        year_move = filtered.groupby("Year", as_index=False)["Abs_Change"].mean()

        fig_year = px.bar(
            year_move,
            x="Year",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Abs_Change",
            color_continuous_scale=["#d4d8df", "#f1c75b", "#d4a017"]
        )
        fig_year.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_year.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
            xaxis_title="Year",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_year, use_container_width=True)

    with p2:
        st.markdown("### Gold Movement by Month")
        month_move = filtered.groupby("Month", as_index=False)["Abs_Change"].mean()

        fig_month = px.bar(
            month_move,
            x="Month",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Abs_Change",
            color_continuous_scale=["#d4d8df", "#f1c75b", "#d4a017"]
        )
        fig_month.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_month.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
            xaxis_title="Month",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("### Monthly Heatmap by Year")

    heat = filtered.pivot_table(
        index="Year",
        columns="Month",
        values="Abs_Change",
        aggfunc="mean"
    )

    fig_heat = px.imshow(
        heat,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale=[
            [0.0, "#f1f1f1"],
            [0.5, "#f1c75b"],
            [1.0, "#d4a017"]
        ]
    )
    fig_heat.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Month",
        yaxis_title="Year"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("### Volume and Gold Movement")
    fig_scatter = px.scatter(
        filtered,
        x="Vol_K",
        y="Abs_Change",
        color="Event_Group",
        hover_data=["Date", "Price", "Change_percent", "Direction", "Event_Count"],
        template="plotly_white",
        opacity=0.75,
        color_discrete_map={
            "1-3 Events": "#d4a017",
            "4+ Events": "#a68118",
            "No Event": "#c9ced6"
        }
    )
    fig_scatter.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Trading Volume",
        yaxis_title="Gold Movement %"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown(f"""
    <div class="insight">
        <b>Another quick read:</b> the year with the strongest average movement here is <b>{best_year}</b>,
        and the month with the strongest average movement is <b>{best_month}</b>.
        So if someone asks where the movement looked stronger in the selected view, these are the first places to notice.
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# tab 4
# ==================================================
with tab4:
    st.markdown("### Biggest Gold Movement Days")
    biggest = filtered.nlargest(10, "Abs_Change")[
        ["Date", "Price", "Change_percent", "Abs_Change", "Event_Count", "Event_Group", "Direction"]
    ].copy()

    biggest["Date"] = biggest["Date"].astype(str)
    st.dataframe(biggest, use_container_width=True)

    with st.expander("Show filtered data"):
        show_cols = [
            "Date", "Price", "Open", "High", "Low", "Vol_K",
            "Change_percent", "Event_Count", "Has_Event",
            "Abs_Change", "Event_Group", "Direction",
            "Year", "Month", "Inflation_Event", "Fed_Event"
        ]
        show_cols = [c for c in show_cols if c in filtered.columns]
        st.dataframe(filtered[show_cols], use_container_width=True)

st.markdown("""
<div class="small-note">
This dashboard shows patterns inside the data. It helps with comparing and exploring,
but it does not prove that economic events directly caused every gold movement.
</div>
""", unsafe_allow_html=True)
