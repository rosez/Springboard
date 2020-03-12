# -*- coding: utf-8 -*-
"""
Choose the best threshold to use, based on the the f1-score.

Best threshold is stored in: best_threshold

NOTE: the hyperparameters were tuned using the roc_auc metric.

* the model was trained in previous step on the entire train dataset

"""

#best_clf.fit(X_train, y_train, categorical_feature=categorical_features)

ytrainprob = best_clf.predict_proba(X_train)[:,1]
 
thresharray = np.arange(0.15, 0.5, 0.01)
thresh_list = list(thresharray)

f1array = [] 
for threshold in thresh_list:
    print("Threshold: ", threshold) 
    
    ypred = ytrainprob > threshold

    f1 = f1_score(y_train, ypred)
    f1array.append(f1)
    print('f1 Score: ', f1)


index = np.argmax(f1array)  

best_threshold = thresharray[index]
best_f1 = f1array[index]

plt.scatter(thresharray, f1array)
plt.title('f1 score vs threshold')
plt.xlabel('proba threshold')
plt.ylabel('f1 score')
plt.axvline(best_threshold, color='green')
plt.axhline(best_f1, color='green')
plt.show()

print('Best threshold, f1_score: {t:.3f}, {f:.3f} '.format(t=best_threshold, f=best_f1)  )   
# ==>  Best threshold, f1_score: 0.220, 0.439 
