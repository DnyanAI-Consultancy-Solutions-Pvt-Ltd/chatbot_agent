import os
import requests
import pandas as pd  # type: ignore[import]
import streamlit as st  # type: ignore[import]
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="MHT-CET AI Counselor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000/api/counsel"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "response" not in st.session_state:
    st.session_state.response = None

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown(
    """
<style>

/* ---------- Hide Streamlit ---------- */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* ---------- Background ---------- */

.stApp{
background:#f5f7fb;
}

/* ---------- Title ---------- */

.main-title{
font-size:40px;
font-weight:800;
color:#1E3A8A;
margin-bottom:5px;
}

.subtitle{
font-size:17px;
color:#6B7280;
margin-bottom:25px;
}

/* ---------- Cards ---------- */

.card{

background:white;

padding:22px;

border-radius:18px;

box-shadow:0 8px 24px rgba(0,0,0,.08);

margin-bottom:20px;

border:1px solid #EEF2F7;

}

/* ---------- Inputs ---------- */

.stTextInput input,
.stNumberInput input,
textarea{

border-radius:12px !important;

border:1px solid #D1D5DB !important;

padding:10px !important;

}

.stSelectbox div[data-baseweb="select"]{

border-radius:12px;

}

/* ---------- Button ---------- */

.stButton>button{

width:100%;

height:52px;

border:none;

border-radius:14px;

background:#2563EB;

color:white;

font-size:17px;

font-weight:600;

transition:.25s;

}

.stButton>button:hover{

background:#1D4ED8;

transform:translateY(-2px);

}

/* ---------- Metrics ---------- */

.metric-box{

background:#EFF6FF;

padding:15px;

border-radius:15px;

text-align:center;

border:1px solid #BFDBFE;

}

.metric-title{

font-size:14px;

color:#6B7280;

}

.metric-value{

font-size:26px;

font-weight:700;

color:#1E40AF;

}

/* ---------- Recommendation ---------- */

.recommend-card{

background:#ECFDF5;

border-left:6px solid #10B981;

padding:18px;

border-radius:12px;

margin-bottom:15px;

}

.warning-card{

background:#FEF2F2;

border-left:6px solid #EF4444;

padding:18px;

border-radius:12px;

margin-bottom:15px;

}

.info-card{

background:#F0F9FF;

border-left:6px solid #0EA5E9;

padding:18px;

border-radius:12px;

margin-bottom:15px;

}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{

background:white;

border-right:1px solid #E5E7EB;

}

/* ---------- Footer ---------- */

.footer{

text-align:center;

color:#9CA3AF;

font-size:13px;

padding-top:30px;

}

</style>
""",
    unsafe_allow_html=True,
)
# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🎓 AI Counselor")

    st.markdown(
        """
        Helping students discover the
        best engineering colleges based on
        their MHT-CET/JEE performance.
        """
    )

    st.divider()

    # -----------------------------
    # Student Profile
    # -----------------------------
    st.markdown("### 👤 Student Profile")

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    exam = st.selectbox(
        "Entrance Exam",
        [
            "MHT-CET",
            "JEE Main"
        ]
    )

    category = st.selectbox(
        "Category",
        [
            "OPEN",
            "OBC",
            "EWS",
            "SC",
            "ST",
            "NT-A",
            "NT-B",
            "NT-C",
            "NT-D",
            "SBC",
            "SEBC"
        ]
    )

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female",
            "Other"
        ]
    )

    st.divider()

    # -----------------------------
    # Quick Statistics
    # -----------------------------
    st.markdown("### 📊 Quick Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Colleges",
            "450+"
        )

    with col2:
        st.metric(
            "Branches",
            "40+"
        )

    st.metric(
        "Cutoff Records",
        "2 Lakh+"
    )

    st.divider()

    # -----------------------------
    # API Status
    # -----------------------------
    st.markdown("### 🌐 Backend Status")

    try:
        requests.get(
            BACKEND_URL,
            timeout=2
        )

        st.success("Backend Connected")

    except Exception:
        st.error("Backend Offline")

    st.divider()

    # -----------------------------
    # Reset Conversation
    # -----------------------------
    if st.button("🗑 Reset Session"):

        st.session_state.history = []
        st.session_state.response = None

        st.rerun()

    st.divider()

    st.caption("Version 1.0")
    st.caption("Built with Streamlit ❤️")
# =====================================================
# MAIN HEADER
# =====================================================

