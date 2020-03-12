# -*- coding: utf-8 -*-
"""
 
Generate factors for  user-product pairs for each product a user has purchased
in the past 
 
"""


#### OVERVIEW ##############################

## The approach is to generate a 'grid' of user-products pairs and related 
## factors for each product a user has purchased in the past.  
## These will be evaluated by the model to predict which products a user is 
## likely to purchase on his next order, given characteristics of the next
## order such as day_of_week, hour_of_day, and days_since_prior_order
##
## The folowing notation is used for variable names:
##      u : user
##      o : order
##      p : product
##      a : aisle
##      d: department

## Examples: 
##  *   a user-specific value of average day of week (dow) would be denoted:
##            u_avg_dow
##
##  *   a user-product statistic, such as averge position of a product in a 
##      user's cart across multiple orders would be denoted:
##            up_avg_pos_in_cart
##
##
 
############################# Generate Factors  ###############################

## subset (train, test) orders for augmenting with factors ....
orders_train_test = orders[orders.eval_set != 'prior']

## merge normalized prior data parts into work dataframe to be used 
##   as a source for calculating statistics and factors
work = pd.merge(order_products__prior, orders, on='order_id')
work = pd.merge(work, products, on='product_id')

### Generate a 'grid' of user-products ######
# grid base: test/train users/orders...
#....this will be augmented throughout the script 
grid = orders_train_test.copy()


## grid: add user stats : 
#   u_reorderedMean

ugroup = work.groupby('user_id')
ustats = ugroup.agg(u_reorderMean =('reordered', 'mean')).reset_index()

grid = pd.merge(grid, ustats, on='user_id')


## grid: add user/order stats: 
#   uo_totalorders
#   uo_avg_days_between_orders
#   uo_avg_day_of_week
#   uo_avg_hour_of_day

uogroup = orders[orders.eval_set == 'prior'].groupby('user_id')
uostats = uogroup.agg(uo_totalorders = ('order_id', 'count'),
                      uo_avg_days_between_orders = ('days_since_prior_order', 'mean'),
                      uo_avg_day_of_week = ('order_dow', 'mean'),
                      uo_avg_hour_of_day = ('order_hour_of_day', 'mean')
                      )
uostats.reset_index(inplace=True)
 
grid = pd.merge(grid, uostats, on='user_id' )


## grid: add  user/product (up) stats
#   up_avg_pos_in_cart
#   up_order_proportion

upgroup = work.groupby(['user_id', 'product_id'])

uptemp = upgroup.agg(up_avg_pos_in_cart = ('add_to_cart_order', 'mean'),
                     up_order_count = ('reordered', 'count')                 
                     ).reset_index()

uptemp = pd.merge(uptemp, uostats[['user_id', 'uo_totalorders']])
uptemp['up_order_proportion'] = uptemp.up_order_count / uptemp.uo_totalorders
upstats = uptemp.drop(['uo_totalorders', 'up_order_count'], axis=1)

grid = pd.merge(grid, upstats)
del upstats, uptemp


## grid: add product stats
#   p_reorder_proportion
#   p_count

print('* product stats *')

pgroup = order_products__prior.groupby('product_id')
ptemp = pgroup.agg(p_count = ('reordered', 'count'),
                   p_reordered = ('reordered', 'sum') )
ptemp ['p_reorder_proportion'] = ptemp.p_reordered / ptemp.p_count

pstats = ptemp.drop(['p_reordered'], axis=1).reset_index()
pstats.sort_values('p_reorder_proportion')

grid = pd.merge(grid, pstats)  # ,on=product_id


## aisle- specific
#  obtain the aisle_id (and department_id)
#   a_reordered_proportion
#   aisle_id
#   a_count
#   
grid = pd.merge(grid, products.drop('product_name', axis=1))

awork = work[['product_id', 'reordered']]
awork = pd.merge(awork, products.drop('product_name', axis=1))

agroup = awork.groupby('aisle_id')

atemp = agroup.agg(a_count = ('reordered', 'count'),
                   a_reordered = ('reordered', 'sum') )

atemp ['a_reorder_proportion'] = atemp.a_reordered / atemp.a_count

astats = atemp.drop(['a_reordered'], axis=1).reset_index()
#astats.sort_values('a_reorder_proportion')

grid = pd.merge(grid, astats) # on=aisle_id
del astats


###   user product lapsed days 
#       runningdays
##
## calculate days since product was last reordered...use running days backward
## from the order being predicted.

runtemp = orders[['order_id', 'user_id', 'eval_set', 'order_number', 'days_since_prior_order']]
runtemp.sort_values(['user_id', 'order_number'], ascending=False, inplace=True)
runtemp.days_since_prior_order.fillna(0, inplace=True)
runtemp['runningdaytemp'] = runtemp.groupby(['user_id']).days_since_prior_order.cumsum()
runtemp['runningdays'] = runtemp.runningdaytemp - runtemp.days_since_prior_order
 
upowork = work[['user_id', 'product_id', 'order_number']]
# get last order number of the up combo
xuplast = upowork.groupby(['user_id', 'product_id']).order_number.max().reset_index()
xuplast = pd.merge(xuplast, runtemp)
 
grid = pd.merge(grid, xuplast[['user_id', 'product_id','runningdays']], on=['user_id', 'product_id'])


## add label in train data: whether or not product was reordered  
#   label

order_products__train.head()

grid = pd.merge(grid, order_products__train, on=['order_id', 'product_id'], how='left')

grid['label'] = grid['reordered']
grid.label.fillna(value=0, inplace=True)

# these columns have nulls
grid.drop(['reordered'], axis=1, inplace=True)
grid.drop(['add_to_cart_order'], axis=1, inplace=True)
 

### DONE  ###
print('Done with prep. Writing out to file')


## Write grid to file, so we don't have to recreate again
dateTimeObj = datetime.now()
 
timestampStr = dateTimeObj.strftime("%Y%b%d%H%M%S")
#print('Current Timestamp : ', timestampStr)

ipath =   'C:\\Users\\rozoe\\jy\\SpringBoardCapstoneOne\\'  
gridpicklefile = 'grid' + timestampStr + '.pickle'

outfile = ipath + gridpicklefile
with open(outfile, 'wb') as pickle_file:
    pickle.dump(grid, pickle_file)






