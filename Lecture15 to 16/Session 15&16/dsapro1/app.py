import streamlit as st
from random_utils import generate_random_numbers, analyze_numbers
from analyzer import RandomAnalyzer

st.title("Random Number Analyzer")

count = st.slider("Select number of random values", 10, 1000, 100)
lower = st.number_input("Lower Bound", value=1)
upper = st.number_input("Upper Bound", value=100)

if st.button("Generate and Analyze"):
    nums = generate_random_numbers(count, lower, upper)
    analyzer = RandomAnalyzer(nums)
    df = analyzer.to_dataframe()

    st.subheader("Generated Numbers")
    st.dataframe(df)

    st.subheader("Analysis")
    stats = analyze_numbers(nums)
    st.write(stats)
