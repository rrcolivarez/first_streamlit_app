import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# Let's Create Some User Interaction
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')  # Choose the Fruit Name Column as the Index
#streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
  #streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#Choose a Few Fruits to Set a Good Example
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#L9 Streamlit - USING APIs
#Create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    #import requests
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # take the json version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized



#New Section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # output it the screen as table
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()


#L12


#import snowflake.connector
streamlit.header("The fruit load list contains:")

#Snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()  

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows) 


#don't run anything past here while we troubleshoot
streamlit.stop()

#Add a second text entry box
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')") #This will not work correctly, but just go with it for now
