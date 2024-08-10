# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write("""Choose the fruits you want on your custom Smoothie!""")

cnx = st.connection("snowflake")
session = cnx.session()

name_on_smoothie = st.text_input("Name on Smoothie:")
st.write('"Choose the fruits your want in your custom Smoothie"')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

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
        #if vCount==4:
            #ingredients_string += fruit_chosen
        #elif vCount >= 5:
            #ingredients_string = ingredients_string
        #elif vCount ==0:
            #ingredients_string += fruit_chosen
        #else:
            #ingredients_string += ", " + fruit_chosen #fruit_chosen + ", " 

        ingredients_string += fruit_chosen + " "
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        #if search_on == ''
            #search_on = 'None'
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df =st.dataframe(data=fruityvice_response.json(), use_container_width=True)
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



