# ============================================================
# AI POOKALAM DESIGNER
# GENAI PROMPT GENERATOR
#
# Purpose:
#   Converts recommendation_output.json into a GenAI prompt.
#
# Logic:
#   1. Recommended flowers remain the PRIMARY flowers.
#   2. Additional complementary flowers are allowed.
#   3. Final flower cost must NOT exceed customer budget.
#   4. Customer color preference must be incorporated.
#   5. Maximum diameter must be respected.
#   6. GenAI is asked to provide final flower quantity/cost
#      breakdown after creating the design.
# ============================================================

import os
import json


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RECOMMENDATION_FILE = os.path.join(
    BASE_DIR,
    "recommendation_output.json"
)

PROMPT_DIR = os.path.join(
    BASE_DIR,
    "pookalam"
)

PROMPT_FILE = os.path.join(
    PROMPT_DIR,
    "pookalam_prompt.txt"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value, default="Any"):
    """
    Convert a value into clean text.
    """

    if value is None:
        return default

    try:
        if isinstance(value, float) and value != value:
            return default
    except Exception:
        pass

    value = str(value).strip()

    if not value:
        return default

    return value


def get_number(value, default=0.0):
    """
    Safely convert value to float.
    """

    try:

        if value is None:
            return default

        if isinstance(value, str):

            if value.strip().lower() == "any":
                return default

            value = (
                value
                .replace(",", "")
                .replace("₹", "")
                .strip()
            )

        return float(value)

    except (ValueError, TypeError):

        return default


def is_any(value):
    """
    Check whether a value represents 'Any'.
    """

    return (
        clean_text(value, "Any")
        .strip()
        .lower()
        == "any"
    )


def format_money(value):
    """
    Format money values for prompt.
    """

    value = get_number(value)

    return f"₹{value:,.2f}"


# ============================================================
# FLOWER DESCRIPTION
# ============================================================

def build_flower_description(flowers):
    """
    Build a readable flower description including
    recommended quantities.

    Example:
        Chrysanthemum (0.90 kg),
        Green Leaves (0.40 kg),
        Marigold (0.80 kg)
    """

    flower_items = []

    if not isinstance(flowers, list):
        return (
            "fresh locally available Kerala flowers"
        )

    for flower in flowers:

        if not isinstance(flower, dict):
            continue

        name = clean_text(
            flower.get("name"),
            ""
        )

        quantity = get_number(
            flower.get("quantity_kg"),
            0.0
        )

        if not name:
            continue

        if quantity > 0:

            flower_items.append(
                f"{name} ({quantity:g} kg)"
            )

        else:

            flower_items.append(
                name
            )

    if flower_items:

        return ", ".join(
            flower_items
        )

    return (
        "fresh locally available Kerala flowers"
    )


# ============================================================
# FLOWER COST SUMMARY
# ============================================================

def calculate_recommended_cost(flowers):
    """
    Calculate the recommendation-engine flower cost
    from the supplied flower JSON.

    This is used only as reference information in
    the prompt. The GenAI is allowed to add complementary
    flowers as long as the FINAL cost stays within budget.
    """

    total = 0.0

    if not isinstance(flowers, list):
        return 0.0

    for flower in flowers:

        if not isinstance(flower, dict):
            continue

        cost = get_number(
            flower.get("estimated_cost"),
            0.0
        )

        if cost > 0:
            total += cost

    return round(
        total,
        2
    )


# ============================================================
# PATTERN DESCRIPTION
# ============================================================

def get_pattern_description(pattern):
    """
    Convert pattern name into a visual description.
    """

    pattern_lower = (
        clean_text(pattern, "")
        .lower()
    )

    if "circular" in pattern_lower:

        return (
            "beautiful concentric circular layers "
            "with a detailed floral center and a "
            "clean decorative outer border"
        )

    if "lotus" in pattern_lower:

        return (
            "an elegant lotus-inspired floral pattern "
            "with layered petals and a detailed center"
        )

    if "peacock" in pattern_lower:

        return (
            "a graceful peacock-inspired floral pattern "
            "with flowing feather-like details and a "
            "decorative border"
        )

    if "butterfly" in pattern_lower:

        return (
            "a graceful butterfly-inspired floral pattern "
            "with symmetrical wings and a detailed center"
        )

    if "conch" in pattern_lower:

        return (
            "an elegant conch-inspired floral pattern "
            "with curved layers and a detailed center"
        )

    if "star" in pattern_lower:

        return (
            "a symmetrical star-shaped floral pattern "
            "with clearly defined points and layered petals"
        )

    if "temple" in pattern_lower:

        return (
            "a traditional temple-inspired floral pattern "
            "with symmetrical layers and a decorative border"
        )

    return (
        "a beautiful symmetrical floral pattern "
        "with a detailed center and decorative border"
    )


