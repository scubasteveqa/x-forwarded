import streamlit as st

st.write("""
# IP Spoofing Detection App
This app shows how X-Forwarded-For headers are processed by infrastructure.
""")

# Get the X-Forwarded-For header
xff = st.context.headers.get("X-Forwarded-For", "")

st.write("## X-Forwarded-For Header Analysis")
if not xff:
    st.write("❌ No X-Forwarded-For header found")
elif "," in xff:
    # Parse the chain
    ips = [ip.strip() for ip in xff.split(",")]
    st.write("🚨 **Potential IP Spoofing Detected!**")
    st.write(f"📌 First IP in chain (likely spoofed): **{ips[0]}**")
    st.write(f"📌 Last IP in chain (likely real client): **{ips[-1]}**")
    st.write("📌 Complete IP chain:")
    for i, ip in enumerate(ips):
        st.write(f"  {i+1}. {ip}")
else:
    st.write(f"📌 Single IP address: **{xff}**")

# Show all headers for debugging
st.write("## All Request Headers")
st.write(dict(st.context.headers))
