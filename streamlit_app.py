import pandas
import requests
import streamlit
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("CHOOSE FRUIT")
  else:
    fruit_advice = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruit_advice)
    
except URLError as e:
  streamlit.error()

  

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM pc_rivery_db.public.FRUIT_LOAD_LIST")
    return my_cur.fetchall()

streamlit.header("Fruit List Contains:")
if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  

def insert_fruit(fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO pc_rivery_db.public.FRUIT_LOAD_LIST values ('from streamlit')")
    return "thanks for adding " + fruit_to_add
  
fruit_to_add = fruit_choice = streamlit.text_input('what fruit would you like to add?')
if streamlit.button("ADD FRUIT"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  response = insert_fruit(fruit_to_add)
  streamlit.text(response)
