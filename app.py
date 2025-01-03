import streamlit as st
import json
import pandas as pd

# Load JSON data
with open("data/output.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

# Streamlit App
st.title("🎬 Movie Service Finder")

# Sorting Options
sort_by = st.sidebar.selectbox("Sort movies by", ["Title", "Year", "Runtime"])
sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])
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


            cols = st.columns(4)
            cols[0].markdown("**Service**")
            cols[1].markdown("**Link**")
            cols[2].markdown("**Quality**")
            cols[3].markdown("**Price**")

            for offer in movie["offers"]:
                cols = st.columns(4)
                icon_url = offer.get("service_icon_url", "")
                cols[0].markdown(f"{offer['service']}")
                if icon_url:
                    cols[1].markdown(
                        f"<div><a href='{offer['url']}' target='_blank'><img src='{offer['service_icon_url']}' width='30'></a></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    cols[1].markdown(
                        "<div><a href='{offer['url']}' target='_blank'><img src='https://via.placeholder.com/200x300?text=No+Icon' width='30'></div>",
                        unsafe_allow_html=True,
                    )
                quality = "4K" if offer['quality'] == "_4K" else offer['quality']
                cols[2].markdown(f"{quality}")
                cols[3].markdown(f"{offer['price']} {offer['currency']}")

    else:
        st.write("No offers available.")

    st.write("---")

st.sidebar.success("Use sorting options to rearrange the movie list.")
