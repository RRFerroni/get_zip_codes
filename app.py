import streamlit as st
import pandas as pd
import shutil

# Give your app a title
st.title('Get the zip codes')

# Add a short description
st.write('This short app downloads a CSV containing the list of cities associated with their zip code, and returns the zip codes of the city you submitted.')

# Upload the CSV file
uploaded_file = st.file_uploader("Upload the CSV", type="csv")

# Create a form to manually enter the name of a city
form = st.form(key="zip_code")
city = form.text_input(label="Enter the name of a city")
submit = form.form_submit_button(label="Get the zip codes")

# Function that returns the following index:
# {city: [*zip_code]}
# Since lots of cities have the same name, the length of the list of the zip codes can be greater than 1
def create_index(df):
	feature_dict = pd.DataFrame.from_dict({
        "zip_code": df["Code Postal"].values,
        "city": df["Commune"].values}).groupby("city")['zip_code'].apply(set)
	return feature_dict.to_dict()

# Function that returns the list of the zip code(s) given a city
def get_zip_codes(index, city):
    try:
        zip_codes = index[city]
        return zip_codes 
    except:
        return None

# Check if you have uploaded a file
if uploaded_file is not None:
	# Read the file
    with open("cities.csv", "wb") as buffer:
        shutil.copyfileobj(uploaded_file, buffer)

    # Check if you have submitted a city
    if submit:
        # Read the CSV as a dataframe
        df = pd.read_csv("cities.csv", sep=';', header=0)
        # Create the index
        index = create_index(df) 
        # Get the list of zip codes
        zip_codes = get_zip_codes(index, city.upper())

        # Write the results
        st.header("Result: ")
        if zip_codes is None:
            st.write('No zip codes found! Check the spelling.')
        else:
            st.write(zip_codes)