import streamlit as st
import json
from utils.constants import GENRE_MAP, IMDB_LOGO_URL, RT_LOGO_URL

# Load JSON data
with open("data/output.json", "r", encoding="utf-8") as f:
    movies = json.load(f)
with open("data/ratings.json", "r", encoding="utf-8") as f:
    ratings = json.load(f)

# Streamlit App
st.title("🎬 Movie Service Finder")

# Sidebar Filters
st.sidebar.header("Filter Movies")

# Get the actual min and max values from the data
min_imdb_rating = min(
    (ratings.get(movie['imdb_id'], {}).get('imdb_rating', 0) for movie in movies if ratings.get(movie['imdb_id'], {}).get('imdb_rating') is not None),
    default=0.0
)
max_imdb_rating = max(
    (ratings.get(movie['imdb_id'], {}).get('imdb_rating', 10) for movie in movies if ratings.get(movie['imdb_id'], {}).get('imdb_rating') is not None),
    default=10.0
)

min_rt_rating = min(
    (ratings.get(movie['imdb_id'], {}).get('rt_rating', 0) for movie in movies if ratings.get(movie['imdb_id'], {}).get('rt_rating') is not None),
    default=0
)
max_rt_rating = max(
    (ratings.get(movie['imdb_id'], {}).get('rt_rating', 100) for movie in movies if ratings.get(movie['imdb_id'], {}).get('rt_rating') is not None),
    default=100
)

min_year = min((movie['year'] for movie in movies), default=1900)
max_year = max((movie['year'] for movie in movies), default=2030)

min_runtime = min((movie['runtime'] for movie in movies), default=0)
max_runtime = max((movie['runtime'] for movie in movies), default=500)

# Extract unique offer types and services from the movie data
offer_types = set()
services = set()
for movie in movies:
    if "offers" in movie and movie["offers"]:
        for offer in movie["offers"]:
            offer_types.add(offer["type"])
            services.add(offer["service"])

# Convert sets to lists
offer_types = list(offer_types)
services = list(services)

# IMDb Rating Filter (min and max)
min_imdb_rating, max_imdb_rating = st.sidebar.slider(
    "IMDb Rating",
    min(
        (ratings.get(movie['imdb_id'], {}).get('imdb_rating', 0) for movie in movies if ratings.get(movie['imdb_id'], {}).get('imdb_rating') is not None),
        default=0.0
    ),
    max(
        (ratings.get(movie['imdb_id'], {}).get('imdb_rating', 10) for movie in movies if ratings.get(movie['imdb_id'], {}).get('imdb_rating') is not None),
        default=10.0
    ),
    (min_imdb_rating, max_imdb_rating),
    step=0.1,
    format="%.1f"
)

# Rotten Tomatoes Rating Filter (min and max)
min_rt_rating, max_rt_rating = st.sidebar.slider(
    "Rotten Tomatoes Rating",
    min(
        (ratings.get(movie['imdb_id'], {}).get('rt_rating', 0) for movie in movies if ratings.get(movie['imdb_id'], {}).get('rt_rating') is not None),
        default=0
    ),
    max(
        (ratings.get(movie['imdb_id'], {}).get('rt_rating', 100) for movie in movies if ratings.get(movie['imdb_id'], {}).get('rt_rating') is not None),
        default=100
    ),
    (min_rt_rating, max_rt_rating),
    step=1,
    format="%d"
)

# Year Filter (min and max)
min_year, max_year = st.sidebar.slider(
    "Year",
    min_value=min(
        (movie['year'] for movie in movies), default=1900
    ),
    max_value=max(
        (movie['year'] for movie in movies), default=2030
    ),
    value=(min_year, max_year)
)

# Runtime Filter (min and max)
min_runtime, max_runtime = st.sidebar.slider(
    "Runtime (minutes)",
    min_value=min(
        (movie['runtime'] for movie in movies), default=0
    ),
    max_value=max(
        (movie['runtime'] for movie in movies), default=500
    ),
    value=(min_runtime, max_runtime)
)

# Genre Filter (Checklist) - Start with no genres checked
available_genres = list(GENRE_MAP.values())  # Get the genre names
selected_genres = st.sidebar.multiselect(
    "Genres",
    available_genres,
    []  # Default to no genres selected
)

# Offer Type Filter (Checklist)
selected_offer_types = st.sidebar.multiselect(
    "Offer Types",
    offer_types,
    []  # Default to no offer types selected
)

# Service Filter (Checklist)
selected_services = st.sidebar.multiselect(
    "Services",
    services,
    []  # Default to no services selected
)

# Search Box
search_query = st.sidebar.text_input("Search for a movie")

# Filtering movies based on the search query
if search_query:
    movies = [movie for movie in movies if search_query.lower() in movie["title"].lower()]

# Filtering based on IMDb and Rotten Tomatoes ratings, year, runtime, genres, offer types, and services
filtered_movies = []

