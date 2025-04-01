import streamlit as st

st.set_page_config(
    page_title="Streamlit test-drive",
    page_icon="👋",
    layout="wide",
)

st.sidebar.success("Select a demo above.")

st.markdown("# Welcome to Streamlit! 👋")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    ### Learn more about DuckDB use cases?
    - Impressive show case using Dutch railway data, [Link](https://duckdb.org/2025/03/28/using-duckdb-in-streamlit.html),
        [GitHub](https://github.com/duckdb/duckdb-web/tree/main/code_examples/duckdb_streamlit)
"""
)
