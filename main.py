import langhcain_name_gen as lh 
import streamlit as st 

st.title("🐶 Pet Name generator")

animal_type = st.sidebar.selectbox("What is your pet name",("cat","dog","rabbit",("hen"),("duck")))

animal_color = st.sidebar.text_area(label=f"What color is your {animal_type}",max_chars=15)

if animal_color:
    response  = lh.pet_name_gen(animal_type,animal_color)
    st.write(response['text'])