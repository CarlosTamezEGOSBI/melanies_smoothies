# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write("""Choose the fruits you want on your custom Smoothie!""")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
name_on_smoothie = st.text_input("Name on Smoothie:")
st.write('"Choose the fruits your want in your custom Smoothie"')

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:"
    , my_dataframe
    , max_selections=5
)

ingredients_string = ''
vCount=0
vInsert = False
vRemaining = 0

if ingredients_list:
    for fruit_chosen in ingredients_list:
        if vCount==4:
            ingredients_string += fruit_chosen
        elif vCount >= 5:
            ingredients_string = ingredients_string
        elif vCount ==0:
            ingredients_string += fruit_chosen
        else:
            ingredients_string += ", " + fruit_chosen #fruit_chosen + ", " #"', '" 
        vRemaining = 4 - vCount
        vCount = vCount + 1 

    if vRemaining >= 1:
        st.write(str(vRemaining) + ' Ingredients Left.')
        
    if vCount > 5:
        st.write('Just choose up to 5 ingredients. Please delete ' + str(vCount-5) + ' ingredients.')
        vInsert = False
    elif vCount<=5:
        vInsert = True

    if vInsert:
        time_to_insert = st.button('Order here!')
    else:
        time_to_insert = False
    
    if time_to_insert:
        if ingredients_string != "" and name_on_smoothie != "":
            my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                                    values ('""" + ingredients_string + """', '""" + name_on_smoothie + """')"""

            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        else:
            if name_on_smoothie == "":
                st.write("Please write a name on your smoothie.")
                
            if ingredients_string == "":
                st.write("Choose your fruits befor order.")
