
# coding: utf-8

# In[811]:

import string
import pandas as pd
import random
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec
import time as ttime
from pandas.tools.plotting import table
import numpy as np
import numpy.matlib
from matplotlib import colors as mcolors
import SquirtleAgent as Sqrtle

friends = Sqrtle.friendsTab(Sqrtle.friends)
points,votes = Sqrtle.calc_moviepoints(Sqrtle.friends,Sqrtle.filmTrust)
movie = Sqrtle.chooseCandidates(points,votes)
watched = {}
for key, value in movie:
	watched[key] = ''
	aa = Sqrtle.movieRatings[Sqrtle.movieRatings['movie'] == key]
	for f in Sqrtle.friends['user']:
		if len(aa[aa['user'] == f]) > 0:
			watched[key] += Sqrtle.names[f] + ', '
    	
movies = Sqrtle.movieTab(movie,watched)
choosenmovie = Sqrtle.choosemovie(movie)

input("Press [enter] to continue.")
# In[812]:

eventSchedule = pd.read_csv('Events.txt', sep=';')
eventSchedule


# In[813]:

beliefs = eventSchedule[eventSchedule['isPlanned'] == 1]
beliefs


# In[814]:

events = eventSchedule[eventSchedule['isPlanned'] == 0]
events


# In[815]:

desireSchedule = pd.read_csv('Desires.txt', sep=';')
desireSchedule.set_index(keys='id',drop=False,inplace=True)
desireSchedule


# In[816]:

randomDesires = pd.read_csv('randomDesires.txt', sep=';')
randomDesires.set_index(keys='id',drop=False,inplace=True)
randomDesires



# In[819]:
#########################################################################################################

def create_templete(eventsTab):
    event = 'Her Sey Cok Guzel Olacak'

    beliefsTab = pd.DataFrame(data = np.matlib.repmat('trusted friends ',1,5),columns=['Name', 'IMDB_AC', 'Trainer_AC', 'Friend_degree' ,'Tot_Trust'] )
    desiresTab = pd.DataFrame(data = np.matlib.repmat('trust ',2,4), columns=['ID', 'IMDB', 'Calculated' , 'Vote_Count' ] )
    intentTab= pd.DataFrame(data = np.matlib.repmat('  ',1,15), columns=['8', '9', '10' , '11' , '12' ,'13', '14', '15' , '16' , '17' , '18' , '19' , '20' ,'21' ,'22'] )


    #print(tabulate(df,headers="keys",tablefmt="psql"))

    # yellow = mcolors.BASE_COLORS['y']
    # white = mcolors.BASE_COLORS['w']
    # pattern = np.asarray([ white , yellow])
    # rep = np.matlib.repeat(pattern,int((events.values.shape[1])/2),events.values.shape[0] )
    # print (rep)

    #cellColours = rep,

    ax_event.axis('tight')
    ax_event.axis('off')
    event_table = ax_event.table(bbox = [0,0,1,1],colLabels=eventsTab.columns,cellText=pd.DataFrame.as_matrix(eventsTab), rowLabels=list(eventsTab.index),loc = 'center', fontsize=15 )
    ax_event.set_title(event,fontsize=30)
    #event_table.scale(1.2,1.8)


    ax_belief.axis('tight')
    ax_belief.axis('off')
    belief_table = ax_belief.table(bbox = [0,-0.3,1,1.5],colLabels=beliefsTab.columns,cellText=pd.DataFrame.as_matrix(beliefsTab),loc = 'center' )
    #table.scale(1,4)
    #ax_belief.set_title('Trusted Friends',fontsize=20)
    #belief_table.scale(1.2,1.8)


    ax_desire.axis('tight')
    ax_desire.axis('off')
    desire_table = ax_desire.table(bbox = [0,-0.3,1,1.5], colLabels= desiresTab.columns , cellText=pd.DataFrame.as_matrix(desiresTab),loc = 'center' )
    #ax_desire.set_title('Top 10 movies',fontsize=20)
    #desire_table.scale(1.2,1.8)

    #fig, axs =plt.subplots(2,2)
    #axs[0,0].axis('tight')
    #axs[0,0].axis('off')

    ax_intent.axis('tight')
    ax_intent.axis('off')
    intent_table = ax_intent.table(bbox=[0, 0, 1, 1] ,  colLabels = intentTab.columns , cellText=pd.DataFrame.as_matrix(intentTab) ,loc = 'center', fontsize=15)
    #ax_intent.set_title('intentions', fontsize=20)

    plt.ion()
    plt.show()
    plt.draw()
    plt.pause(0.001)



