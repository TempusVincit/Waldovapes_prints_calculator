import pandas as pd
import numpy as np
import streamlit as st
import random
from PIL import Image


def write_in_usd(number):
    st.write(
        "$"
        + "{:,}".format(
            round(
                number,
                2,
            )
        )
    )


small_logo = Image.open("./Absolute_merch_small.png")


# read the database csv into multiple dataframe
quantity_pricing = pd.read_excel(
    "./VENDOR PRINT PRICING.xlsx", sheet_name="order_units"
)
production_pricing = pd.read_excel(
    "./VENDOR PRINT PRICING.xlsx", sheet_name="Production_Costs"
)
st.set_page_config(layout="wide", page_icon=small_logo)


main_column, caculation = st.columns([3, 1])

# create the prices quates df
pdf_df = pd.DataFrame(columns=["title", "price", "quantity", "string"])

with main_column:
    # Select Box for the three companies
    st.subheader(":label: Select the Company That you want to order from")
    select_company = st.selectbox(
        "**:red[Which Company you like to order from]**",
        ("HAPPY FACTORY", "MERCH PRODUCTION", "Empire Graphics"),
    )
    pdf_df = pdf_df._append(
        {"title": "Company", "string": select_company}, ignore_index="True"
    )

    st.markdown("---")
    quantity_pricing["vendor"] = quantity_pricing["vendor"].str.rstrip()
    quantity_pricing = quantity_pricing[quantity_pricing["vendor"] == select_company]

    # create an number input box for the quantity
    st.subheader(":thermometer: Quantity")
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
        blanks_provider = st.text_input("**:red[Blank]**", placeholder="Supplier Name")
    # an input box with the base cost per blank -- default 2.62
    with blanks_column2:
        base_cost = st.number_input("**:red[Base Cost Per Blank]**", value=0.0)

    # a column dvided into 2 columns containg the % or $ select box and the mark up amount

    with blanks_column3:
        select_box_blanks_precent_or_dollar = st.selectbox("", ("$", "%"))
    with blanks_column4:
        blank_markup = st.number_input("**:red[Markup Amount]**")

    # a select box stating is the blank dyed or not
    with blanks_column5:
        dyed = st.selectbox(
            "**:red[Dyed?]**",
            ["No", "Yes"],
        )
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
    blank_string = (
        "Source:"
        + blanks_provider
        + ", Base Cost Per Blank:"
        + str(base_cost)
        + ", Markup Amount:"
        + select_box_blanks_precent_or_dollar
        + str(blank_markup)
        + ", Dyed:"
        + dyed
        + ", Dyed Price: "
        + str(dyed_price)
    )
    pdf_df = pdf_df._append(
        {
            "title": "Blanks",
            "quantity": quantity,
            "string": blank_string,
            "price": price_per_blank,
        },
        ignore_index="True",
    )

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
            location_name_col,
            color_col,
            oversized_col,
            speciality_col,
            m_Ink,
            Foil,
            remove_col,
        ) = st.columns([1.5, 1, 1, 1, 1, 1, 0.5])
        with remove_col:
            st.subheader("")

            delete_button_key = f"delete_button_{input_key}"
            delete_button_clicked = st.button(
                f"X", key=delete_button_key, type="primary"
            )

        if delete_button_clicked:
            st.session_state.input_keys.remove(input_key)

        else:
            with location_name_col:
                location_name = st.text_input(
                    "**:red[Name]**", placeholder="Location", key=f"name_{input_key}"
                )

            with color_col:
                if select_company == "HAPPY FACTORY":
                    num_colors = st.selectbox(
                        "**:red[Colors]**", list(range(0, 13)), key=input_key
                    )
                else:
                    num_colors = st.selectbox(
                        "**:red[Colors]**", list(range(0, 18)), key=input_key
                    )
            with oversized_col:
                st.write("")
                oversized_key = f"oversized_{input_key}"
                oversized_input = st.checkbox("**:red[Oversized]**", key=oversized_key)
                Over_Seam_Printing__key = f"Over_Seam_Printing_{input_key}"
                Over_Seam_Printing__input = st.checkbox(
                    "**:red[Over Seam Printing]**",
                    key=Over_Seam_Printing__key,
                )
            with speciality_col:
                st.write("")
                ink_key = f"specialty_ink_{input_key}"
                ink_input = st.checkbox("**:red[Specialty Ink]**", key=ink_key)
                Sewn_Patches_key = f"Sewn_Patches{input_key}"
                Sewn_Patches_input = st.checkbox(
                    "**:red[Sewn Patches]**",
                    key=Sewn_Patches_key,
                )
            with m_Ink:
                st.write("")
                mink_key = f"m_Ink_{input_key}"
                mink_input = st.checkbox("**:red[3M Ink]**", key=mink_key)
                Poly_Nylon_Inks_key = f"Poly_Nylon_Inks{input_key}"
                Poly_Nylon_Inks_input = st.checkbox(
                    "**:red[Poly/Nylon Inks]**",
                    key=Poly_Nylon_Inks_key,
                )
            with Foil:
                st.write("")
                foil_key = f"foil_{input_key}"
                foil_input = st.checkbox("**:red[Foil]**", key=foil_key)
                Fleece_key = f"Fleece Printing{input_key}"
                Fleece_input = st.checkbox(
                    "**:red[Fleece Printing]**",
                    key=Fleece_key,
                )

            input_values_colors.append(num_colors)

            quantity_pricing_filterd = (
                quantity_pricing[quantity_pricing["max_num_colours"] >= num_colors]
                .sort_values(by="price")
                .head(1)
            )

            final_color_price = quantity_pricing_filterd["price"].iloc[0]
            price_key = f"color_price_{input_key}"
            price_list.append(final_color_price)
            # price_1 = st.write("Price:", final_color_price, key=price_key)
            location_string = (
                "Name : " + location_name + "\n Colors : " + str(num_colors)
            )

            if ink_input:
                location_string = location_string + "\n Speciality Ink"
            if foil_input:
                location_string = location_string + "\n Foil"
            if Sewn_Patches_input:
                location_string = location_string + "\n Sewn Patches"
            if oversized_input:
                location_string = location_string + "\n Oversized"
            if Poly_Nylon_Inks_input:
                location_string = location_string + "\n Poly Nylon Inks"
            if Over_Seam_Printing__input:
                location_string = location_string + "\n Over Seam Printing"
            if mink_input:
                location_string = location_string + "\n 3M Ink"
            if Fleece_input:
                location_string = location_string + "\n Fleece Printing"

            pdf_df = pdf_df._append(
                {
                    "title": "Location",
                    "quantity": quantity,
                    "string": location_string,
                    "price": final_color_price,
                },
                ignore_index="True",
            )

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
        (
            title_col,
            radio_button_col,
            price_input_col,
            option_quantity,
            place_holder,
        ) = st.columns([2, 2, 2, 2, 1.5])

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
        with option_quantity:
            if radio_option == "Yes":
                option_quantity = st.number_input(
                    label="**Quantity**",
                    value=quantity,
                    key=option + "_quantity",
                    step=1,
                )
            else:
                option_quantity = 0
        with price_input_col:
            if radio_option == "Yes":
                option_price = production_pricing_by_company_indexed["price"].loc[
                    option
                ]
                option_price_input = st.number_input(
                    "**Price**", value=option_price, key=option
                )
                pdf_df = pdf_df._append(
                    {
                        "title": "Option",
                        "quantity": option_quantity,
                        "string": option,
                        "price": option_price_input,
                    },
                    ignore_index="True",
                )
            else:
                option_price_input = 0
        if option_price_list != 0:
            option_price_list.append(option_price_input)

    # st.caption(
    #     "Section Total: $" + str(round(np.sum(option_price_list), 2)) + " / unit:"
    # )
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
        (
            title_col,
            radio_button_col,
            price_input_col,
            setup_fee_quantity,
            place_holder,
        ) = st.columns([2, 2, 2, 2, 1.5])
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
        with setup_fee_quantity:
            if radio_option == "Yes":
                setup_fee_quantity = st.number_input(
                    label="**Quantity**", key=setup_fee + "_quantity", step=1
                )
            else:
                option_quantity = 0
        with price_input_col:
            if radio_option == "Yes":
                setup_fee_price = production_pricing_by_company_indexed["price"].loc[
                    setup_fee
                ]
                setup_fee_price_input = st.number_input(
                    "**Price**", value=setup_fee_price, key=setup_fee
                )
                pdf_df = pdf_df._append(
                    {
                        "title": "Setup Fee",
                        "quantity": setup_fee_quantity,
                        "string": setup_fee,
                        "price": setup_fee_price_input,
                    },
                    ignore_index="True",
                )
            else:
                setup_fee_price_input = 0
            if setup_fee_price_input != 0:
                setup_fee_price_list.append(setup_fee_price_input)

    # calculating the sum of the setup fees
    setup_fee_sum = np.sum(
        pdf_df["price"][pdf_df["title"] == "Setup Fee"]
        * pdf_df["quantity"][pdf_df["title"] == "Setup Fee"]
    )

    st.caption("Section Total: $" + str(round(setup_fee_sum, 2)))
    st.markdown("---")

    # ------------------------- create the misslenios per unit section--------------------------
    st.subheader(":diamond_shape_with_a_dot_inside: Miscellaneous Per Unit")
    numbers, others_name, others_amount, quantity_misc_col, remove_col = st.columns(
        [0.5, 3, 3, 3, 2]
    )

    if "Miscellaneous_per_unit" not in st.session_state:
        st.session_state.Miscellaneous_per_unit = []

    if st.button("Add New Row"):
        new_row_key = random.randint(0, 999999)
        st.session_state.Miscellaneous_per_unit.append(new_row_key)

    Miscellaneous_per_unit_numbers = []
    Miscellaneous_per_unit_name = []
    Miscellaneous_per_unit_amount = []

    Miscellaneous_per_unit_rows_to_remove = []

    for Miscellaneous in st.session_state.Miscellaneous_per_unit:
        numbers, others_name, others_amount, quantity_misc_col, remove_col = st.columns(
            [0.5, 3, 3, 3, 2]
        )
        with remove_col:
            st.subheader("")
            delete_button_key = f"delete_button_{Miscellaneous}"
            delete_button_clicked = st.button(
                f"X", key=delete_button_key, type="primary"
            )
        if delete_button_clicked:
            st.session_state.Miscellaneous_per_unit.remove(Miscellaneous)

        else:
            with others_name:
                name = st.text_input(
                    "**:red[Name]**",
                    placeholder="Miscellaneous Name",
                    key=Miscellaneous,
                )
            with numbers:
                st.subheader("")
                st.subheader(
                    str(
                        st.session_state.Miscellaneous_per_unit.index(Miscellaneous) + 1
                    )
                    + "."
                )
            with others_amount:
                amount_key = f"specialty_ink_{Miscellaneous}"
                amount_input = st.number_input(
                    "**:red[Amount Per Unit]**",
                    key=amount_key,
                )
            with quantity_misc_col:
                quantity_misc_key = f"quantiy_misc{Miscellaneous}"
                quantity_misc_input = st.number_input(
                    "**:red[Quantity]**", key=quantity_misc_key, step=1
                )
            pdf_df = pdf_df._append(
                {
                    "title": "Miscellaneous per unit",
                    "quantity": quantity_misc_input,
                    "string": name,
                    "price": amount_input,
                },
                ignore_index="True",
            )
            Miscellaneous_per_unit_amount.append(amount_input)

    st.caption(
        "Section Total: $"
        + str(round(np.sum(Miscellaneous_per_unit_amount), 2))
        + " / unit:"
    )
    Miscellaneouses_per_unit_total = round(np.sum(Miscellaneous_per_unit_amount), 2)

    st.markdown("---")
    # ------------------------- create the misslenios per unit section--------------------------
    st.subheader(":sparkles: Miscellaneous ")
    numbers, others_name, others_amount, remove_col = st.columns([0.5, 3, 3, 5])

    if "Miscellaneouses" not in st.session_state:
        st.session_state.Miscellaneouses = []

    if st.button("Add New row"):
        new_row_key = random.randint(0, 999999)
        st.session_state.Miscellaneouses.append(new_row_key)

    Miscellaneouses_numbers = []
    Miscellaneouses_name = []
    Miscellaneouses_amount = []

    Miscellaneouses_rows_to_remove = []

    for Miscellaneous in st.session_state.Miscellaneouses:
        (
            numbers,
            others_name,
            others_amount,
            quantity_misc_section_col,
            remove_col,
        ) = st.columns([0.5, 3, 3, 3, 2])
        with remove_col:
            st.subheader("")
            delete_button_key = f"delete_button_{Miscellaneous}"
            delete_button_clicked = st.button(
                f"X", key=delete_button_key, type="primary"
            )
        if delete_button_clicked:
            st.session_state.Miscellaneouses.remove(Miscellaneous)

        else:
            with others_name:
                name = st.text_input(
                    "**:red[Name]**",
                    placeholder="Miscellaneous Name",
                    key=Miscellaneous,
                )
            with numbers:
                st.subheader("")
                st.subheader(
                    str(st.session_state.Miscellaneouses.index(Miscellaneous) + 1) + "."
                )
            with others_amount:
                amount_key = f"specialty_ink_{Miscellaneous}"
                amount_input = st.number_input(
                    "**:red[Amount]**",
                    key=amount_key,
                )
            with quantity_misc_section_col:
                quantity_misc_section_key = f"quantity_misc_section_misc{Miscellaneous}"
                quantity_misc_section_input = st.number_input(
                    "**:red[Quantity]**", key=quantity_misc_section_key, step=1
                )
            pdf_df = pdf_df._append(
                {
                    "title": "Miscellaneous",
                    "quantity": quantity_misc_section_input,
                    "string": name,
                    "price": amount_input,
                },
                ignore_index="True",
            )
            Miscellaneouses_amount.append(amount_input)

    st.caption(
        "Section Total: $" + str(round(np.sum(Miscellaneouses_amount), 2)) + " :"
    )
    Miscellaneouses_amount_total = round(np.sum(Miscellaneouses_amount), 2)

    st.markdown("---")
    #############################################
    #############################################
    st.subheader(":page_with_curl: Note")
    notes = st.text_area(
        "a",
        placeholder="Simplicity is the ultimate sophistication.",
        label_visibility="hidden",
    )


