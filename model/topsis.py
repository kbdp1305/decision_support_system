from model.profile_matching import profile_matching
import numpy as np

class ProfileTopsis() :
    def __init__(self):
        self.profile_matching=profile_matching([5,5,4],[5,5],[4,4,4,5,5],[4,4,4])
        self.criterion,self.dataset=self.profile_matching.compute_final_criterion()
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

    def weighting_matrix(self,weights=[0.3,0.3,0.3,0.1]):
        normalized_matrix=self.normalize_matrix()
        final_weighted_matrix=normalized_matrix.copy()
        for idx,criterion in enumerate(normalized_matrix) :
            final_weighted_matrix[idx]= normalized_matrix[idx]*weights[idx]
        return final_weighted_matrix

    def calculate_ideal_score(self):
        weighted_matrix=self.weighting_matrix()
        """
       clubfinancial = benefit,followers = benefit,clubhistory = benefit,seasonstats = benefit
        """
        ideal_positif=[np.max(weighted_matrix[0]),np.max(weighted_matrix[1]),np.max(weighted_matrix[2]),np.max(weighted_matrix[3])]
        ideal_negatif=[np.min(weighted_matrix[0]),np.min(weighted_matrix[1]),np.min(weighted_matrix[2]),np.min(weighted_matrix[3])]
        return ideal_positif,ideal_negatif

    def calcualte_d_score(self):
        ideal_positif,ideal_negatif=self.calculate_ideal_score()
        final_weighted_matrix=self.weighting_matrix()
        dplus_crit=final_weighted_matrix.copy()
        dminus_crit=final_weighted_matrix.copy()

        for idx,criterion in enumerate(final_weighted_matrix) :
            for alternatif in range(len(criterion)) :
                dplus_crit[idx][alternatif]=pow(ideal_positif[idx]-criterion[alternatif],2)
                dminus_crit[idx][alternatif]=pow(criterion[alternatif]-ideal_negatif[idx],2)
        dplus=np.sqrt(dplus_crit[0]+dplus_crit[1]+dplus_crit[2]+dplus_crit[3])
        dminus=np.sqrt(dminus_crit[0]+dminus_crit[1]+dminus_crit[2]+dminus_crit[3])
        return dplus,dminus

    def calculate_preferences(self):
        dplus,dminus = self.calcualte_d_score()
        preferences=[]

        for alternatif in range(len(dplus)) :
            V=dminus[alternatif]/(dminus[alternatif]+dplus[alternatif])
            preferences.append(V)
        # print(preferences)
        return preferences

    def ranking(self):
        preferences=self.calculate_preferences()
        result=dict(zip(self.dataset['club_id'], zip(self.dataset['club_name'], preferences)))
        return dict(sorted(result.items(), key=lambda item: item[1][1],reverse=True))