# ============================================================
# COMPLEXITY DESCRIPTION
# ============================================================

def get_complexity_description(complexity):
    """
    Convert complexity into natural language.
    """

    complexity_lower = (
        clean_text(complexity, "")
        .lower()
    )

    descriptions = {

        "easy":
            "simple and elegant",

        "medium":
            "moderately detailed",

        "hard":
            "intricate and highly detailed"
    }

    return descriptions.get(
        complexity_lower,
        "moderately detailed"
    )


# ============================================================
# MAIN PROMPT GENERATOR
# ============================================================

def generate_prompt(data):
    """
    Generate a GenAI Pookalam prompt from
    recommendation_output.json.

    Returns:
        dict containing:
            prompt
            recommendation
            customer
            flowers
            estimated_cost
            remaining_budget
            unsatisfied_requirements
    """

    if not isinstance(data, dict):

        raise ValueError(
            "Recommendation data must be a dictionary."
        )

    # ========================================================
    # READ MAIN SECTIONS
    # ========================================================

    customer = data.get(
        "customer_requirements",
        {}
    )

    recommendation = data.get(
        "recommendation",
        {}
    )

    flowers = data.get(
        "flowers",
        []
    )

    generation_requirements = data.get(
        "generation_requirements",
        {}
    )

    unmatched_requirements = data.get(
        "unmatched_requirements",
        []
    )

    if not recommendation:

        raise ValueError(
            "Recommendation data is missing."
        )

    # ========================================================
    # CUSTOMER REQUIREMENTS
    # ========================================================

    budget = get_number(
        customer.get("budget"),
        0.0
    )

    customer_occasion = clean_text(
        customer.get("occasion"),
        "Any"
    )

    customer_theme = clean_text(
        customer.get("theme"),
        "Any"
    )

    customer_style = clean_text(
        customer.get("style"),
        "Any"
    )

    customer_pattern = clean_text(
        customer.get("pattern"),
        "Any"
    )

    customer_complexity = clean_text(
        customer.get("complexity"),
        "Any"
    )

    customer_color = clean_text(
        customer.get("color"),
        "Any"
    )

    maximum_diameter = customer.get(
        "maximum_diameter_ft"
    )

    # ========================================================
    # RECOMMENDED DESIGN
    # ========================================================

    recommended_theme = clean_text(
        recommendation.get("theme"),
        "Traditional"
    )

    recommended_style = clean_text(
        recommendation.get("style"),
        "Circular"
    )

    recommended_pattern = clean_text(
        recommendation.get("pattern"),
        recommended_style
    )

    recommended_occasion = clean_text(
        recommendation.get("occasion"),
        "Onam"
    )

    recommended_complexity = clean_text(
        recommendation.get("difficulty"),
        "Medium"
    )

    recommended_color = clean_text(
        recommendation.get("primary_color"),
        ""
    )

    estimated_cost = get_number(
        recommendation.get(
            "estimated_flower_cost"
        ),
        0.0
    )

    # ========================================================
    # FALLBACK VALUES FROM GENERATION REQUIREMENTS
    # ========================================================

    if is_any(recommended_theme):

        recommended_theme = clean_text(
            generation_requirements.get(
                "recommended_theme"
            ),
            "Traditional"
        )

    if is_any(recommended_style):

        recommended_style = clean_text(
            generation_requirements.get(
                "recommended_style"
            ),
            "Circular"
        )

    if is_any(recommended_complexity):

        recommended_complexity = clean_text(
            generation_requirements.get(
                "recommended_complexity"
            ),
            "Medium"
        )

    if is_any(recommended_occasion):

        recommended_occasion = clean_text(
            generation_requirements.get(
                "recommended_occasion"
            ),
            "Onam"
        )

    # ========================================================
    # PATTERN FALLBACK
    # ========================================================

    if is_any(recommended_pattern):

        if not is_any(customer_pattern):

            recommended_pattern = (
                customer_pattern
            )

        else:

            recommended_pattern = (
                recommended_style
            )

    # ========================================================
    # FLOWERS
    # ========================================================

    flower_text = build_flower_description(
        flowers
    )

    recommended_flower_cost = (
        calculate_recommended_cost(
            flowers
        )
    )

    # Prefer recommendation result when
    # flower JSON cost is unavailable.

    if recommended_flower_cost <= 0:

        recommended_flower_cost = (
            estimated_cost
        )

    remaining_budget = max(
        budget - recommended_flower_cost,
        0
    )

    # ========================================================
    # PATTERN
    # ========================================================

    pattern_description = (
        get_pattern_description(
            recommended_pattern
        )
    )

    # ========================================================
    # COMPLEXITY
    # ========================================================

    complexity_description = (
        get_complexity_description(
            recommended_complexity
        )
    )

    # ========================================================
    # FINAL VALUES
    # ========================================================

    final_occasion = (

        recommended_occasion

        if is_any(customer_occasion)

        else customer_occasion
    )

    final_theme = (

        recommended_theme

        if is_any(customer_theme)

        else customer_theme
    )

    final_style = (

        recommended_style

        if is_any(customer_style)

        else customer_style
    )

    final_pattern = (

        recommended_pattern

        if is_any(customer_pattern)

        else customer_pattern
    )

    final_complexity = (

        recommended_complexity

        if is_any(customer_complexity)

        else customer_complexity
    )

    # ========================================================
    # UNSATISFIED REQUIREMENTS
    # ========================================================

    unsatisfied = []

    if isinstance(
        unmatched_requirements,
        list
    ):

        for requirement in unmatched_requirements:

            requirement_text = clean_text(
                requirement,
                ""
            )

            if (
                requirement_text
                and requirement_text
                not in unsatisfied
            ):

                unsatisfied.append(
                    requirement_text
                )

    # ========================================================
    # CHECK CUSTOMER REQUIREMENTS
    # ========================================================

    if (
        not is_any(customer_theme)
        and normalize_compare(
            customer_theme
        )
        != normalize_compare(
            recommended_theme
        )
    ):

        item = f"theme: {customer_theme}"

        if item not in unsatisfied:
            unsatisfied.append(item)

    if (
        not is_any(customer_style)
        and normalize_compare(
            customer_style
        )
        != normalize_compare(
            recommended_style
        )
    ):

        item = f"style: {customer_style}"

        if item not in unsatisfied:
            unsatisfied.append(item)

    if (
        not is_any(customer_complexity)
        and normalize_compare(
            customer_complexity
        )
        != normalize_compare(
            recommended_complexity
        )
    ):

        item = (
            f"complexity: "
            f"{customer_complexity}"
        )

        if item not in unsatisfied:
            unsatisfied.append(item)

    if (
        not is_any(customer_occasion)
        and normalize_compare(
            customer_occasion
        )
        != normalize_compare(
            recommended_occasion
        )
    ):

        item = (
            f"occasion: "
            f"{customer_occasion}"
        )

        if item not in unsatisfied:
            unsatisfied.append(item)

    # ========================================================
    # COLOR
    # ========================================================

    color_mismatch = False

    if not is_any(customer_color):

        if not recommended_color:

            color_mismatch = True

        else:

            if (
                normalize_compare(
                    customer_color
                )
                not in normalize_compare(
                    recommended_color
                )
            ):

                color_mismatch = True

    if color_mismatch:

        item = (
            f"color: {customer_color}"
        )

        if item not in unsatisfied:
            unsatisfied.append(item)

    # ========================================================
    # COLOR SENTENCE
    # ========================================================

    if is_any(customer_color):

        color_sentence = (
            "Use naturally harmonious Kerala "
            "floral colors that complement the "
            "recommended flowers and theme."
        )

    else:

        color_sentence = (
            f"Use {customer_color.lower()} "
            "prominently in the final color palette "
            "while keeping the overall colors "
            "natural, harmonious and visually balanced."
        )

    # ========================================================
    # CUSTOMER REQUIREMENT SENTENCE
    # ========================================================

    customer_requirement_sentence = ""

    if unsatisfied:

        requirements_text = ", ".join(
            unsatisfied
        )

        customer_requirement_sentence = (
            "Naturally incorporate the customer's "
            f"requested {requirements_text} into "
            "the final design wherever visually "
            "appropriate, without compromising the "
            "overall Pookalam composition."
        )

    # ========================================================
    # BUDGET SENTENCE
    # ========================================================

    if budget > 0:

        budget_sentence = (
            f"Keep the final total estimated flower "
            f"cost at or below the customer's "
            f"₹{budget:,.2f} budget."
        )

    else:

        budget_sentence = (
            "Use a practical amount of flowers "
            "suitable for the design."
        )

    # ========================================================
    # COMPLEMENTARY FLOWER RULE
    # ========================================================

    complementary_flower_sentence = (

        "The recommended flowers must remain the "
        "primary flowers of the design. Additional "
        "complementary Kerala flowers may be used "
        "only when they genuinely improve the visual "
        "composition, color harmony, layering or "
        "central motif. Any additional flowers must "
        "remain appropriate for a traditional Kerala "
        "Onam Pookalam and the total estimated flower "
        "cost must remain within the customer's budget."
    )

    # ========================================================
    # SIZE
    # ========================================================

    size_sentence = ""

    if (
        maximum_diameter is not None
        and not is_any(maximum_diameter)
        and str(maximum_diameter).strip() != ""
    ):

        diameter_value = get_number(
            maximum_diameter,
            0.0
        )

        if diameter_value > 0:

            size_sentence = (
                f"Keep the complete Pookalam "
                f"within {diameter_value:g} feet "
                "in diameter."
            )

    # ========================================================
    # FLOWER BREAKDOWN INSTRUCTION
    # ========================================================

    flower_breakdown_instruction = (

        "After creating the visual Pookalam design, "
        "provide a clear flower quantity and cost "
        "summary for the final Pookalam. Include "
        "every flower actually used, including the "
        "recommended flowers and any additional "
        "complementary flowers. For each flower, "
        "provide the flower name, estimated quantity, "
        "price per kg, and estimated cost. Then provide "
        "the total estimated flower cost and remaining "
        "budget. Ensure that the final estimated flower "
        "cost does not exceed the customer's specified "
        "budget."
    )

    # ========================================================
    # VISUAL QUALITY INSTRUCTIONS
    # ========================================================

    visual_instruction = (

        "Show the entire Pookalam from a "
        "photorealistic top-down view with "
        "fresh natural flowers, realistic "
        "petal textures, natural lighting, "
        "clean floral placement, harmonious "
        "Kerala colors and a visually balanced "
        "composition."
    )

    # ========================================================
    # NEGATIVE INSTRUCTIONS
    # ========================================================

    negative_instruction = (

        "Do not include people, hands, text, "
        "letters, numbers, logos, watermarks, "
        "artificial flowers, flower shops, "
        "flower baskets or unrelated objects."
    )

    # ========================================================
    # FINAL PROMPT
    # ========================================================

    prompt_parts = [

        (
            "Create a realistic Kerala Onam "
            f"Pookalam for a {final_occasion.lower()} "
            f"setting, inspired by the traditional "
            f"{final_theme} theme and using a "
            f"{final_pattern} design as the primary basis."
        ),

        (
            f"Arrange the Pookalam in "
            f"{pattern_description}."
        ),

        (
            f"Use {flower_text} as the primary "
            "recommended flowers."
        ),

        complementary_flower_sentence,

        color_sentence,

        (
            f"Make the design "
            f"{complexity_description} with a strong "
            f"{final_theme} central motif, carefully "
            "arranged floral layers and a clean "
            "decorative outer border."
        ),

        budget_sentence,

    ]

    if size_sentence:

        prompt_parts.append(
            size_sentence
        )

    if customer_requirement_sentence:

        prompt_parts.append(
            customer_requirement_sentence
        )

    prompt_parts.extend([

        visual_instruction,

        flower_breakdown_instruction,

        negative_instruction

    ])

    # ========================================================
    # CLEAN FINAL PROMPT
    # ========================================================

    prompt = " ".join(
        part.strip()
        for part in prompt_parts
        if part and part.strip()
    )

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "prompt":
            prompt,

        "recommendation":
            recommendation,

        "customer":
            customer,

        "flowers":
            flowers,

        "estimated_cost":
            recommended_flower_cost,

        "remaining_budget":
            remaining_budget,

        "unsatisfied_requirements":
            unsatisfied
    }


