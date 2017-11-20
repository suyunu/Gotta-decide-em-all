import string
import pandas as pd
import random
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec
import time
from pandas.tools.plotting import table
import numpy as np
import numpy.matlib
from matplotlib import colors as mcolors
#matplotlib inlin


movieRatings = pd.read_csv('ratings.txt', sep=' ')

def changeRates(rating):
    return rating-2

movieRatings['rating'] = movieRatings['rating'].apply(changeRates)

print('pulled movie ratings')

trustTable = pd.read_csv('trust.txt', sep=' ')

print('pulled trust table')

PokemonNames = open('pokemonnames.txt').read().splitlines()
names = {}

def getfriendsfriends(friends, filmTrust):
    friend_s_friends = pd.DataFrame(columns= ['user' , 'trust'])
    repeat_times = {}
    for trustor in friends['user']:
        friendstrustees= trustTable[trustTable['trustor'] == trustor ][['trustee','trust']]
        friendstrustees.columns = ['user', 'trust']
        for j in friendstrustees['user']:
            if friends[friends['user'] == j].empty and deleted_friends[deleted_friends['user'] == j].empty:
                if j in repeat_times:
                    repeated_user = friend_s_friends[friend_s_friends['user'] == j]
                    repeated_user['trust'] = (repeated_user['trust'] * repeat_times[j] + (((filmTrust[trustor]+2)/8)+0.5) )/(repeat_times[j]+1)
                    friend_s_friends[friend_s_friends['user'] == j] = repeated_user
                    repeat_times[j] +=1
                else:
                    friend_s_friend = friendstrustees[friendstrustees['user'] == j]
                    friend_s_friend['trust'] = list(friends[friends['user'] == int(trustor)]['trust'])[0] * (((filmTrust[int(trustor)]+2)/8)+0.5)
                    print(friend_s_friend)
                    friend_s_friends = friend_s_friends.append(friend_s_friend , ignore_index=True)
                    repeat_times[j] = 1
    return friend_s_friends

def hangoutsuccess(friends, filmTrust):
    friend_s_friends = getfriendsfriends(friends, filmTrust)
    friend_id = np.random.randint(len(friend_s_friends) )
    friends = friends.append(friend_s_friends.loc[[friend_id]], ignore_index=True)
    for i in friend_s_friends.loc[[friend_id]]['user']:
        names[i] = PokemonNames.pop(np.random.randint(len(PokemonNames)))
    return friends

def hangoutfail(friends,deleted_friends):
    friend_id = np.random.randint(len(friends))
    for i in friends.iloc[[friend_id]]['user']:
        names.pop(i)
    deleted_friends = deleted_friends.append(friends.iloc[[friend_id]], ignore_index=True)

    friends = friends.drop(friends.index[friend_id])

    return friends,deleted_friends


def chooseTrainer(minTrustor, maxTrustor):
    possiblerTrainers = []

    for i in range(max(trustTable['trustor']) + 1):
        if len(trustTable[trustTable['trustor'] == i]) >= minTrustor and len(
                trustTable[trustTable['trustor'] == i]) <= maxTrustor:
            possiblerTrainers.append(i)

    trainer = possiblerTrainers[np.random.randint(0, len(possiblerTrainers))]
    return trainer


def calculateIMDB():
    imdbRatings = {}

    for i in range(max(movieRatings['movie']) + 1):
        avgRate = movieRatings[movieRatings['movie'] == i].mean(axis=0)['rating']
        if not np.isnan(avgRate):
            imdbRatings[i] = avgRate
    return imdbRatings


def cal_divergence(lookuprating, userrating):
    dif = abs(lookuprating - userrating)

    if dif >= 2.5: #max 4 min -4
        score = -2 * (dif - 2.5)
    elif dif >= 1.5:
        score = 0
    else:
        score = 2 * (1.5 - dif)

    return score

