import pandas as pd
import numpy as np
from database.dataset_generate import generate_dataset
from sklearn.preprocessing import MinMaxScaler

class profile_matching() :
    def __init__(self,criterion_followers, criterion_clubhistory, criterion_seasonstats, crterion_clubfinancial):
        self.dataset=generate_dataset()
        self.list_of_teams=dict(zip(self.dataset['club_id'], self.dataset['club_name']))
        self.criterion_followers=criterion_followers
        self.criterion_clubhistory=criterion_clubhistory
        self.criterion_seasonstats=criterion_seasonstats
        self.criterion_clubfinancial=crterion_clubfinancial
        self.clubfinancial=["market_value","income","expenditure"]
        self.followers=["instagram_followers","twitter_followers","average_attendance"]
        self.clubhistory=["trophies_won","manager_count"]
        self.seasonstats=["goals_scored","goals_against","matches_won","matches_lost","matches_drawn"]
        self.standard_value={
                                0 : 6,
                                1:5.5,
                                -1 : 5,
                                2 : 4.5,
                                -2 : 4.0,
                                3 : 3.5,
                                -3 :3.0,
                                4:2.5,
                                -4:2,
                                5 : 1.5,
                                -5 : 1

                            }
    def normalize_dataset(self):
        data = self.dataset.drop(["club_id","club_name"], axis=1)
        listss=data.columns
        scaler = MinMaxScaler(feature_range=(1,5))
        scaler.fit(data)
        scaled_data = scaler.transform(data)
        self.dataset[listss]=scaled_data
        return self.dataset
    def remake_data(self):
        self.dataset=self.normalize_dataset()
        n_alternatif=len(self.dataset[self.clubfinancial[0]].values)
        clubfinancial=np.array([[0]*len(self.clubfinancial)]*n_alternatif,dtype=float)
        followers = np.array([[0] * len(self.followers)] * n_alternatif,dtype=float)
        clubhistory = np.array([[0] * len(self.clubhistory)] * n_alternatif,dtype=float)
        seasonstats = np.array([[0] * len(self.seasonstats)] * n_alternatif,dtype=float)
        seasonstats = np.array([[0] * len(self.seasonstats)] * n_alternatif,dtype=float)
        list_of_criterion=[clubfinancial,followers,clubhistory,seasonstats]
        list_of_criterion_str=["clubfinancial","followers","clubhistory","seasonstats"]
        for idx,criterion in enumerate(list_of_criterion) :
            for alternatif in range(criterion.shape[0]) :
                for sub_criterion in range(criterion.shape[1]) :
                    attributes = getattr(self, list_of_criterion_str[idx])[sub_criterion]
                    criterion[alternatif][sub_criterion]=self.dataset[attributes].values[alternatif]
        return list_of_criterion,list_of_criterion_str



    def difference_of_criterion(self):
        criterions,list_of_criterion=self.remake_data()
        list_of_criterion_str=["criterion_clubfinancial","criterion_followers","criterion_clubhistory","criterion_seasonstats"]
        for idx, criterion in enumerate (criterions) :
            for alternatif in range(criterion.shape[0]) :
                for sub_criterion in range(criterion.shape[1]) :
                    weights = getattr(self, list_of_criterion_str[idx])[sub_criterion]
                    criterion[alternatif][sub_criterion]=round(criterion[alternatif][sub_criterion]-weights)
        return criterions,list_of_criterion

    def weighting_matrix(self):
        criterions, list_of_criterion=self.difference_of_criterion()
        for idx, criterion in enumerate (criterions) :
            for alternatif in range(criterion.shape[0]) :
                for sub_criterion in range(criterion.shape[1]) :
                    criterion[alternatif][sub_criterion]=self.standard_value[criterion[alternatif][sub_criterion]]
        return criterions,list_of_criterion

    def NCF_NSF(self):
        ncf_clubfinancial=[]
        nsf_clubfinancial=[]
        ncf_clubhistory=[]
        nsf_clubhistory=[]
        ncf_followers=[]
        nsf_followers=[]
        ncf_seasonstats=[]
        nsf_seasonstats=[]
        criterions, list_of_criterion=self.weighting_matrix()
        tampungan=[]
        ncf_t = np.array([[0]*20]*4,dtype=float)
        nsf_t = np.array([[0]*20]*4,dtype=float)
        for idx, criterion in enumerate(criterions):

            for alternatif in range(criterion.shape[0]):
                ncf=[]
                nsf=[]

                for sub_criterion in range(criterion.shape[1]):
                    if idx==0 :
                        if sub_criterion in [0,1] :
                            ncf.append(criterion[alternatif][sub_criterion])
                        else :
                            nsf.append(criterion[alternatif][sub_criterion])
                    elif idx==1 :
                        if sub_criterion in [2]:
                            ncf.append(criterion[alternatif][sub_criterion])
                        else:
                            nsf.append(criterion[alternatif][sub_criterion])
                    elif idx == 2:
                        if sub_criterion in [1]:
                            ncf.append(criterion[alternatif][sub_criterion])
                        else:
                            nsf.append(criterion[alternatif][sub_criterion])
                    elif idx == 3:
                        if sub_criterion in [2,3,4]:
                            ncf.append(criterion[alternatif][sub_criterion])
                        else:
                            nsf.append(criterion[alternatif][sub_criterion])
                ncf_t[idx][alternatif]=np.average(ncf)
                nsf_t[idx][alternatif] = np.average(nsf)
        return  ncf_t,nsf_t

    def compute_final_criterion(self):
        ncf,nsf=self.NCF_NSF()
        final_skor = np.array([[0] * 20] * 4, dtype=float)
        for criterion in range(ncf.shape[0]) :
            for alternatif in range(ncf.shape[1]) :
                final_skor[criterion][alternatif] = ncf[criterion][alternatif]*0.6 + nsf[criterion][alternatif]*0.4
        return final_skor
    def ranking(self):
        final_skor=self.compute_final_criterion()
        final_skors = np.array([0] * 20, dtype=float)
        for idx, criterion in enumerate(final_skor) :
            # print(criterion)

            for alternatif in range(len(criterion)) :
                temp = 0
                if idx==0 :
                    temp+=criterion[alternatif]*0.3
                elif idx == 1 :
                    temp+=criterion[alternatif]*0.3
                elif idx == 2 :
                    temp+=criterion[alternatif]*0.3
                elif idx == 3 :
                    temp+=criterion[alternatif]*0.1
                final_skors[alternatif]+=temp
        result= dict(zip(self.dataset['club_id'], zip(self.dataset['club_name'], final_skors)))
        return dict(sorted(result.items(), key=lambda item: item[1][1],reverse=True))

