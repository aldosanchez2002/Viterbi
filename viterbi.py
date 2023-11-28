'''
Viterbi algorithm for HMM
'''
import numpy as np

class State:
    def __init__(self,str, index: int, emissionProbs: dict):
        self.index = index
        self.emissionProbs = emissionProbs

class hiddenMarkovModel:
    
    def __init__(self, observations: list, transitionsProbabilities: np.array, emissionProbabilities: np.array, initialProbabilities: dict):
        '''
        observations: a list of observations integers
        transitionProbabilities: a matrix of transition probabilities from state i to state j
        emissionProbabilities: a matrix of dictionaries with emission probabilities from state i to observation j
        initialProbabilities: a dict of initial probabilities for each state
        '''
        self.observations = observations
        self.transitionsProbabilities = transitionsProbabilities
        self.emissionProbabilities = emissionProbabilities
        self.initialProbabilities = initialProbabilities
        self.states = len(initialProbabilities)

    def viterbi(self, observations: list):
        viterbiMatrix = np.zeros((self.states, len(observations)))
        '''
        
        '''
        for i in range(self.states):
            '''
            First value is:
            The probability of starting in the first state mulitpleied by 
            The probability of the first emission at that state
            '''
            viterbiMatrix[i][0] = self.initialProbabilities[i] * self.emissionProbabilities[i][observations[0]]
        for time in range(1, len(observations)):
            for state in range(self.states):
                '''
                For each state, we calculate the probability of being in that state at time t
                '''
                prevStatePossibilities = []
                for prevState in range(self.states):
                    '''
                    For each state, we calculate the probability of being in that state at time t
                    '''
                    prevStatePossibilities.append(viterbiMatrix[prevState][time-1] * self.transitionsProbabilities[prevState][state] * self.emissionProbabilities[state][observations[time]])
                viterbiMatrix[state][time] = max(prevStatePossibilities)
        return viterbiMatrix
    
    def test(self):
        print(self.viterbi(self.observations))


def test():
    observations = [0, 1, 0, 1]
    transitionsProbabilities = np.array([[0.7, 0.3], [0.4, 0.6]])
    emissionProbabilities = np.array([{0: 0.1, 1: 0.4}, {0: 0.6, 1: 0.3}])
    initialProbabilities = {0: 0.6, 1: 0.4}
    hmm = hiddenMarkovModel(observations, transitionsProbabilities, emissionProbabilities, initialProbabilities)
    hmm.test()

if __name__ == "__main__":
    test()