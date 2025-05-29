import streamlit as st

st.write("""
# My first app
Hello *everybody!*

Thanks for using Posit Connect Cloud!
""")

# Get the X-Forwarded-For header
xff = st.context.headers.get("X-Forwarded-For", "")

# Parse the X-Forwarded-For chain
spoofing_detected = False
if xff and "," in xff:
    ips = [ip.strip() for ip in xff.split(",")]
    spoofing_detected = True
    st.write("## Spoofing Attempt Detected!")
    st.write(f"Potentially spoofed IP: {ips[0]}")
    st.write(f"Real client IP: {ips[-1]}")

# Show all headers for complete information
st.write("## All Headers")
st.write(dict(st.context.headers))

# Show raw X-Forwarded-For value
st.write("## Raw X-Forwarded-For Value")
st.write(xff)

# Optionally keep the other sections
st.write("## Query parameters")
st.write(st.query_params)