st.markdown(
    """
    <div class="main-title">
        🎓 MHT-CET & JEE AI Counselor
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Get AI-powered engineering college recommendations based on your
        MHT-CET or JEE Main score, category, and preferences.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# =====================================================
# INPUT CARD
# =====================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📝 Enter Your Counseling Details")

col1, col2 = st.columns(2)

with col1:

    score_type = st.radio(
        "Score Type",
        ["Rank", "Percentile"],
        horizontal=True,
    )

    if score_type == "Rank":
        score_value = st.number_input(
            "MHT-CET / JEE Rank",
            min_value=1,
            max_value=500000,
            step=1,
            placeholder=25000,
        )
    else:
        score_value = st.number_input(
            "Percentile",
            min_value=0.0,
            max_value=100.0,
            step=0.01,
            format="%.2f",
            placeholder=95.50,
        )

    preferred_branch = st.selectbox(
        "Preferred Branch",
        [
            "Any",
            "Computer Engineering",
            "Information Technology",
            "Artificial Intelligence",
            "Artificial Intelligence & Data Science",
            "Data Science",
            "Electronics & Telecommunication",
            "Electronics Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Civil Engineering",
            "Chemical Engineering",
            "Instrumentation Engineering",
            "Production Engineering",
            "Robotics & Automation",
        ],
    )

with col2:

    preferred_region = st.selectbox(
        "Preferred Region",
        [
            "Any",
            "Pune",
            "Mumbai",
            "Navi Mumbai",
            "Thane",
            "Nagpur",
            "Nashik",
            "Aurangabad",
            "Kolhapur",
            "Amravati",
            "Solapur",
        ],
    )

    hostel_required = st.radio(
        "Hostel Required",
        ["No", "Yes"],
        horizontal=True,
    )

    college_type = st.multiselect(
        "College Preference",
        [
            "Government",
            "Government Autonomous",
            "Private",
            "Autonomous",
            "University",
        ],
        default=[],
    )

remarks = st.text_area(
    "Additional Preferences (Optional)",
    placeholder="Example: Low fees, autonomous colleges, strong placements, Pune city...",
    height=100,
)

st.markdown("<br>", unsafe_allow_html=True)

generate_btn = st.button(
    "🚀 Get AI Recommendation",
    use_container_width=True,
)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# API CALL
# =====================================================

if generate_btn:

    # -----------------------------
    # Basic Validation
    # -----------------------------
    if score_value <= 0:
        st.warning("Please enter a valid Rank or Percentile.")
        st.stop()

    payload = {
        "student_name": student_name,
        "exam": exam,
        "category": category,
        "gender": gender,
        "score_type": score_type,
        "score": score_value,
        "preferred_branch": preferred_branch,
        "preferred_region": preferred_region,
        "hostel_required": hostel_required == "Yes",
        "college_preference": college_type,
        "remarks": remarks,
    }

    with st.spinner("🔍 Analyzing your profile and finding the best colleges..."):

        try:

            response = requests.post(
                BACKEND_URL,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            result = response.json()

            st.session_state.response = result

            st.session_state.history.append(
                {
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "payload": payload,
                    "result": result,
                }
            )

            st.success("✅ Recommendations generated successfully!")

        except requests.exceptions.Timeout:
            st.error(
                "The request timed out. Please check whether the backend is busy and try again."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Unable to connect to the backend. Verify that the FastAPI server is running and the BACKEND_URL is correct."
            )

        except requests.exceptions.HTTPError as e:

            message = f"HTTP Error: {e}"

            try:
                error_json = response.json()

                if isinstance(error_json, dict):
                    message = error_json.get("detail", message)

            except Exception:
                pass

            st.error(message)

        except Exception as e:
            st.exception(e)
    
        # =====================================================
# RESULTS DASHBOARD
# =====================================================

if st.session_state.response:

    result = st.session_state.response

    st.markdown("## 📋 AI Counseling Results")

    # -----------------------------
    # Summary Metrics
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    rank_display = result.get(
        "rank",
        score_value if score_type == "Rank" else "-"
    )

    percentile_display = result.get(
        "percentile",
        score_value if score_type == "Percentile" else "-"
    )

    recommendation_count = len(
        result.get("recommendations", [])
    )

    with col1:
        st.metric("Rank", rank_display)

    with col2:
        st.metric("Percentile", percentile_display)

    with col3:
        st.metric("Recommendations", recommendation_count)

    st.divider()

    # -----------------------------
    # AI Summary
    # -----------------------------
    summary = (
        result.get("summary")
        or result.get("analysis")
        or result.get("ai_summary")
        or result.get("message")
    )

    if summary:
        st.markdown(
            f"""
<div class="info-card">
<h4>🤖 AI Counselor Summary</h4>
<p>{summary}</p>
</div>
""",
            unsafe_allow_html=True,
        )

    # -----------------------------
    # College Recommendations
    # -----------------------------
    recommendations = result.get("recommendations", [])

    if recommendations:

        st.subheader("🏫 Recommended Colleges")

        for idx, college in enumerate(recommendations, start=1):

            name = college.get("college_name", "Unknown College")
            branch = college.get("branch", "N/A")
            category_name = college.get("category", category)

            cutoff = (
                college.get("cutoff_rank")
                or college.get("cutoff")
                or "-"
            )

            fees = college.get("fees", "N/A")
            placement = college.get("placement", "N/A")
            city = college.get("city", preferred_region)

            match = int(college.get("match_percentage", 0))

            if match >= 85:
                card_class = "recommend-card"
                badge = "🟢 Safe"
            elif match >= 60:
                card_class = "info-card"
                badge = "🟡 Target"
            else:
                card_class = "warning-card"
                badge = "🔴 Dream"

            st.markdown(
                f"""
<div class="{card_class}">
<h4>{idx}. {name}</h4>

<b>Branch:</b> {branch}<br>
<b>City:</b> {city}<br>
<b>Category:</b> {category_name}<br>
<b>Expected Cutoff:</b> {cutoff}<br>
<b>Annual Fees:</b> {fees}<br>
<b>Placement:</b> {placement}<br><br>

<b>{badge}</b>

<div style="margin-top:10px;">
Match Score: <b>{match}%</b>
</div>
</div>
""",
                unsafe_allow_html=True,
            )

    else:

        st.info(
            "No college recommendations were returned by the backend."
        )
    # =====================================================
# ANALYTICS & VISUALIZATION
# =====================================================

if st.session_state.response:

    recommendations = st.session_state.response.get("recommendations", [])

    if recommendations:

        st.divider()
        st.subheader("📊 Recommendation Analytics")

        # -----------------------------------------
        # Convert recommendations to DataFrame
        # -----------------------------------------
        rows = []

        for college in recommendations:

            rows.append(
                {
                    "College": college.get("college_name", ""),
                    "Branch": college.get("branch", ""),
                    "City": college.get("city", ""),
                    "Category": college.get("category", ""),
                    "Cutoff": college.get(
                        "cutoff_rank",
                        college.get("cutoff", "")
                    ),
                    "Fees": college.get("fees", ""),
                    "Placement": college.get("placement", ""),
                    "Match %": int(
                        college.get("match_percentage", 0)
                    ),
                }
            )

        df = pd.DataFrame(rows)

        # -----------------------------------------
        # Safe / Target / Dream counts
        # -----------------------------------------
        safe = len(df[df["Match %"] >= 85])
        target = len(df[(df["Match %"] >= 60) & (df["Match %"] < 85)])
        dream = len(df[df["Match %"] < 60])

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Match Distribution")

            chart_df = pd.DataFrame(
                {
                    "Category": [
                        "Safe",
                        "Target",
                        "Dream",
                    ],
                    "Count": [
                        safe,
                        target,
                        dream,
                    ],
                }
            )

            st.bar_chart(
                chart_df.set_index("Category")
            )

        with col2:

            st.markdown("#### Match Score Comparison")

            score_df = (
                df[["College", "Match %"]]
                .sort_values(
                    by="Match %",
                    ascending=False,
                )
                .set_index("College")
            )

            st.bar_chart(score_df)

        # -----------------------------------------
        # Region Summary
        # -----------------------------------------
        if "City" in df.columns:

            st.markdown("#### 📍 City-wise Recommendations")

            city_summary = (
                df.groupby("City")
                .size()
                .reset_index(name="Count")
                .set_index("City")
            )

            st.bar_chart(city_summary)

        st.divider()

        # -----------------------------------------
        # Recommendation Table
        # -----------------------------------------
        st.subheader("📋 Recommendation Table")

        display_df = (
            df.sort_values(
                by="Match %",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        # -----------------------------------------
        # Download CSV
        # -----------------------------------------
        csv = display_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Recommendations (CSV)",
            data=csv,
            file_name="mht_cet_recommendations.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # =====================================================
# SEARCH & FILTER RECOMMENDATIONS
# =====================================================

if st.session_state.response:

    recommendations = st.session_state.response.get("recommendations", [])

    if recommendations:

        st.divider()
        st.subheader("🔍 Search & Filter Recommendations")

        # Initialize favorites
        if "favorites" not in st.session_state:
            st.session_state.favorites = []

        col1, col2 = st.columns([2, 1])

        with col1:
            search_text = st.text_input(
                "Search by College or Branch",
                placeholder="Example: COEP, Computer Engineering...",
            )

        with col2:
            min_match = st.slider(
                "Minimum Match %",
                min_value=0,
                max_value=100,
                value=0,
                step=5,
            )

        filtered = []

        for college in recommendations:

            name = college.get("college_name", "")
            branch = college.get("branch", "")
            match = int(college.get("match_percentage", 0))

            if (
                search_text.lower() in name.lower()
                or search_text.lower() in branch.lower()
                or search_text == ""
            ) and match >= min_match:

                filtered.append(college)

        st.write(f"Showing **{len(filtered)}** recommendation(s).")

        for idx, college in enumerate(filtered):

            name = college.get("college_name", "Unknown College")
            branch = college.get("branch", "")
            match = int(college.get("match_percentage", 0))

            cols = st.columns([6, 1])

            with cols[0]:
                st.markdown(
                    f"""
**{name}**

{branch}

Match Score: **{match}%**
"""
                )

            with cols[1]:

                if st.button(
                    "⭐",
                    key=f"fav_{idx}",
                    help="Add to Favorites",
                ):

                    if college not in st.session_state.favorites:
                        st.session_state.favorites.append(college)

                        st.success(f"Added {name}")

# =====================================================
# FAVORITES
# =====================================================

if "favorites" in st.session_state:

    if st.session_state.favorites:

        st.divider()

        st.subheader("⭐ Favorite Colleges")

        for fav in st.session_state.favorites:

            st.markdown(
                f"""
<div class="recommend-card">

<b>{fav.get('college_name')}</b>

<br>

Branch:
{fav.get('branch','')}

<br>

Match:
{fav.get('match_percentage',0)}%

</div>
""",
                unsafe_allow_html=True,
            )

# =====================================================
# SEARCH HISTORY
# =====================================================

if st.session_state.history:

    st.divider()

    st.subheader("🕒 Counseling History")

    history = list(reversed(st.session_state.history))

    for i, item in enumerate(history):

        with st.expander(
            f"{item['time']} | "
            f"{item['payload'].get('preferred_branch','Any')} | "
            f"{item['payload'].get('score')}"
        ):

            payload = item["payload"]

            st.write("### Search Details")

            st.write(
                {
                    "Student": payload.get("student_name"),
                    "Exam": payload.get("exam"),
                    "Category": payload.get("category"),
                    "Score Type": payload.get("score_type"),
                    "Score": payload.get("score"),
                    "Branch": payload.get("preferred_branch"),
                    "Region": payload.get("preferred_region"),
                }
            )

            recs = item["result"].get(
                "recommendations",
                []
            )

            st.write(
                f"Recommendations Returned: {len(recs)}"
            )

# =====================================================
# CLEAR HISTORY
# =====================================================

if st.session_state.history:

    if st.button(
        "🗑 Clear Counseling History",
        use_container_width=True,
    ):

        st.session_state.history = []
        st.rerun()

    # =====================================================
# PROFESSIONAL RESULT HIGHLIGHTS
# =====================================================

if st.session_state.response:

    recommendations = st.session_state.response.get("recommendations", [])

    if recommendations:

        st.divider()

        st.header("🏆 Best Match")

        # Sort recommendations by match percentage
        sorted_recommendations = sorted(
            recommendations,
            key=lambda x: int(x.get("match_percentage", 0)),
            reverse=True
        )

        best = sorted_recommendations[0]

        best_name = best.get("college_name", "Unknown College")
        best_branch = best.get("branch", "N/A")
        best_city = best.get("city", "N/A")
        best_match = int(best.get("match_percentage", 0))
        best_fees = best.get("fees", "N/A")
        best_place = best.get("placement", "N/A")

        st.success(
            f"🎯 {best_name} is currently your strongest recommendation."
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Match Score", f"{best_match}%")
            st.metric("Branch", best_branch)

        with col2:
            st.metric("City", best_city)
            st.metric("Fees", best_fees)

        st.write("Placement:", best_place)

        st.progress(best_match / 100)

        st.divider()

# =====================================================
# MATCH SCORE PROGRESS
# =====================================================

if st.session_state.response:

    recommendations = st.session_state.response.get("recommendations", [])

    if recommendations:

        st.header("📈 Match Score Overview")

        sorted_recommendations = sorted(
            recommendations,
            key=lambda x: int(x.get("match_percentage", 0)),
            reverse=True
        )

        for college in sorted_recommendations:

            name = college.get("college_name", "Unknown College")
            match = int(college.get("match_percentage", 0))

            if match >= 85:
                badge = "🟢 Safe"
            elif match >= 60:
                badge = "🟡 Target"
            else:
                badge = "🔴 Dream"

            cols = st.columns([4, 2])

            with cols[0]:
                st.write(f"**{name}**")

            with cols[1]:
                st.write(badge)

            st.progress(match / 100)

            st.caption(f"{match}% Match")

# =====================================================
# SMART COUNSELING INSIGHTS
# =====================================================

if st.session_state.response:

    recommendations = st.session_state.response.get("recommendations", [])

    if recommendations:

        st.divider()

        st.header("💡 AI Counseling Insights")

        safe = len(
            [r for r in recommendations
             if int(r.get("match_percentage", 0)) >= 85]
        )

        target = len(
            [r for r in recommendations
             if 60 <= int(r.get("match_percentage", 0)) < 85]
        )

        dream = len(
            [r for r in recommendations
             if int(r.get("match_percentage", 0)) < 60]
        )

        if safe > 0:
            st.info(
                f"✅ You have {safe} Safe college option(s). "
                "These are strong choices based on your profile."
            )

        if target > 0:
            st.warning(
                f"🎯 You have {target} Target college option(s). "
                "These are competitive but achievable."
            )

        if dream > 0:
            st.error(
                f"🚀 You have {dream} Dream college option(s). "
                "Apply if you're comfortable with higher competition."
            )

        average_match = (
            sum(
                int(r.get("match_percentage", 0))
                for r in recommendations
            ) / len(recommendations)
        )

        st.metric(
            "Average Match Score",
            f"{average_match:.1f}%"
        )

# =====================================================
# QUICK COUNSELING CHECKLIST
# =====================================================

st.divider()

st.header("📝 Counseling Checklist")

checklist = [
    "Verify your rank/percentile before CAP registration.",
    "Keep caste/category certificates ready (if applicable).",
    "Prepare domicile and income certificates.",
    "Shortlist Safe, Target, and Dream colleges.",
    "Review previous year's cutoffs.",
    "Check hostel availability if required.",
    "Keep scanned documents ready for verification.",
]

for item in checklist:
    st.checkbox(item, value=False)

    # =====================================================
# COLLEGE COMPARISON
# =====================================================

if st.session_state.response:

    recommendations = st.session_state.response.get("recommendations", [])

    if len(recommendations) >= 2:

        st.divider()
        st.header("⚖️ Compare Colleges")

        college_names = [
            c.get("college_name", "Unknown College")
            for c in recommendations
        ]

        col1, col2 = st.columns(2)

        with col1:
            college_a = st.selectbox(
                "College A",
                college_names,
                key="compare_a"
            )

        with col2:
            college_b = st.selectbox(
                "College B",
                college_names,
                index=1,
                key="compare_b"
            )

        if college_a != college_b:

            data_a = next(
                x for x in recommendations
                if x.get("college_name") == college_a
            )

            data_b = next(
                x for x in recommendations
                if x.get("college_name") == college_b
            )

            comparison = {
                "Attribute": [
                    "Branch",
                    "City",
                    "Fees",
                    "Placement",
                    "Match %",
                    "Cutoff"
                ],
                college_a: [
                    data_a.get("branch", "-"),
                    data_a.get("city", "-"),
                    data_a.get("fees", "-"),
                    data_a.get("placement", "-"),
                    data_a.get("match_percentage", "-"),
                    data_a.get(
                        "cutoff_rank",
                        data_a.get("cutoff", "-")
                    )
                ],
                college_b: [
                    data_b.get("branch", "-"),
                    data_b.get("city", "-"),
                    data_b.get("fees", "-"),
                    data_b.get("placement", "-"),
                    data_b.get("match_percentage", "-"),
                    data_b.get(
                        "cutoff_rank",
                        data_b.get("cutoff", "-")
                    )
                ]
            }

            compare_df = pd.DataFrame(comparison)

            st.dataframe(
                compare_df,
                use_container_width=True,
                hide_index=True,
            )

# =====================================================
# CAP ROUND SIMULATION
# =====================================================

if st.session_state.response:

    recommendations = st.session_state.response.get("recommendations", [])

    if recommendations:

        st.divider()
        st.header("🎯 CAP Round Simulation")

        cap_round = st.selectbox(
            "Select CAP Round",
            [
                "CAP Round I",
                "CAP Round II",
                "CAP Round III"
            ]
        )

        adjustment = {
            "CAP Round I": 0,
            "CAP Round II": 5,
            "CAP Round III": 10
        }

        bonus = adjustment[cap_round]

        simulated = []

        for college in recommendations:

            score = min(
                int(college.get("match_percentage", 0)) + bonus,
                100
            )

            simulated.append(
                {
                    "College": college.get("college_name", ""),
                    "Simulated Match %": score
                }
            )

        sim_df = (
            pd.DataFrame(simulated)
            .sort_values(
                "Simulated Match %",
                ascending=False
            )
        )

        st.dataframe(
            sim_df,
            use_container_width=True,
            hide_index=True,
        )

# =====================================================
# PRINTABLE REPORT
# =====================================================

if st.session_state.response:

    st.divider()
    st.header("🖨️ Counseling Report")

    result = st.session_state.response
    recommendations = result.get("recommendations", [])

    report_lines = []

    report_lines.append("MHT-CET AI COUNSELING REPORT")
    report_lines.append("=" * 40)
    report_lines.append("")

    report_lines.append(f"Student : {student_name}")
    report_lines.append(f"Exam    : {exam}")
    report_lines.append(f"Category: {category}")
    report_lines.append(f"Gender  : {gender}")
    report_lines.append(f"Score   : {score_value}")
    report_lines.append("")

    summary = (
        result.get("summary")
        or result.get("analysis")
        or "No summary available."
    )

    report_lines.append("AI Summary")
    report_lines.append(summary)
    report_lines.append("")

    report_lines.append("Recommended Colleges")
    report_lines.append("-" * 40)

    for idx, college in enumerate(recommendations, start=1):

        report_lines.append(
            f"{idx}. {college.get('college_name', '-')}"
        )

        report_lines.append(
            f"   Branch : {college.get('branch', '-')}"
        )

        report_lines.append(
            f"   Match  : {college.get('match_percentage', '-')}"
        )

        report_lines.append(
            f"   Fees   : {college.get('fees', '-')}"
        )

        report_lines.append(
            f"   City   : {college.get('city', '-')}"
        )

        report_lines.append("")

    report_text = "\n".join(report_lines)

    st.text_area(
        "Preview Report",
        report_text,
        height=350,
    )

    st.download_button(
        "📄 Download Report (.txt)",
        report_text,
        file_name="MHT_CET_Counseling_Report.txt",
        mime="text/plain",
        use_container_width=True,
    )

# =====================================================
# SESSION SUMMARY
# =====================================================

if st.session_state.history:

    st.divider()
    st.header("📌 Session Summary")

    st.metric(
        "Searches Performed",
        len(st.session_state.history)
    )

    st.metric(
        "Favorite Colleges",
        len(st.session_state.get("favorites", []))
    )

    st.metric(
        "Current Recommendations",
        len(
            st.session_state.response.get(
                "recommendations",
                []
            )
        )
    )
    # =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        <h4>🎓 MHT-CET & JEE AI Counselor</h4>

        <p>
        Powered by AI • Streamlit UI • FastAPI Backend
        </p>

        <p>
        This application provides recommendations based on previous cutoff
        trends and AI analysis. Final admission depends on the official CAP
        rounds, seat availability, reservation policies, and government rules.
        </p>

        <br>

        <p style="font-size:12px;color:#9CA3AF;">
            © 2026 MHT-CET AI Counselor | Built with ❤️ using Streamlit
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# FINAL SUCCESS MESSAGE
# =====================================================

if st.session_state.response:

    st.success(
        "🎉 Your counseling session has been completed successfully."
    )

    st.info(
        "You can compare colleges, download your report, "
        "save favorites, and perform another search anytime."
    )

# =====================================================
# END OF APPLICATION
# =====================================================