def update_figure(eventsTab,event,friends,movies,intention,choosenmovie,tdeh):

    patternDesire = np.array([['w']*(len(movies)) , ] *4).transpose()
    patternDesire[movies[movies['ID'] == choosenmovie[0]].index.values[0],:] = 'c'

    
    global patternBelief
    patternBelief = np.array([['w']*(15), ]*7).transpose()

    if len(friends) == 0:
        ax_belief.clear()
        ax_belief.axis('off')
        beliefsTab = pd.DataFrame(data = np.matlib.repmat(' ',1,5), columns=['Name', 'IMDB_AC', 'Trainer_AC', 'Friend_degree' ,'Tot_Trust'] , index = [3])
        belief_table = ax_belief.table(bbox = [0,-0.3,1,1.5],colLabels=beliefsTab.columns,cellText=pd.DataFrame.as_matrix(beliefsTab),loc = 'center', fontsize=15 )
        #ax_belief.set_title("I dont have any friends :(",fontsize=20)

    if len(friends) > 0:
        friends = friends[['Name', 'IMDB_AC', 'Trainer_AC', 'Friend_degree' ,'Tot_Trust']]
        friends
        #global patternBelief
        #patternBelief = np.array([['w']*(15), ]*7).transpose()
        ax_belief.clear()
        ax_belief.axis('off')
        belief_table = ax_belief.table(bbox = [0,-0.3,1,1.5],colLabels=friends.columns,cellText=pd.DataFrame.as_matrix(friends), loc='center', fontsize=15)
        #ax_belief.set_title('My Trusted Friends',fontsize=20)
    #belief_table.scale(1.2,1.8)


    if len(movies) > 0:
        print(len(movies))
        ax_desire.clear()
        ax_desire.axis('off')
        desire_table = ax_desire.table(cellColours = patternDesire, bbox = [0,-0.3,1,1.5], colLabels=movies.columns, cellText=pd.DataFrame.as_matrix(movies), loc='center', fontsize=15)
        #ax_desire.set_title('Movies to go',fontsize=20)

    if(intention):
        patternIntention = patternBelief
        eventsTab.loc[tdeh[0],tdeh[1]] = intention
        patternIntention[tdeh[0]-8,tdeh[1]-15] = 'm'
        ax_event.clear()
        ax_event.axis('off')
        event_table = ax_event.table(cellColours = patternIntention, bbox = [0,0,1,1], colLabels=eventsTab.columns, cellText=pd.DataFrame.as_matrix(eventsTab), rowLabels=list(eventsTab.index), loc='center')
        #event_table.scale(1.2,1.8)
        ax_intent.clear()
        ax_intent.axis('off')
        ax_intent.set_title('Daily intentions',fontsize=20)
        pd.DataFrame.as_matrix(eventsTab)
        k = np.transpose(pd.DataFrame.as_matrix(eventsTab))[tdeh[1] - 15]
        k.shape = (15,1)
        k = k.transpose()
        patternIntention
        c = np.transpose(patternIntention)[tdeh[1]-15]
        c.shape = (15, 1)
        c = c.transpose()
        intent_table = ax_intent.table(cellColours = c, bbox = [0,0,1,1], colLabels=['8', '9', '10' , '11' , '12' ,'13', '14', '15' , '16' , '17' , '18' , '19' , '20' ,'21' ,'22'] , cellText= k , loc='center', fontsize=15)
    if(event):
        ax_event.set_title(event,fontsize=30)
        ax_intent.set_title(event,fontsize=30)
    plt.draw()
    plt.pause(0.001)


fig = plt.figure(figsize=(30,35))
fig2 = plt.figure(figsize=(30,35))

