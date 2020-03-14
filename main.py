import random

GOAL_PROBAILITY = 5.3 / 90

class FootballTeam:
    def __init__(self, name, attack = 0.5, defense = 0.5, homeMorale = 0.5, awayMorale = 0.5):
        self.name = name
        self.attack = min(max(attack, 0), 1)
        self.defense =  min(max(defense, 0), 1)
        self.homeMorale =  min(max(homeMorale, 0), 1)
        self.awayMorale =  min(max(awayMorale, 0), 1)

class Match:
    def __init__(self, homeTeam, awayTeam):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.isOver = False
        self.homeGoalTimes = []
        self.awayGoalTimes = []
        self.homeGoals = 0
        self.awayGoals = 0
    
    def run(self):
        self.isOver = True
        if self.homeTeam.homeMorale >= 0.5:
            coff = (self.homeTeam.homeMorale - 0.5) / 0.5
            homeAttack = self.homeTeam.attack * (1 - coff) + coff
            homeDefense = self.homeTeam.defense * (1 - coff) + coff
        else:
            coff = (0.5 - self.homeTeam.homeMorale) / 0.5
            homeAttack = self.homeTeam.attack * (1 - coff)
            homeDefense = self.homeTeam.defense * (1 - coff)
        if self.awayTeam.awayMorale >= 0.5:
            coff = (self.awayTeam.awayMorale - 0.5) / 0.5
            awayAttack = self.awayTeam.attack * (1 - coff) + coff
            awayDefense = self.awayTeam.defense * (1 - coff) + coff
        else:
            coff = (0.5 - self.awayTeam.awayMorale) / 0.5
            awayAttack = self.awayTeam.attack * (1 - coff)
            awayDefense = self.awayTeam.defense * (1 - coff)

        homeForce = homeAttack * (1 - awayDefense)
        awayForce = awayAttack * (1 - homeDefense)
        for i in range(90):
            rd = random.random()
            if rd < homeForce*GOAL_PROBAILITY:
                self.homeGoalTimes.append(i+1)
            rd = random.random()
            if rd < awayForce*GOAL_PROBAILITY:
                self.awayGoalTimes.append(i+1)
        self.homeGoals = len(self.homeGoalTimes)
        self.awayGoals = len(self.awayGoalTimes)


class TeamSessionInfor:
    def __init__(self, footballTeam):
        self.team = footballTeam
        self.matches = []
        self.win = 0
        self.draw = 0
        self.lose = 0
        self.points = 0
        self.goalsFor = 0
        self.goalsAgainst = 0
        self.goalsDiff = 0

    def addMatch(self, match):
        if match.isOver and (self.team.name == match.homeTeam.name or self.team.name == match.awayTeam.name):
            self.matches.append(match)
            if self.team.name == match.homeTeam.name:
                ownGoals = match.homeGoals
                competitorGoals = match.awayGoals
            else:
                ownGoals = match.awayGoals
                competitorGoals = match.homeGoals
            self.goalsFor += ownGoals
            self.goalsAgainst += competitorGoals
            self.goalsDiff = self.goalsFor - self.goalsAgainst
            if ownGoals > competitorGoals:
                self.win += 1
                self.points += 3
            elif ownGoals < competitorGoals:
                self.lose += 1
            else:
                self.draw += 1
                self.points += 1


