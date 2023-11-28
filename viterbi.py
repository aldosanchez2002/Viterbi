'''
Viterbi algorithm for Hidden Markov Models
Aldo Sanchez
'''
class hiddenMarkovModel:

    def __init__(
            self, 
            observations: list = [0, 1, 0, 1], 
            transitionsProbabilities: list =    [[0.7, 0.3], 
                                                [0.4, 0.6]], 
            emissionProbabilities: list =   [[0.1, 0.4], 
                                            [0.6, 0.3]], 
            initialProbabilities: list =   [0.6, 0.4]
            ):
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
                    '''
                    curPosibilty value is:
                    The probability of the previous state at the previous time multiplied by
                    The probability of the transition from the previous state to the current state multiplied by
                    The probability of emmiting the current observation
                    '''
                    curPosibilty = viterbiMatrix[prevState][time-1] 
                    curPosibilty *= self.transitionsProbabilities[prevState][state] 
                    curPosibilty *= self.emissionProbabilities[state][observations[time]]
                    # Taking the max means that the paths with lower probabilities will be ignored
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
    model = hiddenMarkovModel() #default values
    model.testViterbi()