def calculateImdbDivergence(imdbRatings):
    imdbDivergence = {}

    for i in range(max(trustTable['trustee']) + 1):
        userMovies = movieRatings[movieRatings['user'] == i]
        divergence = 0
        if len(userMovies) > 5:
            for index, row in userMovies.iterrows():
                divTemp = cal_divergence(row['rating'],imdbRatings[int(row['movie'])])#max 3 min -3
                divergence += divTemp
            divergence /= len(userMovies)
            imdbDivergence[i] = divergence
        else:
            imdbDivergence[i] = divergence

    return imdbDivergence


def calculateTrainerDivergence(trainer):
    trainerDivergence = {}

    trainerMovies = movieRatings[movieRatings['user'] == trainer]

    for i in range(max(trustTable['trustee']) + 1):
        if i == trainer:
            trainerDivergence[i] = 0
            continue
        userMovies = movieRatings[movieRatings['user'] == i]
        divergence = 0

        if len(userMovies) > 0:
            for index, row in userMovies.iterrows():
                if len(trainerMovies[trainerMovies['movie'] == row['movie']]) > 0:
                    divTemp = cal_divergence(row['rating'] , list(trainerMovies[trainerMovies['movie'] == row['movie']]['rating'])[0])
                    divergence +=  divTemp

            trainerDivergence[i] = divergence
        else:
            trainerDivergence[i] = 0

    return trainerDivergence


def calculateFilmTrust(normImdbDivergence, normTrainerDivergence):
    filmTrust = {}

    for user, rating in imdbDivergence.items():
        filmTrust[user] = 0.4 * normImdbDivergence[user] + 0.6 * normTrainerDivergence[user]

    return filmTrust


def evalRecMovies(friends, filmTrust):
    recMovieWatchCount = {}
    recMoviePoints = {}

    for index, friend in friends.iterrows():
        for index2, movie in movieRatings[movieRatings['user'] == friend['user']].iterrows():
            if movie['movie'] not in recMoviePoints:
                recMoviePoints[int(movie['movie'])] = friend['trust'] * filmTrust[friend['user']] * movie['rating']
                recMovieWatchCount[int(movie['movie'])] = 1
            else:
                recMoviePoints[int(movie['movie'])] += friend['trust'] * filmTrust[friend['user']] * movie['rating']
                recMovieWatchCount[int(movie['movie'])] += 1

    for movie, rating in recMoviePoints.items():
        recMoviePoints[movie] = rating / recMovieWatchCount[movie]

    return recMoviePoints , recMovieWatchCount


def isConvinced(normRecMoviePoints):
    more3 = 0
    for movie, rating in normRecMoviePoints.items():
        if rating > 0.8:
            return True
        if rating > 0.6:
            more3 += 1
    if more3 > 3:
        return True
    else:
        return False


def chooseCandidates(normRecMoviePoints,votes):
    sortedRMP = [(k, normRecMoviePoints[k]) for k in
                 sorted(normRecMoviePoints, key=normRecMoviePoints.get, reverse=True)]

    trainerMovies = movieRatings[movieRatings['user'] == trainer]
    trainerMovies = list(trainerMovies['movie'])

    sortedRMP = [(movie, rating) for (movie, rating) in sortedRMP if not movie in trainerMovies]

    candidateMovies = []

    maxSRMP = sortedRMP[0][1]
    for srmp in sortedRMP:
        if maxSRMP - srmp[1] <= 0.15:
            candidateMovies.append(srmp)
        else:
            break
    #a = {}
    #newcandidates = []
    #for i in np.transpose(candidateMovies)[0]:
    #    a[votes[i]] = i
    #for i in np.transpose(candidateMovies)[0]:
    #    if(votes[i] == max(a)):
    #        newcandidates.append(candidateMovies[np.where( np.transpose(candidateMovies)[0]== i )[0]])


    return candidateMovies

def choosemovie(newcandidates):

    chosenMovie = newcandidates[np.random.choice(len(newcandidates), 1, p=np.transpose(newcandidates)[1] / np.sum(np.transpose(newcandidates)[1]))[0]]
    return chosenMovie