class FootballSession:
    def __init__(self, footballTeams):
        self.numOfTeams = len(footballTeams)
        self.SessionInfor = {}
        for team in footballTeams:
            self.SessionInfor[team.name] = TeamSessionInfor(team)
        self.isOver = False
        self.matchDoneCount = 0
        self.numOfMatches =  self.numOfTeams * (self.numOfTeams - 1)
        self.matches = []
        self.isEven = (self.numOfTeams % 2 == 0)
        if self.isEven:
            self.numOfRound = self.numOfTeams - 1
        else:
            self.numOfRound = self.numOfTeams
        
        # Create all matches
        pairs = []
        for i in range(self.numOfRound):
            matchedList = []
            for j in range(self.numOfRound):
                if j in matchedList:
                    continue
                k = (self.numOfRound + i - j) % self.numOfRound
                if k == j:
                    if self.isEven:
                        pairs.append((j,self.numOfRound))
                        matchedList.append(j)
                        matchedList.append(self.numOfRound)
                else:
                    pairs.append((j,k))
                    matchedList.append(j)
                    matchedList.append(k)

        indexs = [i for i in range(self.numOfTeams)]
        random.shuffle(indexs)
        shufflePairs1 = [(indexs[p[0]],indexs[p[1]]) for p in pairs]
        random.shuffle(indexs)
        shufflePairs2 = [(indexs[p[0]],indexs[p[1]]) for p in pairs]
        finalPairs = []
        for p in shufflePairs1:
            if p in shufflePairs2:
                finalPairs.append((p[1],p[0]))
            else:
                finalPairs.append(p)
        finalPairs.extend(shufflePairs2)

        for i in range(len(finalPairs)):
            self.matches.append(Match(footballTeams[finalPairs[i][0]], footballTeams[finalPairs[i][1]]))
        
        # for match in self.matches:
        #     print("{} vs {}".format(match.homeTeam.name.ljust(25), match.awayTeam.name.rjust(25)))

    def runMatch(self, numOfMatch = 1):
        for i in range(numOfMatch):
            if not self.isOver:
                self.matches[self.matchDoneCount].run()
                self.SessionInfor[self.matches[self.matchDoneCount].homeTeam.name].addMatch(self.matches[self.matchDoneCount])
                self.SessionInfor[self.matches[self.matchDoneCount].awayTeam.name].addMatch(self.matches[self.matchDoneCount])
                self.matchDoneCount += 1
            if self.matchDoneCount >= self.numOfMatches:
                self.isOver = True

    def printRankings(self):
        sessionInforList = list(self.SessionInfor.values())
        sessionInforList = sorted(sessionInforList, key = lambda x: (x.points, x.goalsDiff, x.goalsFor), reverse = True)
        print("{:<4}{:<24}{:>7}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>7}".format("Pos", "Team's Name", "Played", "Won", "Drawn", "Lost", "GF", "GA", "GD", "Points"))
        for i in range(self.numOfTeams):
            print("{:<4}{:<24}{:>7}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>7}".format(i+1, sessionInforList[i].team.name, len(sessionInforList[i].matches), 
                sessionInforList[i].win, sessionInforList[i].draw, sessionInforList[i].lose, sessionInforList[i].goalsFor, sessionInforList[i].goalsAgainst, 
                sessionInforList[i].goalsDiff, sessionInforList[i].points))

    def printAllMatches(self):
        for i in range(self.matchDoneCount):
            print("{} {} {} - {} {} {}".format(self.matches[i].homeTeam.name, self.matches[i].homeGoals, self.matches[i].homeGoalTimes, 
                                        self.matches[i].awayGoals, self.matches[i].awayGoalTimes, self.matches[i].awayTeam.name))


footballTeams = [FootballTeam("Manchester United", 0.8, 0.7, 0.72, 0.55),
                FootballTeam("Liverpool", 0.9, 0.6, 0.65, 0.5),
                FootballTeam("Manchester City", 0.85, 0.6, 0.65, 0.55),
                FootballTeam("Leicester City", 0.6, 0.7, 0.8, 0.4),
                FootballTeam("Chelsea", 0.5, 0.8, 0.65, 0.5),
                FootballTeam("Wolverhampton", 0.5, 0.6, 0.6, 0.4),
                FootballTeam("Sheffield United", 0.45, 0.65, 0.6, 0.4),
                FootballTeam("Tottenham Hotspur", 0.5, 0.6, 0.7, 0.4),
                FootballTeam("Arsenal", 0.8, 0.5, 0.6, 0.6),
                FootballTeam("Burnley", 0.4, 0.6, 0.5, 0.3),
                FootballTeam("Crystal Palace", 0.4, 0.4, 0.7, 0.4),
                FootballTeam("Everton", 0.5, 0.4, 0.7, 0.3),
                FootballTeam("Newcastle United", 0.4, 0.3, 0.7, 0.3),
                FootballTeam("Southampton", 0.5, 0.3, 0.7, 0.3),
                FootballTeam("Brighton & Hove Albion", 0.2, 0.6, 0.5, 0.3),
                FootballTeam("West Ham United", 0.3, 0.4, 0.5, 0.3),
                FootballTeam("Watford", 0.4, 0.2, 0.7, 0.4),
                FootballTeam("AFC Bournemouth", 0.4, 0.2, 0.5, 0.4),
                FootballTeam("Aston Villa", 0.2, 0.5, 0.5, 0.4),
                FootballTeam("Norwich City", 0.3, 0.3, 0.5, 0.3)]
footballSession = FootballSession(footballTeams)

footballSession.runMatch(10000)
footballSession.printAllMatches()
footballSession.printRankings()



# mu = FootballTeam("Manchester United", 0.5, 0.5, 0.5, 0.5)
# liv = FootballTeam("Liverpool", 0.5, 0.5, 0.5, 0.5)
# match1 = Match(mu, liv)
# match2 = Match(liv, mu)
# match1.run()
# print("{} {} - {} {}".format(match1.homeTeam.name.ljust(25), match1.homeGoals, match1.awayGoals, match1.awayTeam.name.rjust(25)))
# match2.run()
# print("{} {} - {} {}".format(match2.homeTeam.name.ljust(25), match2.homeGoals, match2.awayGoals, match2.awayTeam.name.rjust(25)))