# ============================================================
# AI POOKALAM DESIGNER
# RECOMMENDATION ENGINE
# STREAMLIT / UI VERSION
#
# IMPORTANT:
# Recommendation logic is preserved.
# Only terminal input/output has been converted to
# function-based input/output for Streamlit.
# ============================================================

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd


# ============================================================
# WINDOWS UTF-8 FIX
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

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

DESIGN_FILE = os.path.join(
    DATASET_DIR,
    "design_flowers.csv"
)

PRICE_FILE = os.path.join(
    DATASET_DIR,
    "flower_prices.csv"
)

POOKALAM_FILE = os.path.join(
    DATASET_DIR,
    "pookalam_processed.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "models",
    "best_recommendation_model.pkl"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "recommendation_output.json"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value, default=""):
    """
    Safely convert a value to clean text.
    """

    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except Exception:
        pass

    text = str(value).strip()

    if text == "":
        return default

    return text


def normalize_text(value):
    """
    Normalize text for comparison.
    """

    return clean_text(value).lower().strip()


def safe_float(value, default=0.0):
    """
    Safely convert a value to float.
    """

    try:

        if value is None:
            return default

        if isinstance(value, str):

            if value.strip().lower() == "any":
                return default

        if pd.isna(value):
            return default

        return float(value)

    except (ValueError, TypeError):

        return default


def clamp(
    value,
    minimum=0.0,
    maximum=100.0
):
    """
    Restrict score to a range.
    """

    return max(
        minimum,
        min(
            maximum,
            float(value)
        )
    )


def find_column(
    df,
    possible_names
):
    """
    Find a column using case-insensitive matching.
    """

    columns_lower = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for name in possible_names:

        key = name.strip().lower()

        if key in columns_lower:
            return columns_lower[key]

    return None


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

required_files = {

    "design_flowers.csv":
        DESIGN_FILE,

    "flower_prices.csv":
        PRICE_FILE,

    "pookalam_processed.csv":
        POOKALAM_FILE,

    "best_recommendation_model.pkl":
        MODEL_FILE
}


missing_files = []

for file_name, file_path in required_files.items():

    if not os.path.exists(file_path):

        missing_files.append(
            (
                file_name,
                file_path
            )
        )


if missing_files:

    error_message = (
        "Required file(s) not found:\n\n"
    )

    for file_name, file_path in missing_files:

        error_message += (
            f"Missing: {file_name}\n"
            f"Expected: {file_path}\n\n"
        )

    raise FileNotFoundError(
        error_message
    )


# ============================================================
# LOAD DATA
# ============================================================

try:

    design_flowers = pd.read_csv(
        DESIGN_FILE
    )

    flower_prices = pd.read_csv(
        PRICE_FILE
    )

    designs = pd.read_csv(
        POOKALAM_FILE
    )

    model = joblib.load(
        MODEL_FILE
    )

except Exception as error:

    raise RuntimeError(
        f"Error while loading recommendation files: {error}"
    ) from error


# ============================================================
# FIND DESIGN COLUMNS
# ============================================================

DESIGN_ID_COL = find_column(
    designs,
    [
        "design_id",
        "id",
        "pookalam_id"
    ]
)

THEME_COL = find_column(
    designs,
    [
        "theme"
    ]
)

STYLE_COL = find_column(
    designs,
    [
        "style"
    ]
)

OCCASION_COL = find_column(
    designs,
    [
        "occasion"
    ]
)

DIFFICULTY_COL = find_column(
    designs,
    [
        "difficulty",
        "complexity"
    ]
)

DIAMETER_COL = find_column(
    designs,
    [
        "diameter_ft",
        "diameter",
        "maximum_diameter"
    ]
)


# ============================================================
# FIND FLOWER COLUMNS
# ============================================================

DF_DESIGN_ID_COL = find_column(
    design_flowers,
    [
        "design_id",
        "id",
        "pookalam_id"
    ]
)

DF_FLOWER_COL = find_column(
    design_flowers,
    [
        "flower",
        "flower_name",
        "flower_type"
    ]
)

DF_QUANTITY_COL = find_column(
    design_flowers,
    [
        "quantity_kg",
        "quantity",
        "kg",
        "weight"
    ]
)


# ============================================================
# FIND PRICE COLUMNS
# ============================================================

FP_FLOWER_COL = find_column(
    flower_prices,
    [
        "flower",
        "flower_name",
        "flower_type"
    ]
)

FP_PRICE_COL = find_column(
    flower_prices,
    [
        "price_per_kg",
        "price",
        "cost_per_kg"
    ]
)


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = {

    "design_id":
        DESIGN_ID_COL,

    "theme":
        THEME_COL,

    "style":
        STYLE_COL,

    "occasion":
        OCCASION_COL,

    "difficulty":
        DIFFICULTY_COL,

    "diameter":
        DIAMETER_COL,

    "design flower design_id":
        DF_DESIGN_ID_COL,

    "design flower name":
        DF_FLOWER_COL,

    "design flower quantity":
        DF_QUANTITY_COL,

    "flower price flower":
        FP_FLOWER_COL,

    "flower price":
        FP_PRICE_COL
}


