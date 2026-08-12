# ============================================================
# AI POOKALAM DESIGNER
# STREAMLIT APPLICATION
#
# FLOW:
# Customer Inputs
#       ↓
# recommendation_engine.py
#       ↓
# recommendation_output.json
#       ↓
# pookalam_generator.py
#       ↓
# Generated Pookalam Prompt
#       ↓
# Download Prompt
#
# IMPORTANT:
# - Budget is mandatory
# - Other preferences are optional
# - No Design ID shown
# - No diameter shown in results
# - No confidence shown
# - No raw HTML shown
# - Only prompt download is provided
# ============================================================

import os
import sys
import json
import streamlit as st

# ============================================================
# WINDOWS UTF-8
# ============================================================

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RECOMMENDATION_OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "recommendation_output.json"
)

PROMPT_FILE = os.path.join(
    BASE_DIR,
    "pookalam",
    "pookalam_prompt.txt"
)


# ============================================================
# IMPORT RECOMMENDATION ENGINE
# ============================================================

try:
    from recommendation_engine import (
        recommend_pookalam,
        get_ui_options
    )
except Exception as error:
    st.error(
        "Unable to load recommendation_engine.py."
    )
    st.exception(error)
    st.stop()


# ============================================================
# IMPORT PROMPT GENERATOR
# ============================================================

try:
    from pookalam_generator import (
        generate_prompt_from_file
    )
except Exception as error:
    st.error(
        "Unable to load pookalam_generator.py."
    )
    st.exception(error)
    st.stop()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Pookalam Designer",
    page_icon="🌼",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
#
# NOTE:
# This is CSS injected intentionally for styling only.
# No result data is rendered using HTML.
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        linear-gradient(
            180deg,
            #fffaf0 0%,
            #fffdf7 45%,
            #fff8e8 100%
        );
    }

    .main-title {
    color: #4A2C20 !important;
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    }

    .subtitle {
    color: #5A4035 !important;
    font-size: 18px;
    text-align: center;
    margin-bottom: 25px;
    }

    .section-title {
    color: #4A2C20 !important;
    font-size: 25px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 15px;
    }

    .prompt-box {
        background-color: #fffdf7;
        border: 1px solid #eadfca;
        border-radius: 14px;
        padding: 18px;
        line-height: 1.7;
        font-size: 16px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
        min-height: 48px;
    }

    div.stDownloadButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
        min-height: 48px;
    }
    
    label,
    .stMarkdown,
    .stText,
    p,
    span {
       color: #3D2B24 !important;
    }

    .stDownloadButton > button {
    background-color: #8B4513 !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
    }

    .stDownloadButton > button p {
    color: #FFFFFF !important;
    }

    .stDownloadButton > button span {
    color: #FFFFFF !important;
    }

    .stDownloadButton > button div {
    color: #FFFFFF !important;
    }

    .stDownloadButton > button:hover {
    background-color: #6F350F !important;
    color: #FFFFFF !important;
    }

    .stDownloadButton > button:hover p,
    .stDownloadButton > button:hover span,
    .stDownloadButton > button:hover div {
    color: #FFFFFF !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌼 AI Pookalam Designer 🌼</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    "Create a beautiful Kerala Onam Pookalam "
    "based on your budget and preferences."
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# GET UI OPTIONS
# ============================================================

try:
    ui_options = get_ui_options()
except Exception as error:
    st.error(
        "Unable to load Pookalam options."
    )
    st.exception(error)
    st.stop()


# ============================================================
# SAFE OPTION HELPER
# ============================================================

def safe_options(
    values,
    default="Any"
):
    """
    Clean dropdown options.
    Ensures Any is available.
    """

    cleaned = []

    if values:
        for value in values:
            text = str(value).strip()

            if text and text not in cleaned:
                cleaned.append(text)

    if default not in cleaned:
        cleaned.append(default)

    return cleaned


themes = safe_options(
    ui_options.get("themes", [])
)

styles = safe_options(
    ui_options.get("styles", [])
)

occasions = safe_options(
    ui_options.get("occasions", [])
)

complexities = safe_options(
    ui_options.get("complexities", [])
)

colors = safe_options(
    ui_options.get("colors", [])
)


# ============================================================
# CUSTOMER INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">🌸 Tell Us About Your Pookalam</div>',
    unsafe_allow_html=True
)

