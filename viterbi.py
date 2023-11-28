'''
Viterbi algorithm for Hidden Markov Models
'''
class hiddenMarkovModel:

    def __init__(self, observations: list, transitionsProbabilities: list, emissionProbabilities: list, initialProbabilities: list):
        '''
        obersevations: list of observations
        transitionsProbabilities: list of lists of transition probabilities from state i to state j
        emissionProbabilities: list of lists of emission probabilities from state i to observation j
        initialProbabilities: list of initial probabilities for each state
        '''
        self.observations = observations
        self.transitionsProbabilities = transitionsProbabilities
        self.emissionProbabilities = emissionProbabilities
        self.initialProbabilities = initialProbabilities
        self.states = len(initialProbabilities)
        
    @classmethod
    def buildDefault(self):
        observations =             [0, 1, 0, 1]
        transitionsProbabilities = [[0.7, 0.3], 
                                    [0.4, 0.6]]
        emissionProbabilities =    [[0.1, 0.4], 
                                    [0.6, 0.3]]
        initialProbabilities =     [0.6, 0.4]
        return hiddenMarkovModel(observations, transitionsProbabilities, emissionProbabilities, initialProbabilities)

    def viterbi(self, observations: list):
        viterbiMatrix = [[0 for _ in observations] for j in range(self.states)]
        prevStateMatrix = [[-1 for _ in observations] for j in range(self.states)]
        '''
            First column value is:
            The probability of starting in the first state multiplied by 
            The probability of the first emission at that state
        '''
        for i in range(self.states):
            initialProbToState = self.initialProbabilities[i] * self.emissionProbabilities[i][observations[0]]
            viterbiMatrix[i][0] = initialProbToState
        
        #Fill the matrix by looking for the max probability to that state from the previous column
        for time in range(1, len(observations)):
            for state in range(self.states):
                maxPrevStatePossibility = 0
                for prevState in range(self.states):
                    curPosibilty = viterbiMatrix[prevState][time-1] * self.transitionsProbabilities[prevState][state] * self.emissionProbabilities[state][observations[time]]
                    if curPosibilty > maxPrevStatePossibility:
                        maxPrevStatePossibility = curPosibilty
                        prevStateMatrix[state][time] = prevState
                viterbiMatrix[state][time] = maxPrevStatePossibility
        return self.getPath(viterbiMatrix, prevStateMatrix)
    
    def getPath(self, viterbiMatrix: list, prevStateMatrix: list):
        # Get the max probability from last column
        maxProbability, maxProbabilityIndex = 0, 0
        for index,row in enumerate(viterbiMatrix):
            if row[-1] > maxProbability:
                maxProbability = row[-1]
                maxProbabilityIndex = index
        #Get the path by tracing prevStateMatrix from last column to first column
        path = []
        path.append(maxProbabilityIndex)
        while prevStateMatrix[path[-1]][-len(path)]>-1:
            path.append(prevStateMatrix[path[-1]][len(path)])
        path.reverse()
        return path

    def testViterbi(self):
        print(self.viterbi(self.observations))

if __name__ == "__main__":
    model = hiddenMarkovModel.buildDefault()
    model.testViterbi()