missing_columns = []

for column_name, actual_column in required_columns.items():

    if actual_column is None:

        missing_columns.append(
            column_name
        )


if missing_columns:

    error_message = (
        "Required CSV columns are missing.\n\n"
    )

    for column in missing_columns:

        error_message += (
            f"- {column}\n"
        )

    error_message += (
        "\nAvailable design columns:\n"
    )

    error_message += (
        f"{list(designs.columns)}\n\n"
    )

    error_message += (
        "Available design flower columns:\n"
    )

    error_message += (
        f"{list(design_flowers.columns)}\n\n"
    )

    error_message += (
        "Available flower price columns:\n"
    )

    error_message += (
        f"{list(flower_prices.columns)}"
    )

    raise ValueError(
        error_message
    )


# ============================================================
# STANDARDIZE FLOWER DATA
# ============================================================

design_flowers["_design_id"] = (
    design_flowers[
        DF_DESIGN_ID_COL
    ]
    .astype(str)
    .str.strip()
)

design_flowers["_flower"] = (
    design_flowers[
        DF_FLOWER_COL
    ]
    .astype(str)
    .str.strip()
)

design_flowers["_quantity"] = (
    pd.to_numeric(
        design_flowers[
            DF_QUANTITY_COL
        ],
        errors="coerce"
    )
    .fillna(0)
)


# ============================================================
# STANDARDIZE PRICE DATA
# ============================================================

flower_prices["_flower"] = (
    flower_prices[
        FP_FLOWER_COL
    ]
    .astype(str)
    .str.strip()
)

flower_prices["_price_per_kg"] = (
    pd.to_numeric(
        flower_prices[
            FP_PRICE_COL
        ],
        errors="coerce"
    )
    .fillna(0)
)


# ============================================================
# CREATE PRICE LOOKUP
# ============================================================

price_dict = {}

for _, row in flower_prices.iterrows():

    flower_name = normalize_text(
        row["_flower"]
    )

    price = safe_float(
        row["_price_per_kg"]
    )

    if flower_name and price > 0:

        price_dict[
            flower_name
        ] = price


# ============================================================
# FLOWER REQUIREMENTS
# ============================================================

def get_flower_requirements(
    design_id
):
    """
    Return flower requirements for a design.
    """

    design_id = str(
        design_id
    ).strip()

    rows = design_flowers[
        design_flowers["_design_id"]
        == design_id
    ]

    requirements = []

    for _, row in rows.iterrows():

        flower = clean_text(
            row["_flower"]
        )

        quantity = safe_float(
            row["_quantity"]
        )

        if not flower or quantity <= 0:
            continue

        price = price_dict.get(
            normalize_text(flower),
            0.0
        )

        if price <= 0:
            continue

        cost = quantity * price

        requirements.append(
            {
                "flower": flower,
                "quantity": quantity,
                "price_per_kg": price,
                "cost": cost
            }
        )

    return requirements


# ============================================================
# DESIGN COST
# ============================================================

def calculate_design_cost(
    design_id
):
    """
    Calculate total flower cost for a design.
    """

    flowers = get_flower_requirements(
        design_id
    )

    total = 0.0

    for flower in flowers:

        total += flower["cost"]

    return round(
        total,
        2
    )


# ============================================================
# STANDARDIZE DESIGN IDS
# ============================================================

designs["_design_id_string"] = (
    designs[
        DESIGN_ID_COL
    ]
    .astype(str)
    .str.strip()
)


# ============================================================
# CALCULATE FLOWER COST FOR ALL DESIGNS
# ============================================================

designs["_calculated_cost"] = (
    designs[
        "_design_id_string"
    ]
    .apply(
        calculate_design_cost
    )
)


# ============================================================
# FLOWER DATA VALIDATION
# ============================================================

designs["_flower_count"] = (
    designs[
        "_design_id_string"
    ]
    .apply(
        lambda x:
        len(
            get_flower_requirements(x)
        )
    )
)


# ============================================================
# REMOVE INVALID DESIGNS
# ============================================================

designs = designs[
    (designs["_calculated_cost"] > 0)
    &
    (designs["_flower_count"] > 0)
].copy()


if designs.empty:

    raise ValueError(
        "No designs contain valid flower data."
    )


# ============================================================
# UI OPTIONS
# ============================================================