eventsTab = pd.DataFrame(data = np.matlib.repmat(' ',15,7),columns= np.arange(15,22) , index = np.arange(8,23))
gs = GridSpec(3, 2)  # 2 rows, 2 columns
gs2 = GridSpec(5, 2)  # 2 rows, 2 columns
ax_event = fig.add_subplot(gs[:2, :])  # First row, first column
ax_belief = fig2.add_subplot(gs2[:3, 0])  # First row, second column
ax_desire = fig2.add_subplot(gs2[:3, 1])  # First row, third column
ax_intent = fig2.add_subplot(gs2[4, :])  # First row, third column
create_templete(eventsTab)

#update_figure(eventsTab,'alp',None,None,None)
#eventsTab.loc[9,20] = "GoingConference"
#ax_event.clear()
#ax_event.axis('off')
#event_table = ax_event.table(colLabels=eventsTab.columns, cellText=pd.DataFrame.as_matrix(eventsTab), rowLabels=list(eventsTab.index), loc='center')
#event_table.scale(1.2,1.8)
#update_figure(eventsTab,'LPA',None,None,None)

input("Press [enter] to continue.")



################################################################################################


def planTheDay(date):
    desires = pd.DataFrame()
    todayDesires = list(beliefs[beliefs['date'] == date]['newDesires'])
    if len(todayDesires) != 0:
        for tds in todayDesires:
            for td in tds.split(','):
                desires = desires.append(desireSchedule[desireSchedule['id'] == int(td)])
        return desires.sort_values('time') 
    else:
        return desires

def eventHappening(currentEvent, beliefs, desires,date):
    for nb in list(currentEvent['newBeliefs'])[0].split(','):
        if int(nb) == 0:
            break
        beliefs = beliefs.append(eventSchedule[eventSchedule.id == int(nb)])
        if int(eventSchedule[eventSchedule.id == int(nb)]['date']) == int(date):
            newDesires = list(eventSchedule[eventSchedule.id == int(nb)]['newDesires'])
            if len(newDesires) != 0:
                for nds in newDesires:
                    for nd in nds.split(','):
                        desires = desires.append(desireSchedule[desireSchedule['id'] == int(nd)])
                
    for ob in list(currentEvent['oldBeliefs'])[0].split(','):
        if int(ob) == 0:
            break
        eventsTab.loc[beliefs[beliefs.id == int(ob)]['time'],beliefs[beliefs.id == int(ob)]['date']] = ''
        beliefs = beliefs[beliefs.id != int(ob)]
    for nd in list(currentEvent['newDesires'])[0].split(','):
        if int(nd) == 0:
            break
        desires = desires.append(desireSchedule[desireSchedule.id == int(nd)])
    for od in list(currentEvent['oldDesires'])[0].split(','):
        if int(od) == 0:
            break
        desires = desires[desires.id != int(od)]
    
    return beliefs, desires
        
