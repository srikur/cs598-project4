import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

def main():
    st.title("Movie Recommendation System - srikurk2")
    st.sidebar.title("Project 4 CS 598")
    st.sidebar.write("Srikur Kanuparthy - srikurk2")

    # Sidebar for navigation
    app_mode = st.sidebar.selectbox("Select from System I or System II",
                                    ["System I - Select Genre", "System II - Rate Movies"])

    if app_mode == "System I - Select Genre":
        genre_selection()
    elif app_mode == "System II - Rate Movies":
        rate_movies()

def genre_selection():
    st.header("System I - Select Genre")

    genres = ["Select a genre", 'Drama','Musical','Comedy','Animation','Romance','Thriller','Action','Western',
              'Documentary','Horror','Crime','Adventure','War',"Children's",'Sci-Fi','Film-Noir','Mystery',
              'Fantasy']
    selected_genre = st.selectbox("Choose a genre", genres, placeholder="Select a genre")

    display_movies_by_genre(selected_genre)

def display_movies_by_genre(genre):

    if genre == "Select a genre":
        st.write("Please select a genre from the dropdown")
        return
    st.write(f"Displaying recommendations for genre: {genre}")
    
    top10movies = pd.read_csv('top10movies.csv', header=0)
    top10movies = top10movies[top10movies['Genres'] == genre]
    top10movies = top10movies[['MovieID', 'Title']]
    top10movies["Image"] = top10movies["MovieID"].apply(lambda x: f"MovieImages/{x}.jpg")

    # Display 2 rows of movie cards with 5 movie cards in each row
    c1, c2, c3, c4, c5 = st.columns(5)
    for i in range(0, 10):
        image = Image.open(top10movies.iloc[i]["Image"])
        image = image.resize((200, 300))
        if i < 2:
            with c1:
                st.image(image, caption=top10movies.iloc[i]["Title"])
        elif i < 4:
            with c2:
                st.image(image, caption=top10movies.iloc[i]["Title"])
        elif i < 6:
            with c3:
                st.image(image, caption=top10movies.iloc[i]["Title"])
        elif i < 8:
            with c4:
                st.image(image, caption=top10movies.iloc[i]["Title"])
        else:
            with c5:
                st.image(image, caption=top10movies.iloc[i]["Title"])


def rate_movies():
    st.header("System II - Rate Movies")

    # Create a session state to store the ratings
    if "random_movies" not in st.session_state:
        st.session_state["random_movies"] = pd.read_csv("movie_list.csv", header=0).sample(n=50, replace=False)
    if "ratings" not in st.session_state:
        st.session_state["ratings"] = st.session_state["random_movies"][["Title", "Rating"]]

    # Display 50 random movies with rating option
    if st.button("Display Movies to Rate"):
        st.session_state["random_movies"] = pd.read_csv("movie_list.csv", header=0).sample(n=50, replace=False)
        st.session_state["ratings"] = st.session_state["random_movies"][["Title", "Rating"]]
        display_random_movies()

    if st.button("Get Recommendations"):
        # Implement the logic for getting recommendations based on ratings
        st.write("Please wait. Calculating...")
        # combine ratings with movieID from movie_list.csv
        ratings = st.session_state["ratings"]
        movies = pd.read_csv("movie_list.csv", header=0)
        ratings = pd.merge(ratings, movies, on="Title", how="right")
        ratings = ratings[["MovieID", "Rating_x"]]
        ratings = ratings.set_index("MovieID")
        preds = pd.DataFrame(myIBCF(ratings))

        preds.columns = ["MovieID"]
        preds["Image"] = preds["MovieID"].apply(lambda x: f"MovieImages/{x[1:]}.jpg")
        preds["Title"] = preds["MovieID"].apply(lambda x: movies[movies["MovieID"] == int(x[1:])]["Title"].values[0])

        # Display 2 rows of movie cards with 5 movie cards in each row
        c1, c2, c3, c4, c5 = st.columns(5)
        for i in range(0, 10):
            image = Image.open(preds.iloc[i]["Image"])
            image = image.resize((200, 300))
            if i < 2:
                with c1:
                    st.image(image, caption=preds.iloc[i]["Title"])
            elif i < 4:
                with c2:
                    st.image(image, caption=preds.iloc[i]["Title"])
            elif i < 6:
                with c3:
                    st.image(image, caption=preds.iloc[i]["Title"])
            elif i < 8:
                with c4:
                    st.image(image, caption=preds.iloc[i]["Title"])
            else:
                with c5:
                    st.image(image, caption=preds.iloc[i]["Title"])



def change_rating(title):
    value = st.session_state[f"{title}"]
    movies = pd.read_csv("movie_list.csv", header=0)
    movies.loc[movies["Title"] == value, "Rating"] = value
    st.header("Scroll down for the buttons!")
    display_random_movies()