st.info(
    "💡 Budget is required. "
    "All other preferences are optional."
)


# ============================================================
# ROW 1
# ============================================================

col1, col2 = st.columns(2)


with col1:

    budget = st.number_input(
        "💰 Flower Budget (₹) *",
        min_value=1.0,
        value=2200.0,
        step=100.0,
        format="%.2f",
        help="Enter the maximum amount you want to spend on flowers."
    )


with col2:

    maximum_diameter = st.number_input(
        "📏 Maximum Diameter (feet)",
        min_value=0.0,
        value=0.0,
        step=0.5,
        format="%.1f",
        help="Enter the maximum diameter. Keep 0 for Any."
    )


# ============================================================
# ROW 2
# ============================================================

col1, col2 = st.columns(2)


with col1:

    occasion = st.selectbox(
        "🎉 Occasion",
        occasions,
        index=(
            occasions.index("Any")
            if "Any" in occasions
            else 0
        )
    )


with col2:

    theme = st.selectbox(
        "🎭 Theme",
        themes,
        index=(
            themes.index("Any")
            if "Any" in themes
            else 0
        )
    )


# ============================================================
# ROW 3
# ============================================================

col1, col2 = st.columns(2)


with col1:

    style = st.selectbox(
        "🌺 Style",
        styles,
        index=(
            styles.index("Any")
            if "Any" in styles
            else 0
        )
    )


with col2:

    complexity = st.selectbox(
        "✨ Complexity",
        complexities,
        index=(
            complexities.index("Any")
            if "Any" in complexities
            else 0
        )
    )


# ============================================================
# ROW 4
# ============================================================

color_preference = st.selectbox(
    "🎨 Colour Preference",
    colors,
    index=(
        colors.index("Any")
        if "Any" in colors
        else 0
    )
)


# ============================================================
# DIAMETER HANDLING
# ============================================================

if maximum_diameter <= 0:
    max_diameter_value = None
else:
    max_diameter_value = maximum_diameter


# ============================================================
# FIND BEST POOKALAM BUTTON
# ============================================================

st.markdown("")


find_button = st.button(
    "🌼 Find My Best Pookalam",
    type="primary",
    use_container_width=True
)


# ============================================================
# RECOMMENDATION PROCESS
# ============================================================

