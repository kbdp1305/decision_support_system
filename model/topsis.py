from model.profile_matching import profile_matching
import numpy as np

class ProfileTopsis() :
    def __init__(self):
        self.profile_matching=profile_matching([1,1,1],[1,1],[1,1,1,1,1],[1,1,1])
        self.criterion=self.profile_matching.compute_final_criterion()
    def normalize_topsis(self):
        squared_criterion=self.criterion.copy()
        for idx,criterion in enumerate(self.criterion) :
            squared_criterion[idx]=self.criterion[idx]**2
        return squared_criterion
    def sum_of_squared_criterion(self):
        sum_of_squared_criterion=[]
        squared_criterion=self.normalize_topsis()
        for idx, criterion in enumerate(squared_criterion) :
            sum_of_squared_criterion.append(np.sum(squared_criterion[idx]))
        return sum_of_squared_criterion
    def normalize_matrix(self):
        criterions=self.criterion.copy()

        sum_of_criterion=self.sum_of_squared_criterion()
        for idx,criterion in enumerate(self.criterion) :
            criterions[idx]=criterions[idx]/sum_of_criterion[idx]
        return criterions
    ## Next job : weighting matrix and do D1+ D1-


