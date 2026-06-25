import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------
# page settings
# ----------------------------
st.set_page_config(
    page_title="Gold Price EDA Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# custom style
# ----------------------------
st.markdown("""
<style>
    .main {
        background-color: #f8f6f1;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f1f1f 0%, #2a2a2a 100%);
        color: white;
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }

    .hero-box {
        background: linear-gradient(135deg, #1f1f1f 0%, #2f2f2f 100%);
        padding: 28px;
        border-radius: 20px;
        color: white;
        margin-bottom: 18px;
        border: 1px solid #d4a017;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 8px;
        color: #f1c75b;
    }

    .hero-text {
        font-size: 16px;
        color: #f2f2f2;
        line-height: 1.8;
    }

    .mini-card {
        background: white;
        border-radius: 18px;
        padding: 18px 20px;
        border-left: 6px solid #d4a017;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        margin-bottom: 10px;
    }

    .mini-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 6px;
    }

    .mini-value {
        font-size: 34px;
        font-weight: 800;
        color: #1f1f1f;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #1f1f1f;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .insight-box {
        background: #fff8e7;
        border: 1px solid #f1d27a;
        border-radius: 16px;
        padding: 14px 16px;
        margin-top: 10px;
        color: #3b2e10;
    }

    .small-note {
        color: #666;
        font-size: 13px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #ece8df;
        border-radius: 10px;
        padding: 10px 18px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #d4a017 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# load data
# ----------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("gold_final.csv")
    data["Date"] = pd.to_datetime(data["Date"])

    # just in case columns already موجودة / أو مو موجودة
    if "Abs_Change" not in data.columns and "Change_percent" in data.columns:
        data["Abs_Change"] = data["Change_percent"].abs()

    if "Year" not in data.columns:
        data["Year"] = data["Date"].dt.year

    if "Month" not in data.columns:
        data["Month"] = data["Date"].dt.month

    if "Direction" not in data.columns and "Change_percent" in data.columns:
        data["Direction"] = np.where(data["Change_percent"] > 0, "Up", "Down")

    if "Has_Event" not in data.columns and "Event_Count" in data.columns:
        data["Has_Event"] = data["Event_Count"] > 0

    if "Event_Group" not in data.columns and "Event_Count" in data.columns:
        data["Event_Group"] = "No Event"
        data.loc[data["Event_Count"].between(1, 3), "Event_Group"] = "1-3 Events"
        data.loc[data["Event_Count"] >= 4, "Event_Group"] = "4+ Events"

    return data

df = load_data()

# ----------------------------
# sidebar filters
# ----------------------------
st.sidebar.markdown("# Filters")
st.sidebar.write("The charts and numbers will change when you pick different options.")

year_options = ["All"] + sorted(df["Year"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Choose the year", year_options)

event_options = ["All days", "Event days", "No event days"]
selected_event = st.sidebar.selectbox("Choose event days", event_options)

direction_options = ["All directions", "Up only", "Down only"]
selected_direction = st.sidebar.selectbox("Choose gold direction", direction_options)

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

# اذا الفلتر صار فاضي
if filtered.empty:
    st.warning("No data found with this filter. Change one of the options from the sidebar.")
    st.stop()

# ----------------------------
# useful summary numbers
# ----------------------------
avg_price = filtered["Price"].mean()
highest_price = filtered["Price"].max()
avg_move = filtered["Abs_Change"].mean()
days_shown = len(filtered)

event_share = filtered["Has_Event"].value_counts(normalize=True) * 100
event_days_pct = event_share.get(True, 0)
no_event_days_pct = event_share.get(False, 0)

top_group = filtered.groupby("Event_Group")["Abs_Change"].mean().sort_values(ascending=False).index[0]

# ----------------------------
# hero section
# ----------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">Gold Price EDA Dashboard ✨</div>
    <div class="hero-text">
        This dashboard shows gold prices and makes it easier to compare gold movement in event days and normal days.
        I also added filters so the charts change when I choose a year or type of days.
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# quick numbers
# ----------------------------
st.markdown('<div class="section-title">Quick Numbers</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="mini-card">
        <div class="mini-title">Average Price</div>
        <div class="mini-value">{avg_price:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="mini-card">
        <div class="mini-title">Highest Price</div>
        <div class="mini-value">{highest_price:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="mini-card">
        <div class="mini-title">Average Movement</div>
        <div class="mini-value">{avg_move:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="mini-card">
        <div class="mini-title">Days Shown</div>
        <div class="mini-value">{days_shown:,}</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# tabs
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Events", "Patterns", "Data Table"])

# ==================================================
# TAB 1 - OVERVIEW
# ==================================================
with tab1:
    left, right = st.columns([2.2, 1])

    with left:
        st.markdown("### Gold Price Over Time")
        fig_line = px.line(
            filtered.sort_values("Date"),
            x="Date",
            y="Price",
            template="plotly_white"
        )
        fig_line.update_traces(
            line=dict(color="#d4a017", width=2),
            fill="tozeroy",
            fillcolor="rgba(212,160,23,0.15)"
        )
        fig_line.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Date",
            yaxis_title="Gold Price"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with right:
        st.markdown("### Event Days Share")
        donut_data = pd.DataFrame({
            "Type": ["Event Days", "No Event Days"],
            "Percent": [event_days_pct, no_event_days_pct]
        })
        fig_donut = px.pie(
            donut_data,
            names="Type",
            values="Percent",
            hole=0.55,
            color="Type",
            color_discrete_map={
                "Event Days": "#d4a017",
                "No Event Days": "#c2c8d1"
            }
        )
        fig_donut.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False
        )
        fig_donut.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_donut, use_container_width=True)

    b1, b2 = st.columns(2)

    with b1:
        st.markdown("### Distribution of Gold Prices")
        fig_hist = px.histogram(
            filtered,
            x="Price",
            color="Direction",
            barmode="overlay",
            opacity=0.65,
            template="plotly_white",
            color_discrete_map={
                "Up": "#5a9e6f",
                "Down": "#c76b6b"
            }
        )
        fig_hist.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Gold Price",
            yaxis_title="Count"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with b2:
        st.markdown("### Movement by Event Group")
        group_move = filtered.groupby("Event_Group", as_index=False)["Abs_Change"].mean()
        order_map = ["1-3 Events", "4+ Events", "No Event"]
        group_move["sorter"] = group_move["Event_Group"].apply(lambda x: order_map.index(x) if x in order_map else 99)
        group_move = group_move.sort_values("sorter")

        fig_bar_group = px.bar(
            group_move,
            x="Event_Group",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Event_Group",
            color_discrete_map={
                "1-3 Events": "#d4a017",
                "4+ Events": "#9a7a14",
                "No Event": "#b8bec8"
            }
        )
        fig_bar_group.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_bar_group.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            xaxis_title="Event Group",
            yaxis_title="Average Movement %"
        )
        st.plotly_chart(fig_bar_group, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
        In the selected data, <b>{top_group}</b> has the highest average movement.
        This does not prove a reason, but it gives a simple pattern to notice.
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# TAB 2 - EVENTS
# ==================================================
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Gold Movement by Year")
        year_move = filtered.groupby("Year", as_index=False)["Abs_Change"].mean()
        fig_year = px.bar(
            year_move,
            x="Year",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Abs_Change",
            color_continuous_scale=["#d6dbe3", "#f1c75b", "#d4a017"]
        )
        fig_year.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_year.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
            xaxis_title="Year",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_year, use_container_width=True)

    with c2:
        st.markdown("### Gold Movement by Month")
        month_move = filtered.groupby("Month", as_index=False)["Abs_Change"].mean()
        fig_month = px.bar(
            month_move,
            x="Month",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Abs_Change",
            color_continuous_scale=["#d6dbe3", "#f1c75b", "#d4a017"]
        )
        fig_month.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_month.update_layout(
            height=360,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
            xaxis_title="Month",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("### Event Type Comparison")

    compare1, compare2 = st.columns(2)

    with compare1:
        infl_compare = filtered.groupby("Inflation_Event", as_index=False)["Abs_Change"].mean()
        infl_compare["Label"] = infl_compare["Inflation_Event"].map({True: "Inflation Days", False: "Other Days"})

        fig_infl = px.bar(
            infl_compare,
            x="Label",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Label",
            color_discrete_map={
                "Inflation Days": "#d4a017",
                "Other Days": "#b8bec8"
            }
        )
        fig_infl.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_infl.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_infl, use_container_width=True)

    with compare2:
        fed_compare = filtered.groupby("Fed_Event", as_index=False)["Abs_Change"].mean()
        fed_compare["Label"] = fed_compare["Fed_Event"].map({True: "Fed Days", False: "Other Days"})

        fig_fed = px.bar(
            fed_compare,
            x="Label",
            y="Abs_Change",
            text="Abs_Change",
            template="plotly_white",
            color="Label",
            color_discrete_map={
                "Fed Days": "#9a7a14",
                "Other Days": "#b8bec8"
            }
        )
        fig_fed.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_fed.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="",
            yaxis_title="Average Movement"
        )
        st.plotly_chart(fig_fed, use_container_width=True)

# ==================================================
# TAB 3 - PATTERNS
# ==================================================
with tab3:
    st.markdown("### Volume and Gold Movement")

    fig_scatter = px.scatter(
        filtered,
        x="Vol_K",
        y="Abs_Change",
        color="Event_Group",
        template="plotly_white",
        opacity=0.7,
        color_discrete_map={
            "1-3 Events": "#d4a017",
            "4+ Events": "#9a7a14",
            "No Event": "#c2c8d1"
        },
        hover_data=["Date", "Price", "Change_percent", "Event_Count", "Direction"]
    )
    fig_scatter.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Trading Volume",
        yaxis_title="Gold Movement %"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    heat_left, heat_right = st.columns([1.3, 1])

    with heat_left:
        st.markdown("### Direction Share")
        direction_share = filtered["Direction"].value_counts().reset_index()
        direction_share.columns = ["Direction", "Count"]

        fig_direction = px.pie(
            direction_share,
            names="Direction",
            values="Count",
            hole=0.45,
            color="Direction",
            color_discrete_map={
                "Up": "#5a9e6f",
                "Down": "#c76b6b"
            }
        )
        fig_direction.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_direction, use_container_width=True)

    with heat_right:
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
                [0.0, "#f3f4f6"],
                [0.5, "#f1c75b"],
                [1.0, "#d4a017"]
            ]
        )
        fig_heat.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Month",
            yaxis_title="Year"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

# ==================================================
# TAB 4 - DATA TABLE
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
        available_cols = [c for c in show_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols], use_container_width=True)

st.markdown("""
<div class="small-note">
This dashboard shows patterns and comparisons in the dataset. It does not prove that economic events directly caused every gold price movement.
</div>
""", unsafe_allow_html=True)