# ============================================================
# NORMALIZE COMPARISON
# ============================================================

def normalize_compare(value):
    """
    Normalize text for requirement comparison.
    """

    return (
        clean_text(
            value,
            ""
        )
        .lower()
        .strip()
    )


# ============================================================
# GENERATE PROMPT FROM JSON FILE
# ============================================================

def generate_prompt_from_file(
    recommendation_file=RECOMMENDATION_FILE
):
    """
    Generate the GenAI prompt from
    recommendation_output.json.
    """

    if not os.path.isfile(
        recommendation_file
    ):

        raise FileNotFoundError(
            "recommendation_output.json not found."
        )

    # --------------------------------------------------------
    # READ JSON
    # --------------------------------------------------------

    with open(
        recommendation_file,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    # --------------------------------------------------------
    # GENERATE PROMPT
    # --------------------------------------------------------

    result = generate_prompt(
        data
    )

    # --------------------------------------------------------
    # CREATE PROMPT DIRECTORY
    # --------------------------------------------------------

    os.makedirs(
        PROMPT_DIR,
        exist_ok=True
    )

    # --------------------------------------------------------
    # SAVE PROMPT
    # --------------------------------------------------------

    with open(
        PROMPT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            result["prompt"]
        )

    return result


# ============================================================
# TERMINAL SUPPORT
# ============================================================

if __name__ == "__main__":

    try:

        result = (
            generate_prompt_from_file()
        )

        print()
        print("=" * 75)
        print("GENERATED GENAI POOKALAM PROMPT")
        print("=" * 75)
        print()
        print(
            result["prompt"]
        )
        print()
        print(
            "Prompt saved to:"
        )
        print(
            PROMPT_FILE
        )
        print()
        print("=" * 75)

    except Exception as error:

        print()
        print(
            "ERROR:",
            error
        )