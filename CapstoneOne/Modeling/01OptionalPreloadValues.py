# -*- coding: utf-8 -*-
"""
Optional step to load, rather than generate values during the various steps.

Values and steps produced:
    grid : Generated factors (vs 00ReadData + 20GenerateFactors)
    best_clf : 40hypertune
    best_threshold : 45thresholdTune


"""
#### categorical_features....used in mulitple places
categorical_features=['aisle_id','department_id']


##### grid: #######################################################
##### Read pre-generated factors from pickle file, and assign to variable 'grid'

## code used to generate output filename...
# dateTimeObj = datetime.now()
#timestampStr = dateTimeObj.strftime("%Y%b%d%H%M%S")
#print('Current Timestamp : ', timestampStr)
import pickle

ipath =   'C:\\Users\\rozoe\\jy\\SpringBoardCapstoneOne\\'  
#gridpicklefile = 'grid' + timestampStr + '.pickle'
gridpicklefile = 'grid2020Mar11100511.pickle'

gridpath = ipath + gridpicklefile

with open(gridpath, 'rb') as pickle_file:
    grid = pickle.load(pickle_file)

 
#####  best_clf:  ################################################
#####  Use previously-determined best lgbm model: best_clf
# NOTE: due to limited compute resources, the best parms were 
# base on only 10 iterations of the CV file.  Nonetheless, the parms
# resulted in a Kaggle score of .3772
    
import lightgbm as lgb
 
best_clf = lgb.LGBMClassifier(boosting_type='gbdt', class_weight=None, colsample_bytree=0.6,
               importance_type='split', learning_rate=0.2997421251594704,
               max_depth=7, min_child_samples=270, min_child_weight=0.001,
               min_split_gain=0.0, n_estimators=75, n_jobs=-1, num_leaves=60,
               objective=None, random_state=None, reg_alpha=0.0, reg_lambda=0.0,
               silent=True, subsample=0.9444444444444444,
               subsample_for_bin=280000, subsample_freq=0)   
    

#####  best_threhold:  ################################################
# from module: 45thresholdTune.py

best_threshold = 0.22



#### original parameters used during model development, prior to hyper tuning
## 
## from link:
##    https://www.analyticsvidhya.com/blog/2017/06/which-algorithm-takes-the-crown-light-gbm-vs-xgboost/

train_data=lgb.Dataset(X_train,label=y_train)
param = {'num_leaves':150, 'objective':'binary','max_depth':7,'learning_rate':.05,'max_bin':200}
param['metric'] = ['auc', 'binary_logloss']
## semi 'tuned' learning rate
param['learning_rate'] = [.25]

num_round=50

lgbm=lgb.train(param,train_data,num_round)





