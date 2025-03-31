import streamlit as st
import duckdb
import pandas as pd
import os

st.set_page_config(
    page_title="Urban Data Explorer",
    page_icon="🌆",
)

st.markdown("# Urban Data Explorer")
st.sidebar.header("Urban Data Explorer")

st.markdown("Explore and filter your dataset using DuckDB and Streamlit.")

# File path (mounted inside the container or local folder)
DATA_PATH = "data/cities.csv"  # Change to .csv if that's your real data

def init_db():
    con = duckdb.connect(DB_PATH)
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS cities AS
        SELECT * FROM read_csv_auto('{DATA_PATH}');
    """)
    con.close()

def load_data():
    con = duckdb.connect(DB_PATH)
    df = con.execute("SELECT * FROM cities;").fetchdf()
    con.close()
    return df

# Check if file exists
if not os.path.exists(DATA_PATH):
    st.error(f"Data file not found at `{DATA_PATH}`. Please upload or mount it.")
else:
    DB_PATH = os.getenv("DUCKDB_PATH", "urban_data.duckdb")

    # Initialize database
    init_db()

    df = load_data()

    # Load data using DuckDB
    # con = duckdb.connect(database=':memory:')
    # con.execute(f"""
    #     CREATE TABLE urban_data AS 
    #     SELECT * FROM read_csv_auto('{DATA_PATH}')
    # """)
    
    # # Read as Pandas DataFrame
    # df = con.execute("SELECT * FROM urban_data").fetchdf()

    # Display summary
    st.subheader("📊 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # Show column stats
    st.subheader("📈 Column Stats")
    st.write(df.describe(include='all'))

    # Optional filtering UI
    st.subheader("🔎 Filter Rows")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if numeric_cols:
        col_to_filter = st.selectbox("Select a numeric column to filter by", numeric_cols)
        min_val, max_val = df[col_to_filter].min(), df[col_to_filter].max()
        selected_range = st.slider("Value range", float(min_val), float(max_val), (float(min_val), float(max_val)))
        filtered_df = df[(df[col_to_filter] >= selected_range[0]) & (df[col_to_filter] <= selected_range[1])]
        st.write(f"Filtered rows: {len(filtered_df)}")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No numeric columns available for filtering.")
