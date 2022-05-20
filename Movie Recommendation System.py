# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO CANVAS

import math
from collections import defaultdict
from collections import Counter

# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
# parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
# return: dictionary that maps movie to ratings
# WRITE YOUR CODE BELOW
def read_ratings_data(f):
    ratingsDict = {}
    userIDList  = []
    for line in open(f):
        movie, rating, userID = line.split('|')
        movie = movie.strip()
        rating = float(rating)
        if tuple((userID,movie)) in userIDList:
            continue
        if rating < 0 or rating> 5:
            continue
        else:
            userIDList.append(tuple((userID,movie)))
            if movie not in ratingsDict:
                #ratingsDict.append(tuple((movie, [])))
                #ratingsDict.update(movie)
                ratingsDict[movie] = []
            ratingsDict[movie].append(rating)
    return ratingsDict
        
   
    

# 1.2
# parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
# return: dictionary that maps movie to genre
# WRITE YOUR CODE BELOW
def read_movie_genre(f):
    movieGenres = {}
    movieIDList = []
    for line in open(f):
        genre, movieID, movie = line.split('|')
        genre = genre.strip()
        movie = movie.strip()
        if movieID in movieIDList:
            continue
        else:
            movieIDList.append(movieID)
            movieGenres[movie] = genre
    return movieGenres
            
            
        
        
    
  
    

# ------ TASK 2: PROCESSING DATA --------

# 2.1
# parameter d: dictionary that maps movie to genre
# return: dictionary that maps genre to movies
# WRITE YOUR CODE BELOW
def create_genre_dict(d):
    genreDict = {}
    for key,value in d.items():
        if value not in genreDict:
            genreDict[value] = []
        genreDict[value].append(key)
    
    return genreDict
    

    
# 2.2
# parameter d: dictionary that maps movie to ratings
# return: dictionary that maps movie to average rating
# WRITE YOUR CODE BELOW
def calculate_average_rating(d):
    averageRatingDict = {}
    for key,value in d.items():
        valuesAverage = 0.0
        if key not in averageRatingDict:
            for v in value:
                valuesAverage+=float(v)
            valuesAverage /= float(len(value))
            averageRatingDict[key] = valuesAverage
                
    
    return averageRatingDict
    

    
# ------ TASK 3: RECOMMENDATION --------

# 3.1
# parameter d: dictionary that maps movie to average rating
# parameter n: integer (for top n), default value 10
# return: dictionary that maps movie to average rating
# WRITE YOUR CODE BELOW
def get_popular_movies(d, n=10):
    topNMovies = {}
    d = sorted(d.items(), key = lambda item: item[1], reverse = True)
    i = 0
    
    for key,value in d:
        if (i >= n):
            break
        topNMovies[key] = value
        i += 1
    return topNMovies


    
# 3.2
# parameter d: dictionary that maps movie to average rating
# parameter thres_rating: threshold rating, default value 3
# return: dictionary that maps movie to average rating
# WRITE YOUR CODE BELOW
def filter_movies(d, thres_rating=3):
    moviesAboveThreshold = {}
    for key,value in d.items():
        if d[key] >= thres_rating:
            moviesAboveThreshold[key] = value
            
    return moviesAboveThreshold


    
# 3.3
# parameter genre: genre name (e.g. "Comedy")
# parameter genre_to_movies: dictionary that maps genre to movies
# parameter movie_to_average_rating: dictionary  that maps movie to average rating
# parameter n: integer (for top n), default value 5
# return: dictionary that maps movie to average rating
# WRITE YOUR CODE BELOW
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    listOfMoviesInGenre = genre_to_movies[genre]
    dct = {}
    for key,value in movie_to_average_rating.items():
        if key in listOfMoviesInGenre:
            dct[key] = value
    return get_popular_movies(dct,n)



    
# 3.4
# parameter genre: genre name (e.g. "Comedy")
# parameter genre_to_movies: dictionary that maps genre to movies
# parameter movie_to_average_rating: dictionary  that maps movie to average rating
# return: average rating of movies in genre
# WRITE YOUR CODE BELOW
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    listofMoviesInGenre = genre_to_movies[genre]
    
#     print(listofMoviesInGenre)
#     print('list of the movies in given genre ^^^^^^^^')
#     print()
#     print(genre_to_movies)
#     print('genre_to_movies ^')
#     print(movie_to_average_rating)
#     print('movie_to_average_rating')
    
    dct = {}
    genreAverage = 0.0
    count = 0
    for key,value in movie_to_average_rating.items():
        if key in listofMoviesInGenre:
            count +=1
            genreAverage += float(movie_to_average_rating[key])
    try:
        genreAverage /= float(count)
    except:
        return 0
    return genreAverage


    
# 3.5
# parameter genre_to_movies: dictionary that maps genre to movies
# parameter movie_to_average_rating: dictionary  that maps movie to average rating
# parameter n: integer (for top n), default value 5
# return: dictionary that maps genre to average rating
# WRITE YOUR CODE BELOW
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    genreAverage = {}
    for key,value in genre_to_movies.items():
        genreAverage[key] = get_genre_rating(key, genre_to_movies, movie_to_average_rating)
    return get_popular_movies(genreAverage,n)



