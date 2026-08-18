"""
Network Routing Principles — Scenario Calculator
Streamlit front-end  (companion to network_calculator.py)

Run with:
    streamlit run app.py
"""

import pandas as pd
import streamlit as st

from tne20002_scenario_calculator import Scenario, AllScenarios

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Network Routing — Scenario Calculator",
    page_icon="🌐",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS  (matches eng10006numbers.streamlit.app clean style)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Overall background ── */
.stApp { background-color: #f5f7fb; }

/* ── Hide Deploy button ── */
[data-testid="stAppDeployButton"] {
    display: none !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { background-color: #1a2744; }
[data-testid="stSidebar"] * { color: #e8ecf4 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label { color: #b0bcdb !important; font-size:0.85rem; }

/* ── Sidebar text input — always dark to match sidebar ── */
[data-testid="stSidebar"] .stTextInput input {
    color: #e8ecf4 !important;
    background-color: #222222 !important;
    border-color: #3a4d7a !important;
}

/* ── Sidebar selectbox trigger (selected value + expand arrow) ── */
.stSelectbox input[role="combobox"] {
    background-color: #222222 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Container around input and button */
.stSelectbox div[role="group"] {
    background-color: #222222 !important;
    border: 1px solid #3a4d7a !important;
}

/* Chevron button */
.stSelectbox button {
    background-color: #222222 !important;
}

/* Chevron */
.stSelectbox button svg {
    fill: #00c8ff !important;
    color: #00c8ff !important;
}

/* Dropdown menu */
div[role="listbox"] {
    background-color: #253460 !important;
}

/* All dropdown items - white on dark blue background */
div[role="option"] {
    background-color: #253460 !important;
    color: #ffffff !important;
}

/* Hovered item - white on grey background */
div[role="option"]:hover {
    background-color: #404040 !important;
    color: #ffffff !important;
}

/* Selected item inside expanded list - white on blue background */
div[aria-selected="true"] {
    background-color: #1a6fc4 !important;
    color: white !important;
}

/* ── Result cards ── */
.result-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 12px;
    border-left: 5px solid #1a6fc4;
    box-shadow: 0 2px 6px rgba(0,0,0,0.07);
}
.result-card h4 { margin: 0 0 4px 0; font-size: 0.80rem;
                  color: #6b7a99; text-transform: uppercase; letter-spacing: .06em; }
.result-card p  { margin: 0; font-size: 1.25rem; font-weight: 700;
                  font-family: 'Courier New', monospace; color: #1a2744; }

/* ── VLAN cards ── */
.vlan-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    border-top: 4px solid;
    box-shadow: 0 2px 6px rgba(0,0,0,0.07);
}
.vlan-card h4 { margin: 0 0 4px 0; font-size: 0.78rem;
                color: #6b7a99; text-transform: uppercase; letter-spacing: .06em; }
.vlan-card p  { margin: 0; font-size: 1.55rem; font-weight: 800;
                font-family: 'Courier New', monospace; }

/* ── Detail table ── */
.detail-table { width:100%; border-collapse:collapse; font-size:0.87rem; }
.detail-table th { background:#1a2744; color:#e8ecf4;
                   padding:8px 12px; text-align:left; }
.detail-table td { padding:7px 12px; border-bottom:1px solid #e4e8f0; }
.detail-table tr:last-child td { border-bottom:none; }
.detail-table tr:hover td { background:#f0f4ff; }

/* ── Section header ── */
.section-header {
    font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; color: #6b7a99; margin: 24px 0 8px 0;
}

/* ── All-weeks table ── */
.styled-df thead th { background:#1a2744 !important; color:#fff !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — inputs
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image('logo.webp', use_container_width=True)
    st.markdown("## 🌐 Scenario Calculator")
    st.markdown("---")
    st.markdown("#### Student ID")
    sid_input = st.text_input(
        "Enter your student ID",
        value="123456789",
        max_chars=12,
        help="9 digits  |  7 digits  |  6 digits + X",
        label_visibility="collapsed",
    )
    st.caption("9 digits · 7 digits · 6 digits + X")

    st.markdown("#### Scenario")
    scenario_options = {f"Scenario {s} — {Scenario.SCENARIO_LABELS[s].split(':')[1].strip()}": s for s in Scenario.SCENARIO_ID}
    scenario_label = st.selectbox("Select scenario", options=list(scenario_options.keys()), label_visibility="collapsed")
    selected_scenario = scenario_options[scenario_label]

    st.markdown("---")
    show_all = st.toggle("Show all 6 scenarios", value=False)

    st.markdown("---")
    st.markdown(
        "<small style='color:#8090b0'>Values derived deterministically from "
        "your Student ID — identical input always gives identical output.</small>",
        unsafe_allow_html=True,
    )

if "cached_sid" not in st.session_state or st.session_state.cached_sid != sid_input:
    try:
        st.session_state.cached_sid = sid_input
        print('recreating cache')
        st.session_state.all_scenarios = AllScenarios(sid_input)
    except Exception as e:
        st.error(f"❌ {e}")
        st.stop()

# Validate ID and build scenario
all_scenarios = st.session_state.all_scenarios
scenario = all_scenarios.scenarios[selected_scenario]

# Main area — header
col_title1, col_title2 = st.columns([2, 1])
with col_title1:
    st.markdown(
        f"<h2 style='margin-bottom:0;color:#1a2744'>🌐 TNE20002/70003 - Network Routing Principles</h2>"
        f'<h3 style="color:#6b7a99;margin-top:2px">{scenario.label}</h3>',
        unsafe_allow_html=True,
    )
with col_title2:
    st.markdown(
        f"<div class='result-card'>"
        f"<h4>Student ID</h4><p>{scenario.id}</p></div>",
        unsafe_allow_html=True,
    )
st.markdown("---")

# Main results — addressing
st.markdown(f"<p class='section-header'>📡 Network Addresses</p>",
            unsafe_allow_html=True)

col_corp, col_isp = st.columns(2)

with col_corp:
    st.markdown(
        f"<div class='result-card' style='border-left-color:#1a6fc4'>"
        f"<h4>Corporate Network</h4>"
        f"<p>{scenario.corporate_address}</p></div>",
        unsafe_allow_html=True,
    )
    with st.expander("Network detail"):
        st.markdown(f"""
| Field | Value |
|---|---|
| Network address | `{scenario.corporate_address}` |
| Subnet mask | `{scenario.corporate_address.netmask}` |
| Wildcard mask | `{scenario.corporate_address.hostmask}` |
| First host | `{scenario.corporate_address[1]}` |
| Last host | `{scenario.corporate_address[-2]}` |
| Usable hosts | `{scenario.corporate_address.num_addresses - 2}` |
""")

with col_isp:
    st.markdown(
        f"<div class='result-card' style='border-left-color:#e07b00'>"
        f"<h4>ISP Point-to-Point Link (/30)</h4>"
        f"<p>{scenario.isp_address}</p></div>",
        unsafe_allow_html=True,
    )
    with st.expander("Network detail"):
        st.markdown(f"""
| Field | Value |
|---|---|
| Network address | `{scenario.isp_address}` |
| Subnet mask | `{scenario.isp_address.netmask}` |
| Wildcard mask | `{scenario.isp_address.hostmask}` |
| Router A (ISP side) | `{scenario.isp_address[1]}` |
| Router B (customer) | `{scenario.isp_address[-2]}` |
| Usable hosts | `{scenario.isp_address.num_addresses - 2}` |
""")

# VLAN cards
st.markdown("<p class='section-header'>🏷️ VLAN Assignments</p>", unsafe_allow_html=True)

v1, v2, v3 = st.columns(3)
vlan_styles = [
    ("#1a6fc4", scenario.vlanxxx, "VLAN XXX"),
    ("#e07b00", scenario.vlanyyy, "VLAN YYY"),
    ("#1e7e34", scenario.vlanzzz, "VLAN ZZZ"),
]
for col, (colour, vid, label) in zip([v1, v2, v3], vlan_styles):
    with col:
        st.markdown(
            f"<div class='vlan-card' style='border-top-color:{colour}'>"
            f"<h4>{label}</h4>"
            f"<p style='color:{colour}'>VLAN {vid}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# All-weeks table (toggle)
# ─────────────────────────────────────────────────────────────────────────────
if show_all:
    st.markdown("---")
    st.markdown("<p class='section-header'>📋 All 6 Weeks — Full Scenario Table</p>",
                unsafe_allow_html=True)

    rows = []
    for s in all_scenarios.scenarios.values():
        rows.append({
            "Scenario": s.label,
            "Corporate Network": str(s.corporate_address),
            "ISP Link (/30)": str(s.isp_address),
            "VLAN XXX": f"VLAN {s.vlanxxx}",
            "VLAN YYY": f"VLAN {s.vlanyyy}",
            "VLAN ZZZ": f"VLAN {s.vlanzzz}",
        })
    df = pd.DataFrame(rows).set_index("Scenario")

    # Highlight current week row
    def highlight_current(row):
        return ["background-color: #1a6fc4; color: #ffffff; font-weight:bold"
                if row.name == Scenario.SCENARIO_LABELS[selected_scenario] else "" for _ in row]

    st.dataframe(
        df.style.apply(highlight_current, axis=1),
        use_container_width=True,
        height="auto",
    )

# ─────────────────────────────────────────────────────────────────────────────
# Download CSV Buttons
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")

st.markdown("<p class='section-header'>⏬ Download CSV Files</p>",
            unsafe_allow_html=True)

col_dl1, col_dl2, _ = st.columns([2, 2, 3])
with (col_dl1):
    single_csv = all_scenarios.csv_bytes(scenario.scenario)
    st.download_button(
        label=f"⬇ Download Scenario {selected_scenario} CSV",
        data=single_csv,
        file_name=f"scenario_{selected_scenario}_{sid_input}.csv",
        mime="text/csv",
    )
with col_dl2:
    if show_all:
        all_csv = all_scenarios.csv_bytes(None)
        st.download_button(
            label="⬇ Download All Scenarios CSV",
            data=all_csv,
            file_name=f"scenarios_{sid_input}_all.csv",
            mime="text/csv",
        )

# Footer
st.markdown(
    "<br><hr><p style='color:#aab4c8;font-size:0.78rem;text-align:center'>"
    "Network Routing Principles — Scenario Calculator &nbsp;|&nbsp; "
    "Swinburne University of Technology</p>",
    unsafe_allow_html=True,
)
