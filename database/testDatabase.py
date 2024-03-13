from database.crud import Query
from dataset_generate import generate_dataset
from model.profile_matching import profile_matching
# a= Query('Z', 10, 200, 190, 190, 91, 910,
#                      190, 19, 91, 91, 910, 91, 190)
# a.delete()
# a=generate_dataset()

s=profile_matching([1,1,1],[1,1],[1,1,1,1,1],[1,1,1])
a=s.difference_of_criterion()
# print(a[0])
a=s.weighting_matrix()
# print(a[0])
# a=s.compute_final_criterion()
a=s.ranking()
print(a)
# a=s.normalize_dataset()