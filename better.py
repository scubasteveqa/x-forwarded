import streamlit as st

st.write("""
# My first app
Hello *everybody!*

Thanks for using Posit Connect Cloud!
""")

# Display a more comprehensive set of forwarding-related headers
forwarding_headers = {
    "X-Forwarded-For": st.context.headers.get("X-Forwarded-For", ""),
    "X-Forwarded-Host": st.context.headers.get("X-Forwarded-Host", ""),
    "X-Real-IP": st.context.headers.get("X-Real-IP", ""),
    "Forwarded": st.context.headers.get("Forwarded", ""),
    "X-Client-IP": st.context.headers.get("X-Client-IP", ""),
    "CF-Connecting-IP": st.context.headers.get("CF-Connecting-IP", "")
}

st.write("## Selected Headers")
st.write(forwarding_headers)

# Parse X-Forwarded-For to show the full IP chain
st.write("## X-Forwarded-For Chain Analysis")
xff = st.context.headers.get("X-Forwarded-For", "")
if xff:
    ip_chain = [ip.strip() for ip in xff.split(",")]
    if len(ip_chain) > 1:
        st.write(f"First IP in chain (possibly spoofed): {ip_chain[0]}")
        st.write(f"Last IP in chain (likely original client): {ip_chain[-1]}")
        st.write("Full chain:")
        for i, ip in enumerate(ip_chain):
            st.write(f"{i+1}. {ip}")
    else:
        st.write(f"Single IP: {xff}")
else:
    st.write("No X-Forwarded-For header found")

# Optionally keep the other sections
st.write("## Query parameters")
st.write(st.query_params)

# Show all headers for debugging
st.write("## All Request Headers")
st.write(dict(st.context.headers))