def display_random_movies():
    st.write("Please rate the following movies")
    
    # read movies from movie_list.txt
    if "random_movies" not in st.session_state:
        random_movies = pd.read_csv("movie_list.csv", header=0).sample(n=50, replace=False)
        st.session_state["random_movies"] = random_movies
    else:
        random_movies = st.session_state["random_movies"]

    if "ratings" not in st.session_state:
        st.session_state["ratings"] = random_movies[["Title", "Rating"]]
    else:
        random_movies["Rating"] = st.session_state["ratings"]["Rating"]

    # Display 10 rows of movie cards with 5 movie cards in each row. Also display a star rating option for each movie
    c1, c2, c3, c4, c5 = st.columns(5)
    for i in range(0, 50):
        image = Image.open(random_movies.iloc[i]["Image"])
        image = image.resize((200, 300))
        if i < 10:
            with c1:
                st.image(image, caption=random_movies.iloc[i]["Title"])
                # st.write(str(st.session_state["ratings"].iloc[i]["Rating"]) == "nan")
                st.slider(label="Rate this movie", min_value=0, 
                          max_value=5, value=st.session_state["ratings"].iloc[i]["Rating"] if str(st.session_state["ratings"].iloc[i]["Rating"]) != "nan" else 0, key=random_movies.iloc[i]["Title"], 
                          on_change=change_rating, args=(random_movies.iloc[i]["Title"],))
        elif i < 20:
            with c2:
                st.image(image, caption=random_movies.iloc[i]["Title"])
                st.slider(label="Rate this movie", min_value=0, 
                          max_value=5, value=st.session_state["ratings"].iloc[i]["Rating"] if str(st.session_state["ratings"].iloc[i]["Rating"]) != "nan" else 0, key=random_movies.iloc[i]["Title"], 
                          on_change=change_rating, args=(random_movies.iloc[i]["Title"],))
        elif i < 30:
            with c3:
                st.image(image, caption=random_movies.iloc[i]["Title"])
                st.slider(label="Rate this movie", min_value=0, 
                          max_value=5, value=st.session_state["ratings"].iloc[i]["Rating"] if str(st.session_state["ratings"].iloc[i]["Rating"]) != "nan" else 0, key=random_movies.iloc[i]["Title"], 
                          on_change=change_rating, args=(random_movies.iloc[i]["Title"],))
        elif i < 40:
            with c4:
                st.image(image, caption=random_movies.iloc[i]["Title"])
                st.slider(label="Rate this movie", min_value=0, 
                          max_value=5, value=st.session_state["ratings"].iloc[i]["Rating"] if str(st.session_state["ratings"].iloc[i]["Rating"]) != "nan" else 0, key=random_movies.iloc[i]["Title"], 
                          on_change=change_rating, args=(random_movies.iloc[i]["Title"],))
        else:
            with c5:
                st.image(image, caption=random_movies.iloc[i]["Title"])
                st.slider(label="Rate this movie", min_value=0, 
                          max_value=5, value=st.session_state["ratings"].iloc[i]["Rating"] if str(st.session_state["ratings"].iloc[i]["Rating"]) != "nan" else 0, key=random_movies.iloc[i]["Title"], 
                          on_change=change_rating, args=(random_movies.iloc[i]["Title"],))

def myIBCF(newuser):
    newuser.index = ["m" + str(i) for i in newuser.index]
    S = pd.read_csv("similarity.csv", header=0, index_col=0)
    newuser = newuser[newuser.index.isin(S.index)]

    # create predictions df with columns movies and ratings. Movies based on newuser index
    predictions = pd.DataFrame(columns=["movies", "ratings"])
    predictions["movies"] = newuser.index
    predictions["ratings"] = np.nan

    for l in range(len(newuser)):
        if np.isnan(newuser.iloc[l][0]):
            sim_scores = S.loc[newuser.index[l], :]
            # print(sim_scores)

            # get the 30 highest similarity scores
            neighbors_idx = sim_scores.sort_values(ascending=False).index[:30]
            # for i in neighbors_idx:
            #     st.write(i, newuser.loc[i][0], sim_scores.loc[i])
            
            numerator = np.sum([sim_scores.loc[i] * newuser.loc[i][0] if (not np.isnan(newuser.loc[i][0])) and (not np.isnan(sim_scores.loc[i])) else 0 for i in neighbors_idx])
            denominator = np.sum([sim_scores.loc[i] if (not np.isnan(newuser.loc[i][0])) and (not np.isnan(sim_scores.loc[i])) else 0 for i in neighbors_idx])

            if denominator != 0:
                predictions.iloc[l, 1] = numerator / denominator
    
    # get top 10 movies
    top_movies_idx = predictions.sort_values(by="ratings", ascending=False).index[:10]

    # print the top 10 movies
    # print(predictions.iloc[top_movies_idx])

    # print the top 10 movies' names
    # print(R_df.columns[top_movies_idx])

    return S.columns[top_movies_idx]

if __name__ == "__main__":
    main()