def realizeDesire(desires,beliefs,time,date,energy,hunger):
    currentDesire = desires[desires.time == time]
    if len(currentDesire) > 1:
        print("WOWOWOWOWOWOWOWOWOWOWOWOOWOWOWOWOWOWOWOWOWOWOWOWO")
    if len(currentDesire) != 0:
        cid = int(currentDesire['id'])
        dname = str(list(currentDesire['name'])[0])

        update_figure(eventsTab,str(list(currentDesire['intentionName'])[0]), friends, movies, dname, choosenmovie, [time,date,energy,hunger])
        

        if dname == "Pokemon" and random.random() > 0.7:
            print()
            print("################################################")
            print("Rocket Team Attack Interrupted the Pokemon Hunt and Hurt You")
            print("################################################")
            print()
            desires = desires[desires.id != cid]
            energy -= 2

            update_figure(eventsTab,"Rocket Team Attack Interrupted the Pokemon Hunt and Hurt You",friends,movies,"Team Rocket Attack",choosenmovie,[time,date,energy,hunger])
            return desires, energy, hunger
        elif dname == "Hangout" and random.random() > 0.7:
            print()
            print("################################################")
            print("Your Friends Forget the Meeting, So sad...")
            print("################################################")
            print()
            desires = desires[desires.id != cid]
            energy -= 1

            update_figure(eventsTab, "Your Friends Forget the Meeting, So sad...", friends, movies,
                          "Friends Forgot Meeting", choosenmovie, [time, date, energy, hunger])

            input("Press [enter] to continue.")

            global friends,movies,choosenmovie

            Sqrtle.friends,Sqrtle.deleted_friends = Sqrtle.hangoutfail(Sqrtle.friends,Sqrtle.deleted_friends)
            friends = Sqrtle.friendsTab(Sqrtle.friends)
            points, votes = Sqrtle.calc_moviepoints(Sqrtle.friends, Sqrtle.filmTrust)
            movie = Sqrtle.chooseCandidates(points, votes)

            watched = {}
            for key, value in movie:
            	watched[key] = ''
            	aa = Sqrtle.movieRatings[Sqrtle.movieRatings['movie'] == key]
            	for f in Sqrtle.friends['user']:
            		if len(aa[aa['user'] == f]) > 0:
            			watched[key] += Sqrtle.names[f] + ', '


            movies = Sqrtle.movieTab(movie,watched)
            choosenmovie = Sqrtle.choosemovie(movie)

            update_figure(eventsTab,"Your Friends Forget the Meeting, So sad...",friends,movies,"Friends Forgot Meeting",choosenmovie,[time,date,energy,hunger])


            return desires, energy, hunger
        elif dname == "Meeting Friends":
            print()
            print("################################################")
            print("Decided to Go Van Gogh Museum While Friend Meeting")
            print("################################################")
            print()
            input("Press [enter] to continue.")

            global friends,movies,choosenmovie
            Sqrtle.friends = Sqrtle.hangoutsuccess(Sqrtle.friends,Sqrtle.filmTrust)
            friends = Sqrtle.friendsTab(Sqrtle.friends)
            points, votes = Sqrtle.calc_moviepoints(Sqrtle.friends, Sqrtle.filmTrust)
            movie = Sqrtle.chooseCandidates(points, votes)
            watched = {}
            for key, value in movie:
            	watched[key] = ''
            	aa = Sqrtle.movieRatings[Sqrtle.movieRatings['movie'] == key]
            	for f in Sqrtle.friends['user']:
            		if len(aa[aa['user'] == f]) > 0:
            			watched[key] += Sqrtle.names[f] + ', '

            movies = Sqrtle.movieTab(movie,watched)
            choosenmovie = Sqrtle.choosemovie(movie)

            update_figure(eventsTab,"Decided to Go Van Gogh Museum While Friend Meeting",friends, movies,"Decided Van Gogh",choosenmovie,[time,date,energy,hunger])
        elif dname == "Museum" or dname == "Art Gallery" or dname == "Exhibition" and random.random() > 0.7:
            print()
            print("################################################")
            print("The Event Has Been Cancelled, It Happens :(")
            print("################################################")
            print()
            desires = desires[desires.id != cid]
            energy -= 1

            update_figure(eventsTab, "The Event Has Been Cancelled, It Happens :( ", friends, movies,  dname+ "Cancelled",choosenmovie,[time,date,energy,hunger])
            return desires, energy, hunger



        if(dname == "Go To Movie"):
            input("Press [enter] to continu"
                  "e.")
            global friends,movies,choosenmovie
            friends = Sqrtle.friendsTab(Sqrtle.friends)
            points, votes = Sqrtle.calc_moviepoints(Sqrtle.friends, Sqrtle.filmTrust)
            movie = Sqrtle.chooseCandidates(points, votes)
            watched = {}
            for key, value in movie:
            	watched[key] = ''
            	aa = Sqrtle.movieRatings[Sqrtle.movieRatings['movie'] == key]
            	for f in Sqrtle.friends['user']:
            		if len(aa[aa['user'] == f]) > 0:
            			watched[key] += Sqrtle.names[f] + ', '

            movies = Sqrtle.movieTab(movie,watched)
            convinced, choosenmovie, Sqrtle.friends = Sqrtle.finalChoosemovie(points, Sqrtle.friends, votes)

            if not convinced:
            	friends = Sqrtle.friendsTab(Sqrtle.friends)
            	points, votes = Sqrtle.calc_moviepoints(Sqrtle.friends, Sqrtle.filmTrust)
            	movie = Sqrtle.chooseCandidates(points, votes)
            	watched = {}
            	for key, value in movie:
            		watched[key] = ''
            		aa = Sqrtle.movieRatings[Sqrtle.movieRatings['movie'] == key]
            		for f in Sqrtle.friends['user']:
            			if len(aa[aa['user'] == f]) > 0:
            				watched[key] += Sqrtle.names[f] + ', '
            	movies = Sqrtle.movieTab(movie,watched)

            if convinced:
            	update_figure(eventsTab, "You Chose the Movie: " + str(choosenmovie), friends, movies, "Movie: " + str(choosenmovie), choosenmovie, [time, date, energy, hunger])
            else:
           		update_figure(eventsTab, "You are not convinced and asked friends' friends and chose the movie: " + str(choosenmovie), friends, movies, "Movie: " + str(choosenmovie), choosenmovie, [time, date, energy, hunger])

            input("Press [enter] to continue.")

        if(dname == "Hangout"):
            input("Press [enter] to continu"
                  "e.")
            global friends,movies,choosenmovie
            Sqrtle.friends= Sqrtle.hangoutsuccess(Sqrtle.friends,Sqrtle.filmTrust)
            friends = Sqrtle.friendsTab(Sqrtle.friends)
            points, votes = Sqrtle.calc_moviepoints(Sqrtle.friends, Sqrtle.filmTrust)
            movie = Sqrtle.chooseCandidates(points, votes)

            watched = {}
            for key, value in movie:
            	watched[key] = ''
            	aa = Sqrtle.movieRatings[Sqrtle.movieRatings['movie'] == key]
            	for f in Sqrtle.friends['user']:
            		if len(aa[aa['user'] == f]) > 0:
            			watched[key] += Sqrtle.names[f] + ', '

            movies = Sqrtle.movieTab(movie,watched)
            choosenmovie = Sqrtle.choosemovie(movie)
        print()
        print("################################################")
        print("I am now " + str(list(currentDesire['intentionName'])[0]))
        print("################################################")
        print()
        energy += float(currentDesire['energy'])
        desires.loc[desires.id == cid, 'hour'] = desires.loc[desires.id == cid, 'hour'] - 1
        if int(desires[desires.id == cid]['hour']) == 0:
            desires = desires[desires.id != cid]
        desires.loc[desires.id == cid, 'time'] = desires.loc[desires.id == cid, 'time'] + 1
        
        if dname == 'Food' or dname == 'Lunch' or dname == 'Dinner':
            hunger = 0
        
            
    return desires, energy, hunger
    
    
