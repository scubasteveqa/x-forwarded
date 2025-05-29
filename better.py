import streamlit as st

st.write("""
# IP Header Analysis App
This app shows how request headers are processed by the infrastructure.
""")

# Get the X-Forwarded-For header and other potential IP headers
xff = st.context.headers.get("X-Forwarded-For", "")
real_ip = st.context.headers.get("X-Real-IP", "")
remote_addr = st.context.headers.get("Remote-Addr", "")
client_ip = st.context.headers.get("Client-IP", "")

st.write("## Your Request IP Information")
st.write(f" Raw X-Forwarded-For value: **{xff}**")

if real_ip:
    st.write(f" X-Real-IP: **{real_ip}**")
if remote_addr:
    st.write(f" Remote-Addr: **{remote_addr}**")
if client_ip:
    st.write(f" Client-IP: **{client_ip}**")

# Parse X-Forwarded-For if it exists
if xff:
    if "," in xff:
        ips = [ip.strip() for ip in xff.split(",")]
        st.write("### X-Forwarded-For Chain Analysis")
        st.write(f" First IP in chain: **{ips[0]}**")
        st.write(f" Last IP in chain: **{ips[-1]}**")
        st.write(" Complete chain:")
        for i, ip in enumerate(ips):
            st.write(f"  {i+1}. {ip}")
    else:
        st.write(f" Single forwarded IP: **{xff}**")

# Show all headers for complete debugging
st.write("## All Request Headers")
st.write(dict(st.context.headers))
