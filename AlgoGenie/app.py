import streamlit as st
from teams.DSA_team import get_dsa_team_and_docker

st.title("AlgoGenie - Our DSA Problem Solver")
st.write("Welcome to AlgoGenie, your personal DSA Problem Solver! Here you may ask solutions to various data structures and algorithms problems.")

task = st.text_input("Enter your DSA problem here:")

if st.button("Run"):
    st.write("Running the task...")

    team, docker = get_dsa_team_and_docker()