#def tryRandomPriorDesires():
#    if time <= 16 and remTime >= 2 and energy >= 4 and hunger <= 6

def tryRandomDesires(desires,beliefs,date,time,energy,hunger,remTime):
    while(True):
        rnd = random.randint(randomDesires.iloc[0]['id'],randomDesires.iloc[len(randomDesires)-1]['id'])
        currentDesire = randomDesires[randomDesires.id == rnd]
        dhour = int(currentDesire['hour'])
        denergy = float(currentDesire['energy'])
        dname = str(list(currentDesire['name'])[0])
        
        print("I randomly chose " + str(dname))
        
        if date == 16 and time < 12 and dhour > 1:
            continue
        if hunger <= 5 and dname == "Food":
            continue
        if dname == 'Conference' and (time < 10 or time > 18) and (date < 16 or date > 20):
            continue
        if energy + denergy <= 2:
            continue
        if dhour > remTime:
            continue
        
        print("Succedeed ++++++++++++++++++++")
        print()
        
        currentDesire.loc[currentDesire.id == rnd, 'date'] = date
        currentDesire.loc[currentDesire.id == rnd, 'time'] = time
        desires = desires.append(currentDesire)
        break
        
    desires, energy, hunger = realizeDesire(desires,beliefs,time,date,energy,hunger)
    return desires, energy, hunger

def goodBadRandomDesires(desires,date,time,energy,hunger,remTime):
    badDesires = pd.DataFrame()
    goodDesires = pd.DataFrame()

    for index, row in randomDesires.iterrows():
        did = int(row['id'])
        dhour = int(row['hour'])
        denergy = float(row['energy'])
        dname = str(list(row['name'])[0])

        if dname == "Food" and hunger <= 5:
            badDesires = badDesires.append(row)
            continue
        if dname == 'Conference' and (time < 10 or time > 18) and (date < 16 or date > 20):
            badDesires = badDesires.append(row)
            continue
        if energy + denergy <= 2:
            badDesires = badDesires.append(row)
            continue
        if dhour > remTime:
            badDesires = badDesires.append(row)
            continue
        goodDesires = goodDesires.append(row)

    return badDesires, goodDesires

