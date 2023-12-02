import json
import random
import numpy as np

import matplotlib.pyplot as plt


class Nation:
    def __init__(self, name="DefaultName",
                 governmentType="Democracy",
                 population=500,
                 publicOpinion=0.5,
                 parties=["Labour Party",  # Ecconomically Left
                          "Libertarian Freedom Party",  # Socially Liberal
                          "Green Party",  # Environmentalists
                          "Conservative Party",  # Ecconomicaly Right
                          "Nationalist Party"],  # Socially Authoratitive
                 currentParty=""):

        self.name = name
        self.governmentType = governmentType
        self.population = population
        self.publicOpinion = publicOpinion
        self.parties = parties

        if currentParty == "":
            self.currentParty = random.choice(parties)

        elif currentParty not in parties:
            raise Exception("Chosen current party is not in list of parties")

        else:
            self.currentParty = currentParty

        print("Party created with the following settings:")
        print(self.GetState())

        # Generate party popularity
        # Current party popularity is based on public opinion,
        # the rest is randomly chosen
        self.partyPopularities = [0] * len(self.parties)

        currentPartyIndex = parties.index(self.currentParty)
        self.partyPopularities[currentPartyIndex] = self.publicOpinion

        otherPopularities = np.random.dirichlet(np.ones(len(self.parties) - 1), size=1)[0]
        otherPopularities = list(otherPopularities * (1 - self.publicOpinion))

        for i in range(len(self.parties)):
            if i == currentPartyIndex:
                continue

            chosenPopularity = random.choice(range(0, len(otherPopularities)))
            self.partyPopularities[i] = otherPopularities[chosenPopularity]

            otherPopularities.remove(otherPopularities[chosenPopularity])

    def PlotPartyPie(self):
        fig, ax = plt.subplots()

        ax.pie(self.partyPopularities, labels=self.parties)
        # Pretify the plot

        return fig

    def GetState(self):
        # Return the current state of the nation for display or further processing
        return {
            "name": self.name,
            "governmentType": self.governmentType,
            "population": self.population,
            "publicOpinion": self.publicOpinion
        }

    def SaveState(self, filename):
        # Save the current state to a file
        with open(filename, "w") as file:
            json.dump(self.GetState(), file)

    def LoadState(self, filename):
        # Load the state from a file and update the current instance
        with open(filename, "r") as file:
            data = json.load(file)
            self.name = data["name"]
            self.government_type = data["governmentType"]
            self.population = data["population"]
            self.publicOpinion = data["publicOpinion"]
