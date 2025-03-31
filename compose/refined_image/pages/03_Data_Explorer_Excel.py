import streamlit as st
import duckdb
import pandas as pd
import os

st.set_page_config(
    page_title="Urban Data Explorer Excel",
    page_icon="🌆",
)

st.markdown("# Urban Data Explorer Excel")
st.sidebar.header("Urban Data Explorer Excel")

st.markdown(f"""
    This example imports an excel file containing two sheets, a purchases fact table and a
    country dimension table. DuckDB reads them and generates two tables out of them. For the
    visualization in streamlit we create a left inner join to be able to aggregate by meaningful
    country names.
""")

# File path (mounted inside the container or local folder)
DATA_PATH = "data/excel_test.xlsx"

def init_db():
    con = duckdb.connect(DB_PATH)
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS purchases AS
        SELECT * FROM read_xlsx('{DATA_PATH}', sheet = 'purchases');
    """)
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS countries AS
        SELECT * FROM read_xlsx('{DATA_PATH}', sheet = 'countries');
    """)
    con.close()

def load_data():
    con = duckdb.connect(DB_PATH)
    df = con.execute(f"""
        SELECT 
            p.ID,
            p.Price,
            p.Quantity,
            c.name AS Country
        FROM purchases AS p
        LEFT JOIN countries AS c
        ON p.country=c.id;
    """).fetchdf()
    con.close()
    return df

def aggregate_data():
    con = duckdb.connect(DB_PATH)
    df = con.execute(f"""
        WITH purchasejoin AS (
            SELECT 
                p.ID,
                p.Price,
                p.Quantity,
                c.name AS Country
            FROM purchases AS p
            LEFT JOIN countries AS c
            ON p.country=c.id
        ), aggregate AS (
            SELECT
                Country,
                SUM(Price) AS Revenue,
                COUNT(*) AS Orders,
                SUM(Quantity) AS Items
            FROM purchasejoin
            GROUP BY Country
        ) SELECT * FROM aggregate ORDER BY Revenue DESC, Country ASC;
    """).fetchdf()
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

    # Display summary
    st.subheader("📊 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # Show column stats
    st.subheader("📈 Column Stats")
    st.write(df.describe(include='all'))

    # Optional filtering UI
    st.subheader("🔎 Aggregation")
    df_agg = aggregate_data()
    st.dataframe(df_agg, use_container_width=True)