def finalChoosemovie(normRecMoviePoints, friends, votes):

    if(isConvinced(normRecMoviePoints)):
        return True, choosemovie(chooseCandidates(normRecMoviePoints, votes)), friends
    else:
        friends = friends.append(getfriendsfriends(friends,filmTrust))
        normRecMoviePoints, votes = calc_moviepoints(friends, filmTrust)
        return False, choosemovie(chooseCandidates(normRecMoviePoints, votes)), friends


#trainer = chooseTrainer(10, 15)
trainer = 452

print('trainer is choosen')
print(trainer)


friends = trustTable[trustTable['trustor'] == trainer][['trustee','trust']]
friends.columns = ['user' , 'trust']
for i in friends['user']:
    names[i] = PokemonNames.pop(np.random.randint(len(PokemonNames)))

deleted_friends = pd.DataFrame(columns= ['user' , 'trust'])

print('friends getted')
print(friends)

imdbRatings = calculateIMDB()
imdbDivergence = calculateImdbDivergence(imdbRatings)
trainerDivergence = calculateTrainerDivergence(trainer)


normImdbDivergence = {}


for user, rating in imdbDivergence.items():
    normImdbDivergence[user] = rating/1.5

#maxDiv = abs(max(list(normImdbDivergence.values())))
#for user, rating in normImdbDivergence.items():
#    normImdbDivergence[user] = 4*rating/maxDiv - 2



normTrainerDivergence = {}

#minDiv = abs(min(list(trainerDivergence.values())))
#for user, rating in trainerDivergence.items():
#    normTrainerDivergence[user] = rating + minDiv

#maxDiv = abs(max(list(normTrainerDivergence.values())))
#for user, rating in normTrainerDivergence.items():
#    normTrainerDivergence[user] = 4*rating/maxDiv -2

minDiv = len(movieRatings[movieRatings['user'] == trainer]) * 3
for user, rating in trainerDivergence.items():
    normTrainerDivergence[user] = rating/(minDiv/2)


filmTrust = calculateFilmTrust(normImdbDivergence, normTrainerDivergence)

#friends = hangoutsuccess(friends, filmTrust)

#friends, deleted_friends = hangoutfail(friends, deleted_friends)

def calc_moviepoints (friends,filmTrust):
    recMoviePoints,recMovieWatchCount = evalRecMovies(friends, filmTrust) # min -2 max 2

    #recImdbPoints = {}
    #for movie, rating in recMoviePoints.items():
    #    recImdbPoints[movie] = imdbRatings[movie]
    #    recImdbPoints[movie] = imdbRatings[movie]

    normRecMoviePoints = {}
    for user, rating in recMoviePoints.items():
        normRecMoviePoints[user] = rating/2

    return normRecMoviePoints,recMovieWatchCount


def friendsTab (friends):
    friendsTab = pd.DataFrame(columns=['Name', 'IMDB_AC', 'Trainer_AC', 'Friend_degree' ,'Tot_Trust'])
    k = 0
    for i in names:
        friendsTab.loc[k]= [names[i] , normImdbDivergence[i] ,normTrainerDivergence[i]  , friends[friends['user'] == i].iloc[0,1] , filmTrust[i]]
        k += 1
    friendsTab = friendsTab.sort_values('Friend_degree', ascending=False).sort_values('Tot_Trust', ascending=False)
    return friendsTab

def movieTab (candidateMovies,recMovieWatchCount):
    movieTab = pd.DataFrame(columns=['ID', 'IMDB', 'Calculated' , 'Vote_Count' ])
    k = 0
    movieTab = movieTab.sort_values('Calculated', ascending=False)
    for movie,rating in candidateMovies:
        movieTab.loc[k]= [movie , imdbRatings[movie] , rating , recMovieWatchCount[movie]]
        k += 1
    return  movieTab


#a,b = d.calc_moviepoints(d.friends,d.filmTrust)
#d.movieTab(d.friends,d.chooseCandidates(a),b)
