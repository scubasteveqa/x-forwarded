import streamlit as st

st.write("""
# My first app
Hello *everybody!*

Thanks for using Posit Connect Cloud!
""")

# Filter and display only the specific headers you want
filtered_headers = {
    "X-Forwarded-For": st.context.headers.get("X-Forwarded-For", ""),
    "X-Forwarded-Host": st.context.headers.get("X-Forwarded-Host", "")
}

st.write("## Selected Headers")
st.write(filtered_headers)

# Optionally keep the other sections
st.write("## Query parameters")
st.write(st.query_params)