# ------ TASK 4: USER FOCUSED  --------

# 4.1
# parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
# return: dictionary that maps user to movies and ratings
# WRITE YOUR CODE BELOW
def read_user_ratings(f):
    userRatings = {}
    userIDList = []
    userIDOnly = []
    for line in open(f):
        movie, rating, userID = line.split('|')
        movie = movie.strip()
        userID = userID.strip()
        rating = float(rating)
        if tuple((userID,movie)) in userIDList:
            # print('user already reviewed' + movie)
            # print()
            continue
        if userID not in userIDOnly:
            # print('user not in list')
            # print()
            userIDOnly.append(userID)
            userRatings[userID] = []
            
        userIDList.append(tuple((userID,movie)))
        userRatings[userID].append(tuple((movie,rating)))
    return userRatings


    
# 4.2
# parameter user_id: user id
# parameter user_to_movies: dictionary that maps user to movies and ratings
# parameter movie_to_genre: dictionary that maps movie to genre
# return: top genre that user likes
# WRITE YOUR CODE BELOW
def get_user_genre(user_id, user_to_movies, movie_to_genre):
  
    genre_to_movie = create_genre_dict(movie_to_genre)
    # print(genre_to_movie)
    # print()
    userRatings = dict(user_to_movies[user_id])
    
    # print(userRatings)
    # print()
    usersFavoriteGenre = genre_popularity(genre_to_movie, userRatings, 1)
    # print(usersFavoriteGenre)
    return list(usersFavoriteGenre.keys())[0]


    
# 4.3    
# parameter user_id: user id
# parameter user_to_movies: dictionary that maps user to movies and ratings
# parameter movie_to_genre: dictionary that maps movie to genre
# parameter movie_to_average_rating: dictionary that maps movie to average rating
# return: dictionary that maps movie to average rating
# WRITE YOUR CODE BELOW
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    preferredGenre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    tempDict = create_genre_dict(movie_to_genre)
    moviesOfGenre = tempDict[preferredGenre]
    movieAverageDictOfGenre = {}
    for key, value in movie_to_average_rating.items():
        if key not in moviesOfGenre:
            continue
        if key in dict(user_to_movies[user_id]).keys():
            continue
        
        movieAverageDictOfGenre[key] = value
    return get_popular_movies(movieAverageDictOfGenre, 3)



# -------- main function for your testing -----
def main():
    # write all your test code here
    # this function will be ignored by us when grading
   
    
    #     print("1.1")
    #     print(read_ratings_data("ratings210.txt"))
    #     print()
    #     print()

    #     print("1.2")
    #     print(read_movie_genre("movies210.txt"))
    #     print()
    #     print()

    #     print("2.1")
    #     genreDict = read_movie_genre("movies210.txt")
    #     genreDictLists = create_genre_dict(genreDict)
    #     print(genreDictLists)
    #     print()
    #     print()

    #     print("2.2")
    #     ratingDict = read_ratings_data("ratings210.txt")
    #     d = calculate_average_rating(ratingDict)
    #     print(d)
    #     print()
    #     print()

    #     print("3.1")
    #     print(get_popular_movies(d, 5))
    #     print()
    #     print()

    #     print("3.2")
    #     #topNMovies = get_popular_movies(d, 2)
    #     print(filter_movies(d, 3.5))
    #     print()
    #     print()

    #     print("3.3")
    #     popularInGenre = get_popular_in_genre("Adventure", genreDictLists, d, 3)
    #     print(popularInGenre)
    #     popularInGenre = get_popular_in_genre("Action", genreDictLists, d, 3)
    #     print(popularInGenre)
    #     print()
    #     # popularInGenre = get_popular_in_genre("Comedy", genreDictLists, d, 3)
    #     # print(popularInGenre)

    #     print("3.4")
    #     genreRating = get_genre_rating("Comedy", genreDictLists, d)
    #     print('comedy average = ' + str(genreRating)) 
    #     print ()
    #     genreRating = get_genre_rating("Action", genreDictLists, d)
    #     print('action average = ' + str(genreRating)) 
    #     print ()
    #     print()
    #     genreRating = get_genre_rating("Adventure", genreDictLists, d)
    #     print('adventure average = ' + str(genreRating)) 
    #     print ()

    #     print("3.5")
    #     popularity_of_genres = genre_popularity(genreDictLists, d, 5)
    #     print(popularity_of_genres)
    #     print()
    #     print()

    #     print("4.1")
    #     userRatings = read_user_ratings("ratings210.txt")
    #     print(userRatings)
    #     print()
    #     print()

    #     print("4.2")
    #     print(get_user_genre('1' ,userRatings, genreDict))
    #     print()
    #     print()

    #     print("4.3")
    #     print(recommend_movies('1', userRatings, genreDict, d))
    #     print()
    #     print()











# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions

    
# program will start at the following main() function call
# when you execute hw1.py
main()
    