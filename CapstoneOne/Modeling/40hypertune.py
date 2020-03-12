# -*- coding: utf-8 -*-
"""
Tune hyperparameters for Light Gradient Boost Model using RandomizedSearchCV()

"""
lgbm = lgb.LGBMClassifier()

categorical_features=['aisle_id','department_id']

# original parms from: !!! denote source here...
# NOTE: Python gave overflow error, when there were too many TOTAL entries in
#  the parameter grid

param_grid = {
    'boosting_type': ['gbdt'],
    'max_depth' : [7],
    'num_leaves': list(range(20, 150, 10)),  
    'learning_rate': list(np.logspace(np.log10(0.05), np.log10(0.5), base = 10, num = 10)),  
    'subsample_for_bin': list(range(20000, 300000, 20000)),   
    'min_child_samples': list(range(20, 500, 50)),
#    'reg_alpha': list(np.linspace(0, 1, 10)),
#    'reg_lambda': list(np.linspace(0, 1,10)),
    'colsample_bytree': list(np.linspace(0.6, 1, 10)),
    'subsample': list(np.linspace(0.5, 1, 10)),
    'n_estimators' : [25, 50, 75]
}    
 

n_iter = 10

cv_clf = RandomizedSearchCV(estimator=lgbm,
                    param_distributions=param_grid,
                    cv=5,
                    n_iter=n_iter,
                    refit=True,
                    return_train_score=False,
                    scoring = 'roc_auc',   # changed from 'accuracy'
#                    scoring = 'f1',   # changed from 'accuracy'
                    random_state=1)


## Perform the parameter search

starttime = time.time() 
cv_clf.fit(X_train, y_train, categorical_feature=categorical_features)
endtime = time.time()
print("Time elapsed: ", endtime - starttime)

## Get the results
results = pd.DataFrame(cv_clf.cv_results_)
best_clf = cv_clf.best_estimator_
cvs = cross_val_score(best_clf, X_train, y_train, cv=5)

best_clf
cvs
results

results.to_csv('resultsRandomf1Iters10.csv')  

 