if find_button:

    # --------------------------------------------------------
    # VALIDATE BUDGET
    # --------------------------------------------------------

    if budget <= 0:

        st.error(
            "Please enter a valid flower budget."
        )

        st.stop()


    # --------------------------------------------------------
    # SPINNER
    # --------------------------------------------------------

    with st.spinner(
        "🌸 Finding the best Pookalam for you..."
    ):

        try:

            # =================================================
            # CALL RECOMMENDATION ENGINE
            # =================================================

            result = recommend_pookalam(

                budget=budget,

                occasion=occasion,

                theme=theme,

                style=style,

                complexity=complexity,

                color_preference=color_preference,

                max_diameter=max_diameter_value,

                save_output=True
            )


        except Exception as error:

            st.error(
                "Something went wrong while generating "
                "the recommendation."
            )

            st.exception(error)

            st.stop()


    # ========================================================
    # CHECK RECOMMENDATION RESULT
    # ========================================================

    if not isinstance(result, dict):

        st.error(
            "Invalid recommendation result."
        )

        st.stop()


    if not result.get("success", False):

        message = result.get(
            "message",
            "No suitable Pookalam was found."
        )

        st.warning(
            f"🌼 {message}"
        )

        st.stop()


    # ========================================================
    # GET RECOMMENDATION
    # ========================================================

    recommendation = result.get(
        "recommendation",
        {}
    )


    if not recommendation:

        st.error(
            "No recommendation was returned."
        )

        st.stop()


    # ========================================================
    # SAVE RESULT IN SESSION
    # ========================================================

    st.session_state[
        "recommendation_result"
    ] = result


    # ========================================================
    # BEST RECOMMENDED POOKALAM
    # ========================================================

    st.markdown("")

    st.markdown(
        '<div class="section-title">'
        "🌼 Best Recommended Pookalam"
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # RESULT METRICS
    #
    # ONLY:
    # - Flower Cost
    # - Remaining Budget
    # - Recommendation Score
    #
    # No Design ID
    # No Diameter
    # No Confidence
    # ========================================================

    flower_cost = float(
        recommendation.get(
            "estimated_flower_cost",
            0
        )
    )

    remaining_budget = float(
        recommendation.get(
            "remaining_budget",
            0
        )
    )

    recommendation_score = float(
        recommendation.get(
            "final_score",
            0
        )
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🌸 Flower Cost",
            "₹{:,.2f}".format(
                flower_cost
            )
        )


    with col2:

        st.metric(
            "💰 Remaining Budget",
            "₹{:,.2f}".format(
                remaining_budget
            )
        )


    with col3:

        st.metric(
            "⭐ Recommendation Score",
            "{:.1f}%".format(
                recommendation_score
            )
        )


    # ========================================================
    # FLOWERS USED
    # ========================================================

    flowers = result.get(
        "flowers",
        []
    )


    if flowers:

        st.markdown(
            '<div class="section-title">'
            "🌺 Flowers Required"
            "</div>",
            unsafe_allow_html=True
        )


        flower_rows = []


        for flower in flowers:

            flower_name = str(
                flower.get(
                    "name",
                    ""
                )
            ).strip()

            quantity = float(
                flower.get(
                    "quantity_kg",
                    0
                )
            )

            cost = float(
                flower.get(
                    "estimated_cost",
                    0
                )
            )


            if flower_name:

                flower_rows.append(
                    {
                        "Flower": flower_name,
                        "Quantity": (
                            "{:.2f} kg".format(
                                quantity
                            )
                        ),
                        "Estimated Cost": (
                            "₹{:,.2f}".format(
                                cost
                            )
                        )
                    }
                )


        if flower_rows:

            st.dataframe(
                flower_rows,
                use_container_width=True,
                hide_index=True
            )


    # ========================================================
    # GENERATE PROMPT
    #
    # IMPORTANT:
    # Prompt is generated ONLY by
    # pookalam_generator.py
    # ========================================================

    st.markdown("")

    with st.spinner(
        "✨ Creating your Pookalam generation prompt..."
    ):

        try:

            # Make sure recommendation_output.json exists.
            #
            # recommendation_engine.py has already created it.

            if not os.path.isfile(
                RECOMMENDATION_OUTPUT_FILE
            ):

                raise FileNotFoundError(
                    "recommendation_output.json "
                    "was not created."
                )


            prompt_result = (
                generate_prompt_from_file(
                    RECOMMENDATION_OUTPUT_FILE
                )
            )


        except Exception as error:

            st.error(
                "Recommendation was created, but the "
                "Pookalam prompt could not be generated."
            )

            st.exception(error)

            st.stop()


    # ========================================================
    # GET GENERATED PROMPT
    # ========================================================

    generated_prompt = ""

    if isinstance(
        prompt_result,
        dict
    ):

        generated_prompt = str(
            prompt_result.get(
                "prompt",
                ""
            )
        ).strip()


    if not generated_prompt:

        st.error(
            "The Pookalam generator returned an empty prompt."
        )

        st.stop()


    # ========================================================
    # SAVE PROMPT IN SESSION
    # ========================================================

    st.session_state[
        "generated_prompt"
    ] = generated_prompt


    # ========================================================
    # PROMPT SECTION
    # ========================================================

    st.markdown("")

    st.markdown(
        '<div class="section-title">'
        "✨ Pookalam Generation Prompt"
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # DISPLAY PROMPT
    #
    # st.code() is intentionally NOT used.
    # It would make the prompt look like code.
    # ========================================================

    st.text_area(
        "Generated Prompt",
        value=generated_prompt,
        height=300,
        disabled=True,
        label_visibility="collapsed"
    )


    # ========================================================
    # ONLY DOWNLOAD OPTION
    # ========================================================

    st.download_button(
        label="⬇️ Download Pookalam Prompt",
        data=generated_prompt,
        file_name="pookalam_prompt.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# DISPLAY PREVIOUS RESULT AFTER STREAMLIT RERUN
#
# This keeps the prompt available after widgets rerun.
# ============================================================

elif (
    "recommendation_result"
    in st.session_state
    and
    "generated_prompt"
    in st.session_state
):

    result = st.session_state[
        "recommendation_result"
    ]

    recommendation = result.get(
        "recommendation",
        {}
    )

    generated_prompt = st.session_state[
        "generated_prompt"
    ]


    # ========================================================
    # BEST RECOMMENDED POOKALAM
    # ========================================================

    st.markdown("")

    st.markdown(
        '<div class="section-title">'
        "🌼 Best Recommended Pookalam"
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # RESULT METRICS
    # ========================================================

    flower_cost = float(
        recommendation.get(
            "estimated_flower_cost",
            0
        )
    )

    remaining_budget = float(
        recommendation.get(
            "remaining_budget",
            0
        )
    )

    recommendation_score = float(
        recommendation.get(
            "final_score",
            0
        )
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🌸 Flower Cost",
            "₹{:,.2f}".format(
                flower_cost
            )
        )


    with col2:

        st.metric(
            "💰 Remaining Budget",
            "₹{:,.2f}".format(
                remaining_budget
            )
        )


    with col3:

        st.metric(
            "⭐ Recommendation Score",
            "{:.1f}%".format(
                recommendation_score
            )
        )


    # ========================================================
    # FLOWERS
    # ========================================================

    flowers = result.get(
        "flowers",
        []
    )


    if flowers:

        st.markdown(
            '<div class="section-title">'
            "🌺 Flowers Required"
            "</div>",
            unsafe_allow_html=True
        )


        flower_rows = []


        for flower in flowers:

            flower_name = str(
                flower.get(
                    "name",
                    ""
                )
            ).strip()

            quantity = float(
                flower.get(
                    "quantity_kg",
                    0
                )
            )

            cost = float(
                flower.get(
                    "estimated_cost",
                    0
                )
            )


            if flower_name:

                flower_rows.append(
                    {
                        "Flower": flower_name,
                        "Quantity": (
                            "{:.2f} kg".format(
                                quantity
                            )
                        ),
                        "Estimated Cost": (
                            "₹{:,.2f}".format(
                                cost
                            )
                        )
                    }
                )


        if flower_rows:

            st.dataframe(
                flower_rows,
                use_container_width=True,
                hide_index=True
            )


    # ========================================================
    # PROMPT
    # ========================================================

    st.markdown("")

    st.markdown(
        '<div class="section-title">'
        "✨ Pookalam Generation Prompt"
        "</div>",
        unsafe_allow_html=True
    )


    st.text_area(
        "Generated Prompt",
        value=generated_prompt,
        height=300,
        disabled=True,
        label_visibility="collapsed"
    )


    # ========================================================
    # ONLY DOWNLOAD BUTTON
    # ========================================================

    st.download_button(
        label="⬇️ Download Pookalam Prompt",
        data=generated_prompt,
        file_name="pookalam_prompt.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("")

st.caption(
    "🌼 AI Pookalam Designer • "
    "Kerala Onam Floral Design Recommendation"
)