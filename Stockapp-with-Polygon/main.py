import os
import streamlit as st
import pandas as pd
from polygon import RESTClient

# Basic UI
st.title('Polygon + Streamlit Stock Analysis App')
st.markdown("Explore stock details, quotes, and historical data by entering a ticker symbol below (e.g., AAPL for Apple, TSLA for Tesla).")

symbol = st.text_input('Enter a stock symbol', placeholder='e.g., AAPL')

with st.sidebar:
    # Check if API key is already stored in session state
    if "polygon_api_key" not in st.session_state:
        st.session_state["polygon_api_key"] = ""

    polygon_api_key = st.text_input("Polygon API Key", type="password", value=st.session_state["polygon_api_key"])

    # Save the API key and notify the user
    if polygon_api_key and st.session_state["polygon_api_key"] != polygon_api_key:
        st.session_state["polygon_api_key"] = polygon_api_key
        st.success("API Key saved! You won't need to re-enter it.")

    # Authenticate with Polygon API
    client = RESTClient(st.session_state["polygon_api_key"])

    col1, col2, col3 = st.columns(3)

# GET STOCK DETAILS
if col1.button("Get Details"):
    if not st.session_state["polygon_api_key"].strip() or not symbol.strip():
        st.error("Please add your Polygon API Key on the left <<<< and enter a stock symbol above.")
    else:
        try:
            details = client.get_ticker_details(symbol)
            st.success(f"Ticker: {details.ticker}\n\n"
                       f"Company Address: {details.address}\n\n"
                       f"Market Cap: {details.market_cap}")
        except Exception as e:
            st.exception(f"Exception: {e}")

# Current bid info
if col2.button("Get Quote"):
    if not st.session_state["polygon_api_key"].strip() or not symbol.strip():
        st.error("Please add your Polygon API Key on the left <-- and enter a stock symbol above.")
    else:
        try:
            aggs = client.get_previous_close_agg(symbol)
            for agg in aggs:
                st.success(f"Ticker: {agg.ticker}\n\n"
                           f"Close: {agg.close}\n\n"
                           f"High: {agg.high}\n\n"
                           f"Low: {agg.low}\n\n"
                           f"Open: {agg.open}\n\n"
                           f"Volume: {agg.volume}")
        except Exception as e:
            st.exception(f"Exception: {e}")

# Historical data for the year
if col3.button("Get Historical"):
    if not st.session_state["polygon_api_key"].strip() or not symbol.strip():
        st.error("Please add your Polygon API Key on the left <-- and enter a stock symbol above.")
    else:
        try:
            dataRequest = client.list_aggs(
                ticker=symbol,
                multiplier=1,
                timespan="day",
                from_="2024-01-01",
                to="2024-04-29"
            )
            chart_data = pd.DataFrame(dataRequest)

            chart_data['date_formatted'] = chart_data['timestamp'].apply(
                lambda x: pd.to_datetime(x * 1000000))

            st.line_chart(chart_data, x="date_formatted", y="close")

        except Exception as e:
            st.exception(f"Exception: {e}")