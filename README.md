# MVChess
This is an offline program to manage chess tournaments. Creating tournaments, manage <br>
players, set ranks, pairs of players for matches.
<br>
##About


#####Architecture of code
The code is Model-View-Controller designed. For details, look at Architecture.png.


#####Algorithm
The algorithm that created pairs is also detailed at Pairs_algorithm.png.


#####Libraries
As demand, the data are saved on a .json at the root of the folder, managed by TinyDB.


##How to install
Before using the program, you must set-up your environment.

#### 1. Clone
You have to clone this project on your system. To do so, type on a terminal :
```
git clone https://github.com/Emericdefay/MVChess.git
```

#### 2. Virtual Environment
Activate your virtual environment at /MVChess. I recommend virtualenv.
```
virtualenv env
```
To activate it, type at /MVChess :
```
source env/scripts/activate
```
#### 3. Libraries
TinyDB is requisite to use this program. To install it, type:
```
pip install -r requirements.txt
```
#### 4. Start
After that, your virtual environment is set. The next time you want to execute <br>
the program, you'll just need to re-activate your virtual environment. <br>
To launch the program, you have to type :
```
python main.py
```
##How to use
#### 1. Help
There are several commands available in this program, at any time you can check them by typing :
```
commands
```
#### 2. Basics usage
Basically, few commands are needed to manage a tournament.
First, you need to create a tournament. So use :
```
new tournament
```
It will ask an ID to give, make sure to give an integer. That will be the ID of this <br> 
tournament. After that, you'll have to give:
- a name
- a place
- date(s)
- number of players
- number of rounds
- the amount of time for each round 
- a description


Then, it will ask you for the players that will play this tournament. <br>
If a player is already recorded in the data base, ID will be enough. <br>
Else, it will ask you:
- a last name
- a first name
- a birthday
- gender
- elo rank


After that, the first round is ready to start.<br>
Once the round is finished, You have to set the results. For that, type:
```
set round
```
It will ask you the ID of the tournament.<br>
After that, you just have to set the results asked on the terminal.
The tournament is now ready to get a new round, so type 
```
new round
```
When everything is up to. It will ask an ID of a tournament.<br>
You can also add a new player to your data base outside of the tournament creation with:
```
new player
```
But you won't be able to add the player to it.
Now, you know how to manage a Chess tournament with this program.
#### 3. Advanced usage
You know how to manage a tournament but you may want to look at previous <br>
tournaments, checking previous results or players' rank.
Before anything, you have to understand the structure of IDs.
- An ID of a tournament is like : "integer_tournament"
- An ID of a round is like : "integer_tournament":"integer_round"
- An ID of a match is like : "integer_tournament":"integer_round":"integer_match"


Because Match BELONG TO Round BELONG TO Tournament. <br>
So if you want to check the match **n°4** of the **second** round of the tournament **3**, <br> 
the ID of this specific match will be : **3:2:4**

So now, when you'll use a function, you'll know what the program needs as an ID.

We can now look at those functions:
###### Checkout all players:
If you want to see every players recorded on this program, you can type:
```
get players -all -alpha
get players -all -rank
```
The flags -alpha/-rank will sort players depending on which flag chosen.
###### Checkout players from a tournament:
If you want check played from a specific tournament, you can type:
```
get players -alpha
get players -rank
```
The flags -alpha/-rank will sort players depending on which flag chosen.
###### Checkout tournament(s):
If you want to see all information from a tournament or all of them, you can type:
```
get tournament -all
get tournament
```
The -all flag will allow you to see each tournaments created.
###### Checkout Round(s):
If you want to see all information from a round or all rounds of a tournament, you can type:
```
get round -all
get round
``` 
The -all flag will allow you to see every rounds from a tournament.
###### Checkout Match(es):
If you want to see all information from a match or all matches of a round, you can type:
```
get match -all
get match
``` 
The -all flag will allow you to see every matches from a round.

#### 4. Other commands
###### Flake8 Report
You can get a flake8 report by typing:
```
get flake-report
```
The report folder will be stored at /MVChess named : "flake8_rapport".
###### Exit the program
If you want to exit softly, you can type:
```
exit
```

#### 5. All commands
```
new tournament
new round
new player

set round
set player

get players -all -alpha
get players -all -rank
get players -alpha
get players -rank

get tournament -all
get tournament

get round -all
get round

get match -all
get match

commands
load
get flake-report
exit
```

## Flake8 report


If you want to create a Flake8 report without execute the program. <br>
You can simply type the followed command on a terminal at the /MVChess path.
```
flake8 --exclude=env,venv --format=html --htmldir=flake8_report --max-line-length=119
```
Please make sure that you virtual environment is named env or venv.
