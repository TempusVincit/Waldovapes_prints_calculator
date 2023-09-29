
# Calculator Manual


**The manual will consist of two parts, the first, explaining how the app works. The second explaining how to make changes and adjustments.**

First, the app is deployed from the GitHub repository through streamlit cloud into the streamlit platform, that means that if you want to change the xlsx or logos you just need to drag the new files into the GitHub repository, uploading the files to the repository is very intuitive and at any point you can contact us, and we will assist you. It is very important that the new files will have the same names as the old ones for the app to be able to read them.

**The company selection part- Basically the option for the select box are derived from the xlsx file (the structure of that excel will be explained in the end). Each vendor added to the file will be added to the app. Once the company is selected it is stored as a variable and used for all later calculations**

**Quantity – number input box, the quantity is straight forward, and the pricing is by the xlsx, same as the company if pricing or quantity thresholds change in the xlsx they will also change in the app, so it is dynamic.**

**Blanks – this part consists of a text input which is then saved on the order summary, a number input of base cost per blank a markup option to add a price or a certain percentage of the price and dyed option that once marked as yes opens a price input to add to each blanks price, the blanks price is multiplied by the total quantity of shirts.**

**Print locations – there is a text input box for the location title, a multi select box of the number of colors and checkboxes for all kinds of features, you can mark as many checkboxes as you like and they will be added to the final summary, the color pricing is decided by the quantity and number of colors as written in the xlsx, so you can always change the color pricing and the quantities, also if you’ll add a new vendor you can add the pricing option of this part for the new vendor**

**The option per unit section – the options are not hard coded and are derived from the xlsx, if you’ll add an option in the xlsx it will automatically be added to the option per unit section(each vendor can have different option based on the once that are written on the xlsx) selecting yes opens the option to pick the quantity and price, each option that is marked yes is then added to the final calculation and to the summary.**

**Setup fees – exactly as the part above, the only difference are they have different titles in the xlsx (source and summary)**

**The miscellaneous parts – nothing special, you can add the title price and quality, it is not xlsx dependent and it is added to the summary in final calculation.**

**Note – the text you’ll write here will be added at the bottom of the summary output.**

**Calculations – True cost per unit, is the total cost divided by the number of units, blanks subtotal is calculated by the blanks price, printing subtotal is calculated by the options per unit, miscellaneous per unit, and printing locations, the setup subtotal is calculated by the setup fees and setup fees miscellaneous, the pricing recommendation is just an adjustment in percentage added to the final totals above.**

**Download summary button – a button to download the summary.**


## **The Excel structure:**

There are two important sheets in the xlsx: “order_units”, “Production_Costs”

The two sheets must keep their names for everything to work.

Vendor names must be written in the same way (capital letters, extra spaces, etc. between the two sheets)


## **Order units sheet – this sheet is responsible for vendor names on the app and for the pricing of the printing locations, the prices are chosen by the quantity of blanks and quantity of colors they are inputted on the app.**

**Vendor column – stating the vendor that the data is related to.**

**Max_num_units – this is the maximum of units(quantity) this row price is related to, for example if the quantity is 100 then the row chosen will be the one with max_num_unit is 143  but if the quantity is 150 the row chosen will be the one with the max_num_unit is 299(for the final calculation the price of the selected row is taken)**

**max_num_colours – same logic as the column above but with colors**

**price – the price is determined by first filtering the table by the vendor chosen, then filtering it by the quantity and then filtering it by the number of colors chosen, it the end we are left with one row (for every printing location picked) this row price column determine the price.**

**If you want to add a vendor you have to follow the same logic, each Max_num_units  value as to have a row for each max_num_colours value and each  max_num_colours value  as to have a row for each Max_num_units  value, all those rows will have the same value in the vendor column and the pricing should be as you wish, if you’ll look at the excel sheet I think it will be clearer.**


## **Production_Costs sheet – this sheet is responsible for options and setup fee price, and it is a little easier to understand.**

**Vendor columns – same as in the previous sheet.**

**Category – states the category of the values in the row there are two options: Cost_Per_Design, Cost_Per_Unit_Per_Design.**

the first is for the setup fees and the second is for the options per unit. To add options just keep the category groups written same as now.

**Type - the name of the option or setup fee, you are free to call them as you wish, just make sure there are no duplicates in types for the same vendor as it might cause issues. This is the name that will show on the app and on the summary page.**

**Price – the price of the option that will show on the app once the option or setup fee is checked, you can change it in the excel but it is also changeable on the app. If you don’t want a default value but you do want the option to show you can either use QUOTE (with capital letters, like it is now) or you can just write 0 or any number you want, but it can only be a number or QUOTE not a different text input.**


Hope everything is clear, we encourage you to try and add some stuff just to try and see how it works and if you are facing any difficulties.
