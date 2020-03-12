# -*- coding: utf-8 -*-
"""
Split factors in the 'grid' dataFrame into test/train datasets

    First split the data by order_id and then get the associated rows from 
    the factors table.

"""

testsize = 0.2

# fields to drop
fdrop = ['label', 'eval_set', 'order_id']

# extract the "development" data from the competition "test" data
dev_factors = grid[grid.eval_set != 'test']
submission_factors = grid[grid.eval_set == 'test']

# split 'dev' data by orders 
otemp = pd.DataFrame((dev_factors.order_id.unique()), columns=['order_id'])
o_train, o_test = train_test_split(otemp, test_size=testsize, random_state=22)


# Get the data rows for the corresponding test/train orders

X_train = pd.merge(o_train, dev_factors)
y_train = X_train.label
X_train = X_train.drop(fdrop, axis=1)

X_test = pd.merge(o_test, dev_factors)
y_test = X_test.label
X_test = X_test.drop(fdrop, axis=1)
 

#  Get the submission factors

#y_sub = submission_factors.label
X_sub = submission_factors.drop(fdrop, axis=1)




