import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include, with defaults 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# REST API Call to fruityvice
streamlit.header("Fruityvice Fruit Advice!")

#create a function to group code
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # streamlit.text(fruityvice_response.json())
    # normalize the json response payload 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

    
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  # streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
     streamlit.error("Please select a fruit to get information.")
  else:
    # display the JSON in a table
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
    
except URLError as e:
  streamlit.error()
  
streamlit.header("The fruit load list contains:")
#Snowflake-related functions

#don't run anything past here while we troubleshoot
#streamlit.stop();

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()
        
#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT into pc_rivery_db.public.fruit_load_list values('" new_fruit "')")
        streamlit.write('The user entered ', new_fruit)
        return "Thanks for adding "+ new_fruit


fruit_add = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.text(insert_row_snowflake(fruit_add)
                   