for movie in movies:
    imdb_rating = ratings.get(movie['imdb_id'], {}).get('imdb_rating', None)
    rt_rating = ratings.get(movie['imdb_id'], {}).get('rt_rating', None)
    year = movie["year"]
    runtime = movie["runtime"]
    movie_genres = [GENRE_MAP.get(genre_code, genre_code) for genre_code in movie['genres']]  # Genre names
    movie_offer_types = [offer["type"] for offer in movie.get("offers", [])]
    movie_services = [offer["service"] for offer in movie.get("offers", [])]

    # Handle None values for imdb_rating and rt_rating
    imdb_rating = imdb_rating if imdb_rating is not None else 0
    rt_rating = rt_rating if rt_rating is not None else 0

    # Apply filters
    if (min_imdb_rating <= imdb_rating <= max_imdb_rating) and \
       (min_rt_rating <= rt_rating <= max_rt_rating) and \
       (min_year <= year <= max_year) and \
       (min_runtime <= runtime <= max_runtime) and \
       (not selected_genres or any(genre in selected_genres for genre in movie_genres)):

        # Handle offer type and service correlation
        if selected_offer_types and selected_services:
            # Filter for movies where both the offer type and service match
            offer_service_match = any(
                offer["type"] in selected_offer_types and offer["service"] in selected_services
                for offer in movie.get("offers", [])
            )
            if offer_service_match:
                filtered_movies.append(movie)

        # If only offer type or only service is selected
        elif selected_offer_types:
            if any(offer["type"] in selected_offer_types for offer in movie.get("offers", [])):
                filtered_movies.append(movie)
        elif selected_services:
            if any(offer["service"] in selected_services for offer in movie.get("offers", [])):
                filtered_movies.append(movie)
        else:
            # If no offer type or service is selected, include all matching movies
            filtered_movies.append(movie)

# Sorting Options
sort_by = st.sidebar.selectbox("Sort movies by", ["Title", "Year", "Runtime", "IMDb", "Rotten Tomatoes"])
sort_order = st.sidebar.radio("Sort order", ["Ascending", "Descending"])
reverse_order = sort_order == "Descending"

if sort_by == "Title":
    filtered_movies.sort(key=lambda x: x["title"], reverse=reverse_order)
elif sort_by == "Year":
    filtered_movies.sort(key=lambda x: x["year"], reverse=reverse_order)
elif sort_by == "Runtime":
    filtered_movies.sort(key=lambda x: x["runtime"], reverse=reverse_order)
elif sort_by == "IMDb":
    filtered_movies.sort(
        key=lambda x: float(ratings.get(x['imdb_id'], {}).get('imdb_rating') or 0),
        reverse=reverse_order
    )
elif sort_by == "Rotten Tomatoes":
    filtered_movies.sort(
        key=lambda x: float(ratings.get(x['imdb_id'], {}).get('rt_rating') or 0),
        reverse=reverse_order
    )

# Pagination Settings
movies_per_page = 10  # 10 movies per page
num_pages = len(filtered_movies) // movies_per_page + (1 if len(filtered_movies) % movies_per_page != 0 else 0)

# Session state to store the current page
if "page" not in st.session_state:
    st.session_state.page = 1

# Create a horizontal layout for buttons using columns
col1, col2, col3 = st.columns([1, 5, 1])  # Creating a third column for spacing

with col1:
    if st.button("Previous") and st.session_state.page > 1:
        st.session_state.page -= 1

with col3:
    if st.button("Next") and st.session_state.page < num_pages:
        st.session_state.page += 1

# Calculate the slice for the selected page
start_idx = (st.session_state.page - 1) * movies_per_page
end_idx = min(st.session_state.page * movies_per_page, len(filtered_movies))

# Display All Movies for the selected page
for movie in filtered_movies[start_idx:end_idx]:
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
    mapped_genres = [GENRE_MAP.get(genre_code, genre_code) for genre_code in movie['genres']]
    st.write(f"**Genres:** {', '.join(mapped_genres)}")
    imdb_rating = ratings.get(movie['imdb_id'], {}).get('imdb_rating')
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="{IMDB_LOGO_URL}" alt="IMDb Logo" width="50">
            <span style="font-size: 18px; font-weight: bold;">{imdb_rating if imdb_rating is not None else 'None'}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    rt_rating = ratings.get(movie['imdb_id'], {}).get('rt_rating')
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="{RT_LOGO_URL}" alt="RT Logo" width="50">
            <span style="font-size: 18px; font-weight: bold;">{f"{rt_rating} %" if rt_rating is not None else 'None'}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(f"**Description:** {movie['description']}")

    # Display Offers as a Table
    st.write("💰 **Offers:**")
    if "offers" in movie and movie["offers"]:
        offer_types = set(offer["type"] for offer in movie["offers"])
        for offer_type in offer_types:
            st.write(f"### {offer_type.capitalize()}")

            # Column headers
            cols = st.columns(4)
            cols[0].markdown("**Service**")
            cols[1].markdown("**Link**")
            cols[2].markdown("**Quality**")
            cols[3].markdown("**Price**")

            # Display offers in columns
            for offer in movie["offers"]:
                if offer["type"] != offer_type:
                    continue
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
                price = f"{offer['price']} {offer['currency']}" if offer['price'] else ""
                cols[3].markdown(price)

    else:
        st.write("No offers available.")

    st.write("---")

# Display pagination info
st.write(f"Page {st.session_state.page} of {num_pages}")
st.sidebar.success("Use sorting options to rearrange the movie list.")
