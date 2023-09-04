import pandas as pd
import numpy as np
import streamlit as st
import random


# read the database csv into multiple dataf
quantity_pricing = pd.read_excel(
    "./עותק של VENDOR PRINT PRICING .xlsx", sheet_name="order_units"
)
production_pricing = pd.read_excel(
    "./עותק של VENDOR PRINT PRICING .xlsx", sheet_name="Production_Costs"
)
st.set_page_config(layout="wide")
main_column, caculation = st.columns([3, 1])

with main_column:
    # Select Box for the three companies
    st.subheader("Select the Company That you want to order from")
    select_company = st.selectbox(
        "**:red[Which Company you like to order from]**",
        ("HAPPY FACTORY", "MERCH PRODUCTION", "Empire Graphics"),
    )
    st.markdown("---")
    quantity_pricing["vendor"] = quantity_pricing["vendor"].str.rstrip()
    quantity_pricing = quantity_pricing[quantity_pricing["vendor"] == select_company]

    # create an number input box for the quantity
    st.subheader("Quantity")
    quantity = st.number_input("**:red[# Units To Order]**", step=1)
    st.markdown("---")

    quantity_pricing = quantity_pricing[
        quantity_pricing["max_num_units"] >= quantity
    ].sort_values(by="max_num_units")
    max_num_units = quantity_pricing["max_num_units"].min()
    quantity_pricing = quantity_pricing[
        quantity_pricing["max_num_units"] == max_num_units
    ]

    # create an section for the blanks price per unit
    st.subheader(":shirt: Blanks")
    # creating 4 columns one for each parameter
    (
        blanks_column1,
        blanks_column2,
        blanks_column3,
        blanks_column4,
        blanks_column5,
        blanks_column6,
    ) = st.columns([1, 1, 0.5, 1.3, 0.6, 0.7])
    # a select box to choose the provider of the blanks
    with blanks_column1:
        blanks_provider = st.selectbox("**:red[Source]**", ["Taste of Ink", "Client"])
    # an input box with the base cost per blank -- default 2.62
    with blanks_column2:
        base_cost = st.number_input("**:red[Base Cost Per Blank]**", value=2.62)

    # a column dvided into 2 columns containg the % or $ select box and the mark up amount

    with blanks_column3:
        select_box_blanks_precent_or_dollar = st.selectbox("", ("$", "%"))
    with blanks_column4:
        blank_markup = st.number_input("**:red[Markup Amount]**")

    # a select box stating is the blank dyed or not
    with blanks_column5:
        dyed = st.selectbox("**:red[Dyed?]**", ["Yes", "No"])
    with blanks_column6:
        if dyed == "Yes":
            dyed_price = st.number_input("", value=4.5)
        else:
            dyed_price = 0

    result_dollar = base_cost + blank_markup + dyed_price
    result_precent = base_cost + (base_cost * blank_markup) / 100 + dyed_price
    price_per_blank = np.where(
        select_box_blanks_precent_or_dollar == "$", result_dollar, result_precent
    )
    st.caption("Section Total: $" + str(price_per_blank) + " / unit")
    st.markdown("---")

    #################################
    #################################
    ################################# new section
    # create the print locations section
    st.subheader(":lower_left_paintbrush: Print Locations")
    color_col, oversized_col, speciality_col, remove_col = st.columns(4)

    if "input_keys" not in st.session_state:
        st.session_state.input_keys = []

    if st.button("Add new row"):
        new_row_key = random.randint(0, 999999)
        st.session_state.input_keys.append(new_row_key)

    input_values_colors = []
    input_values_oversized = []
    input_values_ink = []
    price_list = []

    rows_to_remove = []

    for input_key in st.session_state.input_keys:
        (
            color_col,
            oversized_col,
            speciality_col,
            speciality_input_col,
            remove_col,
        ) = st.columns(5)
        with remove_col:
            st.subheader("")

            delete_button_key = f"delete_button_{input_key}"
            delete_button_clicked = st.button(
                f"X", key=delete_button_key, type="primary"
            )

        if delete_button_clicked:
            st.session_state.input_keys.remove(input_key)

        else:
            with color_col:
                num_colors = st.selectbox(
                    "**:red[Colors]**", list(range(0, 13)), key=input_key
                )
            with oversized_col:
                st.write("")
                st.write("")
                oversized_key = f"oversized_{input_key}"
                oversized_input = st.checkbox("**:red[Oversized?]**", key=oversized_key)
            with speciality_col:
                st.write("")
                st.write("")
                ink_key = f"specialty_ink_{input_key}"
                ink_input = st.checkbox("**:red[Specialty Ink?]**", key=ink_key)
            with speciality_input_col:
                if ink_input:
                    speciality_input_key = f"speciality_input_{input_key}"
                    speciality_input = st.number_input(
                        "ink speicaliy",
                        label_visibility="hidden",
                        key=speciality_input_key,
                    )
                else:
                    speciality_input = 0

            input_values_colors.append(num_colors)
            input_values_oversized.append(oversized_input)
            input_values_ink.append(ink_input)

            quantity_pricing_filterd = (
                quantity_pricing[quantity_pricing["max_num_colours"] >= num_colors]
                .sort_values(by="price")
                .head(1)
            )

            final_color_price = (
                quantity_pricing_filterd["price"].iloc[0] + speciality_input
            )
            price_key = f"color_price_{input_key}"
            price_list.append(final_color_price)
            # price_1 = st.write("Price:", final_color_price, key=price_key)

    st.caption("Section Total: $" + str(round(np.sum(price_list), 2)) + " / unit:")
    st.markdown("---")
    #######################################################
    #######################################################
    st.subheader(":hammer_and_wrench: Options")
    option_price_list = []
    production_pricing["vendor"] = production_pricing["vendor"].str.rstrip()
    production_pricing_by_company = production_pricing[
        production_pricing["vendor"] == select_company
    ]
    production_pricing_by_company["price"] = production_pricing_by_company[
        "price"
    ].replace("QUOTE", 0)
    production_pricing_by_company_filtered = production_pricing_by_company[
        production_pricing_by_company["category"] == "Cost_Per_Unit_Per_Design"
    ]
    options_list = production_pricing_by_company_filtered["type"].drop_duplicates()
    production_pricing_by_company_indexed = (
        production_pricing_by_company_filtered.set_index("type")
    )
    for option in options_list:
        title_col, radio_button_col, price_input_col, place_holder = st.columns(
            [2, 2, 3, 2]
        )
        with title_col:
            st.markdown("")
            html_str = f"""
                <style>
                p.a {{
                color: red ;
                font-size: 14px;
                font-weight: bold;
                vertical-align: middle;
                margin-top:10px;
                }}
                </style>
                <p class="a">{option}</p>
                """
            st.markdown(html_str, unsafe_allow_html=True)
        with radio_button_col:
            radio_option = st.radio(
                "radio_" + option,
                ["No", "Yes"],
                label_visibility="hidden",
                horizontal=True,
            )
        with price_input_col:
            if radio_option == "Yes":
                option_price = production_pricing_by_company_indexed["price"].loc[
                    option
                ]
                option_price_input = st.number_input(
                    "Price", value=option_price, key=option
                )
            else:
                option_price_input = 0
        if option_price_list != 0:
            option_price_list.append(option_price_input)

    st.caption(
        "Section Total: $" + str(round(np.sum(option_price_list), 2)) + " / unit:"
    )
    st.markdown("---")

    #################################################
    #################################################
    st.subheader(":boat: Setup Fee")
    setup_fee_price_list = []

    production_pricing_by_company_filtered = production_pricing_by_company[
        production_pricing_by_company["category"] == "Cost_Per_Design"
    ]
    setup_fee_list = production_pricing_by_company_filtered["type"].drop_duplicates()
    production_pricing_by_company_indexed = (
        production_pricing_by_company_filtered.set_index("type")
    )
    for setup_fee in setup_fee_list:
        title_col, radio_button_col, price_input_col, place_holder = st.columns(
            [2, 2, 3, 2]
        )
        with title_col:
            st.markdown("")
            html_str = f"""
                <style>
                p.a {{
                color: red ;
                font-size: 14px;
                font-weight: bold;
                vertical-align: middle;
                margin-top:10px;
                }}
                </style>
                <p class="a">{setup_fee}</p>
                """
            st.markdown(html_str, unsafe_allow_html=True)
        with radio_button_col:
            radio_option = st.radio(
                "radio_" + setup_fee,
                ["No", "Yes"],
                label_visibility="hidden",
                horizontal=True,
            )
        with price_input_col:
            if radio_option == "Yes":
                setup_fee_price = production_pricing_by_company_indexed["price"].loc[
                    setup_fee
                ]
                setup_fee_price_input = st.number_input(
                    "Price", value=setup_fee_price, key=setup_fee
                )
            else:
                setup_fee_price_input = 0
            if setup_fee_price_input != 0:
                setup_fee_price_list.append(setup_fee_price_input)

    st.caption(
        "Section Total: $"
        + str(round(np.sum(setup_fee_price_list), 2) * np.sum(input_values_colors))
    )
    st.markdown("---")

    ##############################################
    st.subheader(":diamond_shape_with_a_dot_inside: Miscellaneous")
    numbers, others_name, others_amount, place_holder = st.columns([0.5, 3, 3, 5])
    with numbers:
        st.subheader("")
        st.subheader("1. ")
        st.subheader("")
        st.subheader("2. ")
    with others_name:
        other_input1 = st.text_input("**:red[Name]**", placeholder="La Première")
        other_input2 = st.text_input(
            "other_input2", label_visibility="hidden", placeholder="La deuxième"
        )
    with others_amount:
        other_price_input1 = st.number_input("**:red[Amount Per Unit]**", value=0.00)
        other_price_input2 = st.number_input(
            "other_price_input2", label_visibility="hidden", value=0.00
        )
    st.caption("Section Total: $" + str(other_price_input1 + other_price_input2))
    st.markdown("---")
    #############################################
    #############################################
    st.subheader(":page_with_curl: Note")
    st.text_area(
        "a",
        placeholder="Simplicity is the ultimate sophistication.",
        label_visibility="hidden",
    )
