# -*- coding: utf-8 -*-
"""
Create file for Kaggle submission:
 * make predictions
 * reassociate prediction with order_id, since we had excluded it from factors
 * create string of product_ids for submission
"""

## Predict the probabilites
ysubprob = best_clf.predict_proba(X_sub)[:,1]

## Predict the outcome
ysubpred = ysubprob > best_threshold
 
## We had dropped order_id from factors...
## ...associate prediction with order_id via user_id
subtemp = X_sub[['user_id', 'product_id']]
subtemp['ypred'] = ysubpred.astype('int')

## ....retrieve order_id from original grid...
subuo = grid[grid.eval_set == 'test'][['order_id', 'user_id']].drop_duplicates()
subwork = pd.merge(subtemp, subuo )

## get only predicted products
subreorderedtemp = subwork[subwork.ypred == 1][['order_id', 'product_id']]

## generate list, as required by submission
subreorderedtemp.sort_values(['order_id', 'product_id'], ascending=True, inplace=True)
subtemp = subreorderedtemp.groupby(['order_id'])['product_id'].apply(list)
subtemp = pd.DataFrame(subtemp).reset_index()

## make list into string for submission and rename column
subtemp['products'] = subtemp.apply(lambda x : ' '.join(str(elem) for elem in  x['product_id']), axis=1)
subtemp.drop('product_id', inplace=True, axis=1)

## Include orders that did not have reordered items
submission = pd.merge(subuo['order_id'], subtemp, how='left') 
submission.products.fillna('None',inplace=True)

## Sort results and write submission file
submission.sort_values('order_id', inplace=True)
submission.to_excel (r'C:\\Users\\rozoe\\jy\\SpringBoardCapstoneOne\\submission.xlsx', index = None, header=True)




