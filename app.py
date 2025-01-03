import streamlit as st
import json
import pandas as pd

# Load JSON data
with open("data/output.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

# Streamlit App
st.title("🎬 All Movies Viewer")

# Sorting Options
sort_by = st.sidebar.selectbox("Sort movies by", ["Title", "Year", "Runtime"])

sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])

# Sorting Logic
reverse_order = sort_order == "Descending"

if sort_by == "Title":
    movies.sort(key=lambda x: x["title"], reverse=reverse_order)
elif sort_by == "Year":
    movies.sort(key=lambda x: x["year"], reverse=reverse_order)
elif sort_by == "Runtime":
    movies.sort(key=lambda x: x["runtime"], reverse=reverse_order)

# Display All Movies
for movie in movies:
    # Display Poster (Centered with Placeholder)
    poster_url = movie.get("poster_url", "")
    if poster_url:
        st.markdown(
            f"<div style='text-align: center;'><img src='{poster_url}' width='200'></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='text-align: center;'><img src='https://via.placeholder.com/200x300?text=No+Poster' width='200'></div>",
            unsafe_allow_html=True,
        )
        
    st.subheader(movie["title"])
    st.write(f"**Year:** {movie['year']}")
    st.write(f"**Runtime:** {movie['runtime']} min")
    st.write(f"**Genres:** {', '.join(movie['genres'])}")
    st.write(f"**IMDB ID:** {movie['imdb_id']}")
    st.write(f"**Description:** {movie['description']}")

    # Display Offers as a Table
    st.write("💰 **Offers:**")
    if "offers" in movie and movie["offers"]:
        offer_types = set(offer["type"] for offer in movie["offers"])
        for offer_type in offer_types:
            st.write(f"### {offer_type.capitalize()}")

            # Display Offers in columns (with Service, Quality, Price, Link)
            for offer in movie["offers"]:
                cols = st.columns(
                    5
                )  # 4 columns per row (Service, Quality, Price, Link)
                # Service column
                cols[0].markdown(f"**Service**: {offer['service']}")
                # Quality column
                cols[1].markdown(f"**Quality**: {offer['quality']}")
                # Price column
                cols[2].markdown(f"**Price**: {offer['price']} {offer['currency']}")
                # Link column with the image and URL
                cols[3].markdown(f"**Link**: [{offer['service']}]({offer['url']})")
                icon_url = offer.get("service_icon_url", "")
                if icon_url:
                    cols[4].markdown(
                        f"<div style='text-align: center;'><img src='{icon_url}' width='20'></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    cols[4].markdown(
                        "<div style='text-align: center;'><img src='https://via.placeholder.com/200x300?text=No+Icon' width='20'></div>",
                        unsafe_allow_html=True,
                    )

    else:
        st.write("No offers available.")

    st.write("---")

st.sidebar.success("Use sorting options to rearrange the movie list.")