# ------------------------- side bar for totals: --------------------------
with caculation:
    st.subheader(":clipboard: Totals:")
    st.write("**:red[Cost Per Unit]**")
    left_calculator, right_calculator = st.columns([3, 1.5])
    with left_calculator:
        st.write("All in Cost:")
        st.write("Without Setup Fees:")
    with right_calculator:
        price_per_blank = float(price_per_blank)
        try:
            st.write(
                "$"
                + "{:,}".format(
                    round(
                        (
                            (
                                price_per_blank
                                + float(np.sum(price_list))
                                + float(np.sum(option_price_list))
                                + float(other_price_input1)
                                + float(other_price_input2)
                            )
                            + (
                                float(np.sum(setup_fee_price_list))
                                * float(np.sum(input_values_colors))
                                / quantity
                            )
                        ),
                        2,
                    )
                )
            )
            st.write(
                "$"
                + "{:,}".format(
                    round(
                        (
                            price_per_blank
                            + np.sum(price_list)
                            + np.sum(option_price_list)
                            + other_price_input1
                            + other_price_input2
                        ),
                        2,
                    )
                )
            )
        except:
            st.write("")
    st.divider()
    st.write("**:red[Total Setup Fees]**")
    total_left_col, total_right_col = st.columns([3, 1.5])
    with total_left_col:
        st.write("Total:")
    with total_right_col:
        st.write(
            "$",
            str(round(np.sum(setup_fee_price_list), 2) * np.sum(input_values_colors)),
        )
    st.divider()
    st.write("**:red[Subtotal]**")
    subtotal_left_col, subtotal_right_col = st.columns([3, 1.5])
    with subtotal_left_col:
        st.write("Job Total:")
    with subtotal_right_col:
        st.write(
            "$"
            + "{:,}".format(
                round(
                    (
                        (
                            price_per_blank
                            + float(np.sum(price_list))
                            + float(np.sum(option_price_list))
                            + float(other_price_input1)
                            + float(other_price_input2)
                        )
                        * quantity
                        + (
                            float(np.sum(setup_fee_price_list))
                            * float(np.sum(input_values_colors))
                        )
                    ),
                    2,
                )
            )
        )


# price_per_blank

# str(round(np.sum(price_list), 2))
# str(round(np.sum(option_price_list), 2))
# str(round(np.sum(setup_fee_list), 2) * np.sum(input_values_colors))
# str(other_price_input1 + other_price_input2)
