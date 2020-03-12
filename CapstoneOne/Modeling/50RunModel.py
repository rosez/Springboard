# -*- coding: utf-8 -*-
"""
Run the trained model with the hold out 'test' data and calculate F1 score
NOTE: this is not the competition test data (which we call 'submission' data),
since we do not have labels for that. 
"""

# best_threshold = 0.22

# Calculate stats on hold out "test" data 

ytestprob = best_clf.predict_proba(X_test)[:,1]

ytestpred = ytestprob > best_threshold

f1Test = f1_score(y_test, ytestpred)

print('f1 Test Score: ', f1Test)