# Convert the DataFrame to an HTML table
pdf_df["string"] = pdf_df["string"].str.replace(
    ",", "<br>"
)  # Convert commas to HTML line breaks
pdf_df["string"] = pdf_df["string"].str.replace("\n", "<br>")
pdf_df = pdf_df[["title", "string", "quantity", "price"]]
pdf_df = pdf_df.fillna(0)
pdf_df["Amount"] = pdf_df["quantity"] * pdf_df["price"]
sum_amount = "$" + str(np.sum(pdf_df["Amount"]))

# ------------------------- side bar for totals: --------------------------
with caculation:
    st.subheader(":clipboard: Totals:")
    st.write("**:red[True Cost Per Unit]**")
    left_calculator, right_calculator = st.columns([3, 1.5])
    with left_calculator:
        st.write("All in Cost:")
        st.write("Printing Subtotal:")
        st.write("Setup Subtotal:")

    with right_calculator:
        price_per_blank = float(price_per_blank)
        total_price_per_unit = np.sum(
            pdf_df["Amount"][
                pdf_df["title"].isin(
                    ["Blanks", "Location", "Option", "Miscellaneous per unit"]
                )
            ]
        )
        total_setup_fee = np.sum(
            pdf_df["Amount"][pdf_df["title"].isin(["Setup Fee", "Miscellaneous"])]
        )
        try:
            all_in_cost = np.sum(pdf_df["Amount"]) / quantity
            st.write(
                "$"
                + "{:,}".format(
                    round(
                        all_in_cost,
                        2,
                    )
                )
            )
            write_in_usd(total_price_per_unit / quantity)
            write_in_usd(total_setup_fee / quantity)

        except:
            st.write("")
    st.divider()

    st.write("**:red[Subtotal]**")
    subtotal_left_col, subtotal_right_col = st.columns([3, 1.5])
    with subtotal_left_col:
        st.write("Job Total:")
        st.write("Printing Total:")
        st.write("Setup Total:")

    with subtotal_right_col:
        job_total = np.sum(pdf_df["Amount"])
        st.write(
            "$"
            + "{:,}".format(
                round(
                    job_total,
                    2,
                )
            )
        )
        write_in_usd(total_price_per_unit)
        write_in_usd(total_setup_fee)
    ################## pricing recomendation ########################
    st.markdown("---")
    st.write(":clipboard: **:red[Pricing recommendations:]**")
    recommendation_precentage = st.slider(
        "pricing recommendations", step=1, label_visibility="hidden", format="%d%%"
    )
    st.write("**:red[Suggested Cost Per Unit w/ Margin]**")
    left_calculator, right_calculator = st.columns([3, 1.5])
    with left_calculator:
        st.write("All in Cost:")
        st.write("Printing Subtotal:")
        st.write("Setup Subtotal:")

    with right_calculator:
        try:
            st.write(
                "$"
                + "{:,}".format(
                    round(
                        all_in_cost * (1 + recommendation_precentage / 100),
                        2,
                    )
                )
            )
            write_in_usd(
                (total_price_per_unit / quantity)
                * (1 + recommendation_precentage / 100)
            )
            write_in_usd(
                (total_setup_fee / quantity) * (1 + recommendation_precentage / 100)
            )

        except:
            st.write("")

    st.divider()
    st.write("**:red[Subtotal]**")
    subtotal_left_col, subtotal_right_col = st.columns([3, 1.5])
    with subtotal_left_col:
        st.write("Job Total:")
        st.write("Printing Total:")
        st.write("Setup Total:")
    with subtotal_right_col:
        st.write(
            "$"
            + "{:,}".format(
                round(
                    job_total * (1 + recommendation_precentage / 100),
                    2,
                )
            )
        )
        write_in_usd((total_price_per_unit) * (1 + recommendation_precentage / 100))
        write_in_usd((total_setup_fee) * (1 + recommendation_precentage / 100))