def get_ui_options():
    """
    Return values that Streamlit can use to populate
    selectboxes/dropdowns.
    """

    available_themes = sorted(
        list(
            dict.fromkeys(
                [
                    clean_text(value)
                    for value in designs[
                        THEME_COL
                    ].dropna()
                    if clean_text(value)
                ]
            )
        )
    )

    available_styles = sorted(
        list(
            dict.fromkeys(
                [
                    clean_text(value)
                    for value in designs[
                        STYLE_COL
                    ].dropna()
                    if clean_text(value)
                ]
            )
        )
    )

    if "Any" not in available_themes:

        available_themes.append(
            "Any"
        )

    if "Any" not in available_styles:

        available_styles.append(
            "Any"
        )

    return {

        "themes":
            available_themes,

        "styles":
            available_styles,

        "occasions":
            [
                "Competition",
                "Home",
                "Office",
                "Onam",
                "School",
                "Any"
            ],

        "complexities":
            [
                "Easy",
                "Medium",
                "Hard",
                "Any"
            ],

        "colors":
            [
                "Green",
                "Orange",
                "Pink",
                "Purple",
                "Red",
                "White",
                "Yellow",
                "Any"
            ]
    }


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def recommend_pookalam(
    budget,
    occasion="Any",
    theme="Any",
    style="Any",
    complexity="Any",
    color_preference="Any",
    max_diameter=None,
    save_output=True
):
    """
    Main recommendation function.

    Streamlit should call this function.

    IMPORTANT:
    The recommendation logic is kept from the original
    terminal-based version.

    Parameters
    ----------
    budget : float
        Maximum customer budget.

    occasion : str
        Competition / Home / Office / Onam / School / Any

    theme : str
        Selected theme.

    style : str
        Selected style.

    complexity : str
        Easy / Medium / Hard / Any

    color_preference : str
        Selected color.

    max_diameter : float or None
        Maximum diameter in feet.
        None means Any.

    save_output : bool
        Whether to save recommendation_output.json.

    Returns
    -------
    dict
        Recommendation data for Streamlit.
    """

    # ========================================================
    # VALIDATE INPUT
    # ========================================================

    budget = safe_float(
        budget,
        0.0
    )

    if budget <= 0:

        raise ValueError(
            "Budget must be greater than 0."
        )

    occasion = clean_text(
        occasion,
        "Any"
    )

    theme = clean_text(
        theme,
        "Any"
    )

    style = clean_text(
        style,
        "Any"
    )

    complexity = clean_text(
        complexity,
        "Any"
    )

    color_preference = clean_text(
        color_preference,
        "Any"
    )

    if max_diameter in [
        None,
        "",
        0,
        "0",
        "Any"
    ]:

        max_diameter = None

    else:

        max_diameter = safe_float(
            max_diameter,
            None
        )

        if max_diameter is not None:

            if max_diameter <= 0:

                max_diameter = None


    # ========================================================
    # PREPARE DESIGN INFORMATION
    # ========================================================

    working_designs = designs.copy()

    working_designs["_diameter"] = (
        pd.to_numeric(
            working_designs[
                DIAMETER_COL
            ],
            errors="coerce"
        )
        .fillna(0)
    )


    # ========================================================
    # BASIC MATCH COLUMNS
    # ========================================================

    working_designs[
        "occasion_match"
    ] = (
        working_designs[
            OCCASION_COL
        ]
        .apply(normalize_text)
        ==
        normalize_text(occasion)
    )


    working_designs[
        "theme_match"
    ] = (
        working_designs[
            THEME_COL
        ]
        .apply(normalize_text)
        ==
        normalize_text(theme)
    )


    working_designs[
        "style_match"
    ] = (
        working_designs[
            STYLE_COL
        ]
        .apply(normalize_text)
        ==
        normalize_text(style)
    )


    working_designs[
        "complexity_match"
    ] = (
        working_designs[
            DIFFICULTY_COL
        ]
        .apply(normalize_text)
        ==
        normalize_text(complexity)
    )


    # ========================================================
    # COLOR MATCH
    # ========================================================

    COLOR_COLUMNS = []

    for color_column in [
        "primary_color",
        "secondary_color",
        "accent_color"
    ]:

        actual_column = find_column(
            working_designs,
            [color_column]
        )

        if actual_column is not None:

            COLOR_COLUMNS.append(
                actual_column
            )


    if color_preference == "Any":

        working_designs[
            "color_match"
        ] = True

    elif COLOR_COLUMNS:

        requested_color = normalize_text(
            color_preference
        )

        def check_color(row):

            for column in COLOR_COLUMNS:

                value = normalize_text(
                    row[column]
                )

                if requested_color in value:

                    return True

            return False


        working_designs[
            "color_match"
        ] = (
            working_designs.apply(
                check_color,
                axis=1
            )
        )

    else:

        working_designs[
            "color_match"
        ] = False


    # ========================================================
    # HARD CONSTRAINTS
    # ========================================================

    working_designs[
        "within_budget"
    ] = (
        working_designs[
            "_calculated_cost"
        ]
        <= budget
    )


    if max_diameter is None:

        working_designs[
            "diameter_match"
        ] = True

    else:

        working_designs[
            "diameter_match"
        ] = (
            working_designs[
                "_diameter"
            ]
            <= max_diameter
        )


    # ========================================================
    # THEME PRIORITY
    # ========================================================

    # Same logic as original version:
    # If theme is selected and matching designs exist,
    # rank only those designs.
    #
    # If no matching theme exists, retain original
    # fallback behavior.

    if theme != "Any":

        theme_candidates = (
            working_designs[
                working_designs[
                    "theme_match"
                ]
            ]
            .copy()
        )

        if not theme_candidates.empty:

            designs_for_ranking = (
                theme_candidates
                .copy()
            )

        else:

            designs_for_ranking = (
                working_designs
                .copy()
            )

    else:

        designs_for_ranking = (
            working_designs
            .copy()
        )


    # ========================================================
    # PREFERENCE MATCH COUNT
    # ========================================================

    specified_preferences = 0

    designs_for_ranking[
        "preference_match_count"
    ] = 0


    # --------------------------------------------------------
    # THEME
    # --------------------------------------------------------

    if theme != "Any":

        specified_preferences += 1

        designs_for_ranking[
            "preference_match_count"
        ] += (
            designs_for_ranking[
                "theme_match"
            ]
            .astype(int)
        )


    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    if style != "Any":

        specified_preferences += 1

        designs_for_ranking[
            "preference_match_count"
        ] += (
            designs_for_ranking[
                "style_match"
            ]
            .astype(int)
        )


    # --------------------------------------------------------
    # COMPLEXITY
    # --------------------------------------------------------

    if complexity != "Any":

        specified_preferences += 1

        designs_for_ranking[
            "preference_match_count"
        ] += (
            designs_for_ranking[
                "complexity_match"
            ]
            .astype(int)
        )


    # --------------------------------------------------------
    # OCCASION
    # --------------------------------------------------------

    if occasion != "Any":

        specified_preferences += 1

        designs_for_ranking[
            "preference_match_count"
        ] += (
            designs_for_ranking[
                "occasion_match"
            ]
            .astype(int)
        )


    # --------------------------------------------------------
    # COLOR
    # --------------------------------------------------------

    if color_preference != "Any":

        specified_preferences += 1

        designs_for_ranking[
            "preference_match_count"
        ] += (
            designs_for_ranking[
                "color_match"
            ]
            .astype(int)
        )


    # ========================================================
    # PREFERENCE SCORE
    # ========================================================

    PREFERENCE_WEIGHTS = {

        "theme": 30.0,

        "style": 25.0,

        "complexity": 20.0,

        "occasion": 15.0,

        "color": 10.0
    }


    def calculate_preference_score(row):

        total_weight = 0.0

        matched_weight = 0.0

        checks = []


        if theme != "Any":

            checks.append(
                (
                    "theme",
                    row[
                        "theme_match"
                    ]
                )
            )


        if style != "Any":

            checks.append(
                (
                    "style",
                    row[
                        "style_match"
                    ]
                )
            )


        if complexity != "Any":

            checks.append(
                (
                    "complexity",
                    row[
                        "complexity_match"
                    ]
                )
            )


        if occasion != "Any":

            checks.append(
                (
                    "occasion",
                    row[
                        "occasion_match"
                    ]
                )
            )


        if color_preference != "Any":

            checks.append(
                (
                    "color",
                    row[
                        "color_match"
                    ]
                )
            )


        for name, matched in checks:

            weight = (
                PREFERENCE_WEIGHTS[
                    name
                ]
            )

            total_weight += weight

            if bool(matched):

                matched_weight += weight


        if total_weight == 0:

            return 100.0


        return (
            matched_weight
            /
            total_weight
        ) * 100.0


    designs_for_ranking[
        "preference_score"
    ] = (
        designs_for_ranking.apply(
            calculate_preference_score,
            axis=1
        )
    )


    # ========================================================
    # EXACT MATCH
    # ========================================================

    if specified_preferences > 0:

        designs_for_ranking[
            "exact_preference_match"
        ] = (
            designs_for_ranking[
                "preference_match_count"
            ]
            ==
            specified_preferences
        )

    else:

        designs_for_ranking[
            "exact_preference_match"
        ] = True


    # ========================================================
    # BUDGET SUITABILITY
    # ========================================================

    def calculate_budget_score(cost):

        cost = safe_float(
            cost
        )

        if cost <= 0:

            return 0.0


        if cost > budget:

            return 0.0


        ratio = (
            cost
            /
            budget
        )


        # Ideal budget utilization
        if 0.70 <= ratio <= 0.90:

            return 100.0


        # Slightly below ideal
        if 0.60 <= ratio < 0.70:

            return 90.0


        # Very good utilization
        if 0.90 < ratio <= 1.00:

            return 95.0


        # Moderate utilization
        if 0.40 <= ratio < 0.60:

            return 75.0


        # Lower utilization
        if 0.25 <= ratio < 0.40:

            return 55.0


        # Very low utilization
        if 0.10 <= ratio < 0.25:

            return 30.0


        # Extremely low utilization
        return 15.0


    designs_for_ranking[
        "budget_suitability_score"
    ] = (
        designs_for_ranking[
            "_calculated_cost"
        ]
        .apply(
            calculate_budget_score
        )
    )


    # ========================================================
    # DIAMETER SCORE
    # ========================================================

    def calculate_diameter_score(row):

        diameter = safe_float(
            row["_diameter"]
        )

        if diameter <= 0:

            return 0.0


        if max_diameter is None:

            return 75.0


        if diameter > max_diameter:

            return 0.0


        ratio = (
            diameter
            /
            max_diameter
        )


        if ratio >= 0.85:

            return 100.0


        if ratio >= 0.70:

            return 90.0


        if ratio >= 0.50:

            return 80.0


        if ratio >= 0.30:

            return 70.0


        return 60.0


    designs_for_ranking[
        "diameter_score"
    ] = (
        designs_for_ranking.apply(
            calculate_diameter_score,
            axis=1
        )
    )


    # ========================================================
    # FLOWER VARIETY SCORE
    # ========================================================

    def calculate_flower_variety_score(
        design_id
    ):

        flowers = get_flower_requirements(
            design_id
        )

        count = len(
            flowers
        )


        if count >= 6:

            return 100.0


        if count == 5:

            return 90.0


        if count == 4:

            return 80.0


        if count == 3:

            return 70.0


        if count == 2:

            return 55.0


        return 40.0


    designs_for_ranking[
        "flower_variety_score"
    ] = (
        designs_for_ranking[
            "_design_id_string"
        ]
        .apply(
            calculate_flower_variety_score
        )
    )


    # ========================================================
    # ML TRAINING FEATURES
    # ========================================================

    TRAINING_FEATURES = [

        "budget",

        "theme",

        "style",

        "layers",

        "difficulty",

        "primary_flower",

        "secondary_flower",

        "accent_flower",

        "primary_color",

        "secondary_color",

        "accent_color",

        "diameter_ft",

        "estimated_time_hr",

        "people_required",

        "occasion",

        "flower_diversity",

        "color_diversity",

        "estimated_flower_cost"
    ]


    # ========================================================
    # PREPARE ML INPUT
    # ========================================================

    ml_input = pd.DataFrame(
        index=designs_for_ranking.index
    )


    for feature in TRAINING_FEATURES:

        if feature == "budget":

            ml_input[
                feature
            ] = budget


        elif feature == "estimated_flower_cost":

            ml_input[
                feature
            ] = pd.to_numeric(
                designs_for_ranking[
                    "_calculated_cost"
                ],
                errors="coerce"
            ).fillna(0)


        elif feature == "diameter_ft":

            ml_input[
                feature
            ] = pd.to_numeric(
                designs_for_ranking[
                    "_diameter"
                ],
                errors="coerce"
            ).fillna(0)


        elif feature in designs_for_ranking.columns:

            ml_input[
                feature
            ] = designs_for_ranking[
                feature
            ]


        else:

            if feature in [

                "theme",

                "style",

                "difficulty",

                "primary_flower",

                "secondary_flower",

                "accent_flower",

                "primary_color",

                "secondary_color",

                "accent_color",

                "occasion"

            ]:

                ml_input[
                    feature
                ] = ""

            else:

                ml_input[
                    feature
                ] = 0.0


    # ========================================================
    # CLEAN ML INPUT
    # ========================================================

    numeric_features = [

        "budget",

        "layers",

        "diameter_ft",

        "estimated_time_hr",

        "people_required",

        "flower_diversity",

        "color_diversity",

        "estimated_flower_cost"
    ]


    categorical_features = [

        "theme",

        "style",

        "difficulty",

        "primary_flower",

        "secondary_flower",

        "accent_flower",

        "primary_color",

        "secondary_color",

        "accent_color",

        "occasion"
    ]


    for column in numeric_features:

        ml_input[
            column
        ] = pd.to_numeric(
            ml_input[
                column
            ],
            errors="coerce"
        ).fillna(0)


    for column in categorical_features:

        ml_input[
            column
        ] = (
            ml_input[
                column
            ]
            .fillna("")
            .astype(str)
            .str.strip()
        )


    # ========================================================
    # ML PREDICTION
    # ========================================================

    try:

        predictions = model.predict(
            ml_input[
                TRAINING_FEATURES
            ]
        )


        if hasattr(
            model,
            "predict_proba"
        ):

            probabilities = (
                model.predict_proba(
                    ml_input[
                        TRAINING_FEATURES
                    ]
                )
            )

            confidence_values = (
                probabilities.max(
                    axis=1
                ) * 100
            )

        else:

            confidence_values = np.zeros(
                len(predictions)
            )


        designs_for_ranking[
            "ml_recommendation"
        ] = predictions


        designs_for_ranking[
            "ml_confidence"
        ] = confidence_values


    except Exception:

        designs_for_ranking[
            "ml_recommendation"
        ] = "Moderate"


        designs_for_ranking[
            "ml_confidence"
        ] = 0.0


    # ========================================================
    # ML SCORE
    # ========================================================

    def calculate_ml_score(
        category,
        confidence
    ):

        category = normalize_text(
            category
        )

        confidence = safe_float(
            confidence
        )


        if category == "excellent":

            base_score = 100.0


        elif category == "good":

            base_score = 80.0


        elif category == "moderate":

            base_score = 60.0


        elif category == "low":

            base_score = 35.0


        else:

            base_score = 50.0


        confidence_factor = (
            confidence
            /
            100.0
        )


        return (
            base_score * 0.80
            +
            confidence_factor
            * 100.0
            * 0.20
        )


    designs_for_ranking[
        "ml_score"
    ] = (
        designs_for_ranking.apply(
            lambda row:
            calculate_ml_score(
                row[
                    "ml_recommendation"
                ],
                row[
                    "ml_confidence"
                ]
            ),
            axis=1
        )
    )


    # ========================================================
    # FLOWER AVAILABILITY
    # ========================================================

    # Purchased flowers are NOT considered.
    #
    # Therefore this score represents the validity of the
    # flower composition, not customer-owned flowers.

    designs_for_ranking[
        "flower_availability_score"
    ] = 100.0


    # ========================================================
    # FINAL SCORE
    # ========================================================

    WEIGHT_PREFERENCE = 0.40

    WEIGHT_BUDGET = 0.25

    WEIGHT_ML = 0.15

    WEIGHT_DIAMETER = 0.10

    WEIGHT_FLOWERS = 0.10


    designs_for_ranking[
        "final_score"
    ] = (

        designs_for_ranking[
            "preference_score"
        ]
        *
        WEIGHT_PREFERENCE

        +

        designs_for_ranking[
            "budget_suitability_score"
        ]
        *
        WEIGHT_BUDGET

        +

        designs_for_ranking[
            "ml_score"
        ]
        *
        WEIGHT_ML

        +

        designs_for_ranking[
            "diameter_score"
        ]
        *
        WEIGHT_DIAMETER

        +

        designs_for_ranking[
            "flower_availability_score"
        ]
        *
        WEIGHT_FLOWERS
    )


    designs_for_ranking[
        "final_score"
    ] = (
        designs_for_ranking[
            "final_score"
        ]
        .apply(
            clamp
        )
    )


    # ========================================================
    # HARD CONSTRAINT FILTERING
    # ========================================================

    candidates = (
        designs_for_ranking[
            designs_for_ranking[
                "within_budget"
            ]
        ]
        .copy()
    )


    if max_diameter is not None:

        candidates = (
            candidates[
                candidates[
                    "diameter_match"
                ]
            ]
            .copy()
        )


    # ========================================================
    # NO CANDIDATE HANDLING
    # ========================================================

    if candidates.empty:

        result = {

            "success": False,

            "message":
                "No design satisfies the budget and "
                "diameter constraints.",

            "customer_requirements": {

                "budget":
                    budget,

                "occasion":
                    occasion,

                "theme":
                    theme,

                "style":
                    style,

                "complexity":
                    complexity,

                "color":
                    color_preference,

                "maximum_diameter_ft":
                    (
                        max_diameter
                        if max_diameter is not None
                        else "Any"
                    )
            },

            "top_3_recommendations":
                [],

            "recommendation":
                None,

            "flowers":
                [],

            "generation_requirements":
                None,

            "unmatched_requirements":
                [],

            "genai_instructions": {

                "use_recommended_flowers_only":
                    True,

                "do_not_invent_flowers":
                    True,

                "do_not_replace_recommended_flowers":
                    True,

                "use_recommended_style":
                    True,

                "use_recommended_theme":
                    True,

                "use_recommended_complexity":
                    True,

                "respect_customer_budget":
                    True,

                "respect_maximum_diameter":
                    True
            }
        }


        if save_output:

            try:

                with open(
                    OUTPUT_FILE,
                    "w",
                    encoding="utf-8"
                ) as json_file:

                    json.dump(
                        result,
                        json_file,
                        indent=4,
                        ensure_ascii=False
                    )

            except Exception:
                pass


        return result


    # ========================================================
    # EXACT PREFERENCE FILTER
    # ========================================================

    exact_candidates = (
        candidates[
            candidates[
                "exact_preference_match"
            ]
        ]
        .copy()
    )


    if not exact_candidates.empty:

        ranking_pool = (
            exact_candidates
            .copy()
        )

    else:

        ranking_pool = (
            candidates
            .copy()
        )


    # ========================================================
    # BUDGET DISTANCE
    # ========================================================

    ranking_pool[
        "_budget_distance_80"
    ] = (

        (
            ranking_pool[
                "_calculated_cost"
            ]
            /
            budget
        )
        - 0.80

    ).abs()


    # ========================================================
    # RANKING
    # ========================================================

    sort_columns = [

        "exact_preference_match",

        "preference_score",

        "final_score",

        "budget_suitability_score",

        "ml_score",

        "diameter_score",

        "flower_variety_score",

        "_budget_distance_80",

        "_calculated_cost"
    ]


    sort_ascending = [

        False,

        False,

        False,

        False,

        False,

        False,

        False,

        True,

        True
    ]


    ranking_pool = (
        ranking_pool
        .sort_values(
            by=sort_columns,
            ascending=sort_ascending
        )
    )


    # ========================================================
    # TOP 3
    # ========================================================

    results = (
        ranking_pool
        .head(3)
        .copy()
    )


    results = results.reset_index(
        drop=True
    )


    # ========================================================
    # UNMATCHED REQUIREMENTS
    # ========================================================

    def get_unmatched_requirements(
        row
    ):

        unmatched = []


        if theme != "Any":

            if not bool(
                row[
                    "theme_match"
                ]
            ):

                unmatched.append(
                    f"Theme: {theme}"
                )


        if style != "Any":

            if not bool(
                row[
                    "style_match"
                ]
            ):

                unmatched.append(
                    f"Style: {style}"
                )


        if complexity != "Any":

            if not bool(
                row[
                    "complexity_match"
                ]
            ):

                unmatched.append(
                    f"Complexity: {complexity}"
                )


        if occasion != "Any":

            if not bool(
                row[
                    "occasion_match"
                ]
            ):

                unmatched.append(
                    f"Occasion: {occasion}"
                )


        if color_preference != "Any":

            if not bool(
                row[
                    "color_match"
                ]
            ):

                unmatched.append(
                    f"Color: {color_preference}"
                )


        return unmatched


    # ========================================================
    # BEST RECOMMENDATION
    # ========================================================

    best = results.iloc[0]


    best_design_id = clean_text(
        best[
            DESIGN_ID_COL
        ]
    )


    best_flowers = (
        get_flower_requirements(
            best_design_id
        )
    )


    unmatched_requirements = (
        get_unmatched_requirements(
            best
        )
    )


    # ========================================================
    # FLOWER JSON
    # ========================================================

    flower_json = []


    for flower in best_flowers:

        flower_json.append(
            {

                "name":
                    flower[
                        "flower"
                    ],

                "quantity_kg":
                    round(
                        flower[
                            "quantity"
                        ],
                        2
                    ),

                "price_per_kg":
                    round(
                        flower[
                            "price_per_kg"
                        ],
                        2
                    ),

                "estimated_cost":
                    round(
                        flower[
                            "cost"
                        ],
                        2
                    )
            }
        )


    # ========================================================
    # GENERATION REQUIREMENTS
    # ========================================================

    generation_requirements = {

        "budget":
            budget,

        "occasion":
            occasion,

        "theme":
            theme,

        "style":
            style,

        "complexity":
            complexity,

        "color":
            color_preference,

        "maximum_diameter_ft":
            (
                max_diameter
                if max_diameter is not None
                else "Any"
            ),

        "recommended_design_id":
            best_design_id,

        "recommended_theme":
            clean_text(
                best[
                    THEME_COL
                ]
            ),

        "recommended_style":
            clean_text(
                best[
                    STYLE_COL
                ]
            ),

        "recommended_complexity":
            clean_text(
                best[
                    DIFFICULTY_COL
                ]
            ),

        "recommended_occasion":
            clean_text(
                best[
                    OCCASION_COL
                ]
            ),

        "recommended_diameter_ft":
            safe_float(
                best[
                    "_diameter"
                ]
            ),

        "recommended_flower_cost":
            safe_float(
                best[
                    "_calculated_cost"
                ]
            ),

        "unmatched_requirements":
            unmatched_requirements
    }


    # ========================================================
    # FINAL JSON
    # ========================================================

    recommendation_data = {

        "success":
            True,

        "project":
            "AI Pookalam Designer",

        "generated_by":
            "recommendation_engine.py",

        "customer_requirements": {

            "budget":
                budget,

            "occasion":
                occasion,

            "theme":
                theme,

            "style":
                style,

            "complexity":
                complexity,

            "color":
                color_preference,

            "maximum_diameter_ft":
                (
                    max_diameter
                    if max_diameter is not None
                    else "Any"
                )
        },


        "top_3_recommendations":
            [],


        "recommendation": {

            "rank":
                1,

            "design_id":
                best_design_id,

            "theme":
                clean_text(
                    best[
                        THEME_COL
                    ]
                ),

            "style":
                clean_text(
                    best[
                        STYLE_COL
                    ]
                ),

            "difficulty":
                clean_text(
                    best[
                        DIFFICULTY_COL
                    ]
                ),

            "occasion":
                clean_text(
                    best[
                        OCCASION_COL
                    ]
                ),

            "diameter_ft":
                safe_float(
                    best[
                        "_diameter"
                    ]
                ),

            "estimated_flower_cost":
                safe_float(
                    best[
                        "_calculated_cost"
                    ]
                ),

            "remaining_budget":
                round(
                    budget
                    -
                    safe_float(
                        best[
                            "_calculated_cost"
                        ]
                    ),
                    2
                ),

            "ml_recommendation":
                clean_text(
                    best[
                        "ml_recommendation"
                    ]
                ),

            "ml_confidence":
                safe_float(
                    best[
                        "ml_confidence"
                    ]
                ),

            "preferences_matched":
                int(
                    best[
                        "preference_match_count"
                    ]
                ),

            "total_preferences":
                specified_preferences,

            "preference_score":
                round(
                    safe_float(
                        best[
                            "preference_score"
                        ]
                    ),
                    2
                ),

            "budget_suitability_score":
                round(
                    safe_float(
                        best[
                            "budget_suitability_score"
                        ]
                    ),
                    2
                ),

            "ml_score":
                round(
                    safe_float(
                        best[
                            "ml_score"
                        ]
                    ),
                    2
                ),

            "diameter_score":
                round(
                    safe_float(
                        best[
                            "diameter_score"
                        ]
                    ),
                    2
                ),

            "final_score":
                round(
                    safe_float(
                        best[
                            "final_score"
                        ]
                    ),
                    2
                )
        },


        "flowers":
            flower_json,


        "generation_requirements":
            generation_requirements,


        "unmatched_requirements":
            unmatched_requirements,


        "genai_instructions": {

            "use_recommended_flowers_only":
                True,

            "do_not_invent_flowers":
                True,

            "do_not_replace_recommended_flowers":
                True,

            "use_recommended_style":
                True,

            "use_recommended_theme":
                True,

            "use_recommended_complexity":
                True,

            "respect_customer_budget":
                True,

            "respect_maximum_diameter":
                True
        }
    }


    # ========================================================
    # BUILD TOP 3 JSON
    # ========================================================

    for rank, (_, row) in enumerate(
        results.iterrows(),
        start=1
    ):

        design_id = clean_text(
            row[
                DESIGN_ID_COL
            ]
        )


        design_flowers_json = []


        for flower in get_flower_requirements(
            design_id
        ):

            design_flowers_json.append(
                {

                    "name":
                        flower[
                            "flower"
                        ],

                    "quantity_kg":
                        round(
                            flower[
                                "quantity"
                            ],
                            2
                        ),

                    "price_per_kg":
                        round(
                            flower[
                                "price_per_kg"
                            ],
                            2
                        ),

                    "estimated_cost":
                        round(
                            flower[
                                "cost"
                            ],
                            2
                        )
                }
            )


        recommendation_data[
            "top_3_recommendations"
        ].append(
            {

                "rank":
                    rank,

                "design_id":
                    design_id,

                "theme":
                    clean_text(
                        row[
                            THEME_COL
                        ]
                    ),

                "style":
                    clean_text(
                        row[
                            STYLE_COL
                        ]
                    ),

                "difficulty":
                    clean_text(
                        row[
                            DIFFICULTY_COL
                        ]
                    ),

                "occasion":
                    clean_text(
                        row[
                            OCCASION_COL
                        ]
                    ),

                "diameter_ft":
                    safe_float(
                        row[
                            "_diameter"
                        ]
                    ),

                "estimated_flower_cost":
                    safe_float(
                        row[
                            "_calculated_cost"
                        ]
                    ),

                "remaining_budget":
                    round(
                        budget
                        -
                        safe_float(
                            row[
                                "_calculated_cost"
                            ]
                        ),
                        2
                    ),

                "ml_recommendation":
                    clean_text(
                        row[
                            "ml_recommendation"
                        ]
                    ),

                "ml_confidence":
                    safe_float(
                        row[
                            "ml_confidence"
                        ]
                    ),

                "preferences_matched":
                    int(
                        row[
                            "preference_match_count"
                        ]
                    ),

                "total_preferences":
                    specified_preferences,

                "preference_score":
                    round(
                        safe_float(
                            row[
                                "preference_score"
                            ]
                        ),
                        2
                    ),

                "budget_suitability_score":
                    round(
                        safe_float(
                            row[
                                "budget_suitability_score"
                            ]
                        ),
                        2
                    ),

                "ml_score":
                    round(
                        safe_float(
                            row[
                                "ml_score"
                            ]
                        ),
                        2
                    ),

                "diameter_score":
                    round(
                        safe_float(
                            row[
                                "diameter_score"
                            ]
                        ),
                        2
                    ),

                "final_score":
                    round(
                        safe_float(
                            row[
                                "final_score"
                            ]
                        ),
                        2
                    ),

                "flowers":
                    design_flowers_json
            }
        )


    # ========================================================
    # SAVE JSON
    # ========================================================

    if save_output:

        try:

            with open(
                OUTPUT_FILE,
                "w",
                encoding="utf-8"
            ) as json_file:

                json.dump(
                    recommendation_data,
                    json_file,
                    indent=4,
                    ensure_ascii=False
                )

        except Exception as error:

            # Do not fail the Streamlit recommendation
            # merely because JSON saving failed.
            recommendation_data[
                "output_save_error"
            ] = str(error)


    # ========================================================
    # RETURN RESULT TO STREAMLIT
    # ========================================================

    return recommendation_data


# ============================================================
# OPTIONAL DIRECT TEST
#
# This section runs ONLY when:
#
# python recommendation_engine.py
#
# It does NOT run when imported by Streamlit.
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 75)
    print("AI POOKALAM DESIGNER - RECOMMENDATION ENGINE")
    print("=" * 75)
    print()

    print(
        "This recommendation engine is now UI-ready."
    )

    print()

    print(
        "It is designed to be called from Streamlit using:"
    )

    print()

    print(
        "recommend_pookalam("
    )

    print(
        "    budget=1000,"
    )

    print(
        "    occasion='Home',"
    )

    print(
        "    theme='Any',"
    )

    print(
        "    style='Traditional',"
    )

    print(
        "    complexity='Easy',"
    )

    print(
        "    color_preference='White',"
    )

    print(
        "    max_diameter=6"
    )

    print(
        ")"
    )

    print()

    print(
        "No terminal input is required."
    )

    print()

    print("=" * 75)