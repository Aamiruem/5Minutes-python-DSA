import streamlit as st

def is_binary_palindrome(num):
    binary_str = bin(num)[2:] 
    return binary_str == binary_str[::-1], binary_str

st.title("🔁 Binary Palindrome Checker")

num = st.number_input("Enter a decimal number:", min_value=0, value=9)

if st.button("Check Palindrome"):
    result, binary = is_binary_palindrome(num)
    st.write(f"**Binary Representation:** {binary}")
    if result:
        st.success(f"✅ {num} is a Binary Palindrome")
    else:
        st.error(f"❌ {num} is NOT a Binary Palindrome.")