# st.dataframe(pdf_df)
hide_streamlit_style = """
<style>
.row-widget.stCheckbox span{
    font-size:12px;
}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def dataframe_to_html(df):
    # Convert DataFrame to HTML
    html_table = df.to_html(classes="table", escape=False, index=False)

    # Add inline CSS for styling
    html_content = f"""
    <html>
    <head>
    <img src="https://uc93e802551020c403cfb8095cba.previews.dropboxusercontent.com/p/thumb/ACCP3HbvWCdcIs6X-1ieEwl4FL0SXKhMqULwmlFZq1YdFGB1MweV1zt-W-YPw2Qt50VulraOBjFwoBWAmqJip0CncxjOy_w4vT-Em4_AqKpyhK7dUQToVZ_G9givmG75zk4tYm2rDc9RNqUeqM1sUe0l7HkFkssHb4c2gXcVR30j_EGhBog1-i3n5PxTmr2WtcmxVlPPJDiCOZGt16iGOlrjoiLkqeRUwAnL0lpbyUZmowNB-a6OCRbvTzYzOoQnrzJRnhQg74AcRmBAZeDaxgUKAMh6OZLWnoEPuZeyT14CGKoWuUUw9q2oxl7N_j3bi1Q7Ph9PiID_NXXBMEqiHneFjUXMAIZs9oOghJhluQggr_00ZtCKHAttNgZ0aEYLT3s/p.png" >
    <div><p style="display:inline-block; font-family: Arial, Helvetica, sans-serif; margin-left:50px;"> 
                
            </p> </div> <hr>
        <style>
            body {{
            width: 21cm;
            height: 29.7cm;
            margin: 30mm 45mm 10mm 45mm;
            font-family: Arial, Helvetica, sans-serif;
             }}
            img {{
            width: 19cm;
            margin-top: -40px;
            margin-bottom: -40px;


 }}
            .table {{
                border-collapse: collapse;
                width: 800px;
                text-align: left;
                font-size : 14px;
            }}
            .table, .table th, .table td {{
                border: 0px solid black;
                text-align: left;
            }}
            .table th, .table td {{
            padding-top: 6px;
            padding-bottom: 6px;                
            }}

            .table th{{font-weight: 600;
            background-color: #f3f3f3;
            }}

            .table td:first-child {{
                font-weight: bold;
            }}
            .table td {{
                text-align: left;
            }}
            hr.dashed{{
                border-top: 1px dashed;
                border-bottom: none;
                }}
        </style>
    </head>
    <body>
        {html_table}
        <hr class="dashed">
         <div style="text-align: right; margin-right: 180px; margin-bottom: -20px;">Total:</div>
        <div style="font-size: 18px; font-weight: bold; text-align: right; margin-right: 50px;">{sum_amount} </div>
        <hr>
        {notes}
    </body>
    </html>
    """

    return html_content


pdf_df = pdf_df.rename(
    columns={
        "title": "Activity",
        "string": "Description",
        "quantity": "QTY",
        "price": "Rate",
    }
)

html_content = dataframe_to_html(pdf_df)

with caculation:
    st.markdown("---")
    st.download_button(
        "Download Summary",
        data=html_content,
        file_name="Offer_Summary.html",
    )


hide_streamlit_style = """
<style>
.row-widget.stCheckbox span{
    font-size:12px;
}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