# In[807]:
patternBelief = np.array([['w']*(15), ]*7).transpose()
desires = pd.DataFrame()
badDesires = pd.DataFrame()
goodDesires = pd.DataFrame()
hunger = 0
energy = 10
for date in range(15, 22):
    for time in range(8, 23):
        energy = min(10, energy)
        hunger = max(0, hunger)
        
        print()
        print()
        print("Date: " + str(date) + ' - ' + "Time: " + str(time))
        print()
        print("Energy: " + str(energy) + ' - ' + "Hunger: " + str(hunger))
        print()
        
        
        
        #print(desires)
        print("BELIEFS")
        if len(beliefs) != 0:
            beliefs = beliefs.sort_values('time').sort_values('date')
            
        print(beliefs)
        
        print()
        
        if time == 8:
            desires = planTheDay(date)
            energy = 10
            hunger = 0
            print()
            print("################################################")
            print("Wake up to a beautiful day with breakfast!")
            print("################################################")
            print()
            print("DESIREES")
            print(desires)

            update_figure(eventsTab,"Wake up to a beautiful day with breakfast!",friends, movies,"Wake Up",choosenmovie,[time,date,energy,hunger])
            if date == 15:
                input("Press [enter] to continue.")
            continue
        if time == 22:
            print("################################################")
            print("Time to sleep sweetheart")
            print("################################################")
            print()

            update_figure(eventsTab,"Time to sleep sweetheart",friends, movies,"Sleep",choosenmovie,[time,date,energy,hunger])
            # Sleep
            continue
        if date == 21 and time == 16:
            print("################################################")
            print("At Home - The End")
            print("################################################")

            update_figure(eventsTab,"At Home - The End",friends, movies,"The End",choosenmovie,[time,date,energy,hunger])
            print()
            break

        hunger += 1
        energy -= 0.5
        
        beliefs = beliefs[(beliefs.date > date) | (eventSchedule.time > time)]
            
        currentEvent = events[events['date'] == date][events['time'] == time]
        if len(currentEvent) != 0:
            print()
            print("################################################")
            print('Event ' + str(list(currentEvent['name'])[0]) + ' is happening')
            print("################################################")
            print()
            beliefs, desires = eventHappening(currentEvent, beliefs, desires, date)
            if len(desires) != 0:
                desires.sort_values('time')
                print(desires)
            if len(beliefs) != 0:
                beliefs = beliefs.sort_values('time').sort_values('date')
                print(beliefs)

            update_figure(eventsTab,str(list(currentEvent['name'])[0]),friends, movies,[],choosenmovie,[time,date,energy,hunger])
        
        
        print("DESIREES")
        if len(desires) != 0:
            desires = desires.sort_values('time')
        print(desires)
        
        if len(desires) != 0 and len(desires[desires.time == time]) != 0:
            desires, energy, hunger = realizeDesire(desires,beliefs,time,date,energy,hunger)
        else:
            if hunger >= 6 and (hunger+1) >= random.random()*10:
                currentDesire = randomDesires[randomDesires.name == "Food"]
                cid = int(currentDesire['id'])
                currentDesire.loc[currentDesire.id == cid, 'date'] = date
                currentDesire.loc[currentDesire.id == cid, 'time'] = time
                desires = desires.append(currentDesire)
                desires, energy, hunger = realizeDesire(desires,beliefs,time,date,energy,hunger)
            else:
                if len(desires) != 0:
                    nextDesire = desires[desires.date == date][desires.time > time]
                    remTime = nextDesire.loc[nextDesire['time'].idxmin()]['time'] - time
                else:
                    remTime = 22-time
                    
                #if randomPriorDesires not empty:
                #    tryRandomPriorDesires()
                #else:
                desires, energy, hunger = tryRandomDesires(desires,beliefs,date,time,energy,hunger,remTime)

        update_figure(eventsTab,None,friends, movies,[],choosenmovie,[time,date,energy,hunger])

input("Press [enter] to continue.")


