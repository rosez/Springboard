# -*- coding: utf-8 -*-
"""
Read data from source files: 

NOTE: you will need to retrieve source files from the competition website, 
since individuals are not allowed to distribute them:

    https://www.kaggle.com/c/instacart-market-basket-analysis/data

"""
import pandas as pd

############################# Read in Data ###############################
path = 'C:\\Users\\rozoe\\jy\\SpringBoardCapstoneOne\\data\\'


aisles = pd.read_csv(path +'aisles.csv')
departments = pd.read_csv(path +'departments.csv')
orders = pd.read_csv(path +'orders.csv')
order_products__prior = pd.read_csv(path +'order_products__prior.csv')
order_products__train = pd.read_csv(path +'order_products__train.csv')
products = pd.read_csv(path +'products.csv')
sample_submission = pd.read_csv(path +'sample_submission.csv')

