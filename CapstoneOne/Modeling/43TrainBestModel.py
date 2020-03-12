# -*- coding: utf-8 -*-
"""
Train best model using all train data

"""

# categorical_features=['aisle_id','department_id']
# Since these will change based on random CV, we are recording historical values...
# NOTE: you can also set this in the 001OptionalPreloadValues.py script

'''

# Best_clf with n_iters=2; no categorical_features....
LGBMClassifier(boosting_type='gbdt', class_weight=None, colsample_bytree=0.6,
               importance_type='split', learning_rate=0.38713184134056344,
               max_depth=7, min_child_samples=470, min_child_weight=0.001,
               min_split_gain=0.0, n_estimators=75, n_jobs=-1, num_leaves=140,
               objective=None, random_state=None, reg_alpha=0.0, reg_lambda=0.0,
               silent=True, subsample=0.5, subsample_for_bin=80000,
               subsample_freq=0)


# Best_clf with n_iters = 10, cat True

LGBMClassifier(boosting_type='gbdt', class_weight=None, colsample_bytree=0.6,
               importance_type='split', learning_rate=0.2997421251594704,
               max_depth=7, min_child_samples=270, min_child_weight=0.001,
               min_split_gain=0.0, n_estimators=75, n_jobs=-1, num_leaves=60,
               objective=None, random_state=None, reg_alpha=0.0, reg_lambda=0.0,
               silent=True, subsample=0.9444444444444444,
               subsample_for_bin=280000, subsample_freq=0)

'''


best_clf.fit(X_train, y_train, categorical_feature=categorical_features)



# plot importance diagram
lgb.plot_importance(best_clf)

# **** graph -- use this*** ....writes out pdf...

graph = lgb.create_tree_digraph(best_clf, tree_index=0,filename='best0')
graph.render(view=True)

graph = lgb.create_tree_digraph(best_clf, tree_index=22,filename='best22')
graph.render(view=True)

graph = lgb.create_tree_digraph(best_clf, tree_index=11,filename='best11')
graph.render(view=True)






