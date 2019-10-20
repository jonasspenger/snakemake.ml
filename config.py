################################################################################
# author: Jonas Spenger
# date: 07.2018
################################################################################

################################################################################
# DEMO
################################################################################
# use fake data and local cluster
config['demo'] = True

################################################################################
# SGE Dask config
################################################################################
config['SGE_dask'] = {
    'n_workers': 32,
    'queue': 'all.q',
    'walltime': '04:00:00',
    'n_cores': 8,
    'memory': '10G',
    }

################################################################################
# File
################################################################################
# use raw or similar directory (not interim) so that file does not get deleted by cleanup
config['filename'] = 'data/raw/preprocessed.csv'
config['x_cols'] = [1, 2, 3]  # predictor variable column
config['y_col'] = 0  # target variable column

################################################################################
# cross validation
################################################################################
config['cv_repeats'] = 2 # number of repeats

################################################################################
# scorers for reporting results
################################################################################
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer
# which score and perfomance methods to report
config['scorers'] = {
    'accuracy': make_scorer(accuracy_score),
    'precision': make_scorer(precision_score, average='macro'),  # use binary for binary
    'recall': make_scorer(recall_score, average='macro'),
    'f1-score': make_scorer(f1_score, average='macro'),
    }

################################################################################
# grid search
################################################################################
# scorer for the grid search
config['grid_scorer'] = 'accuracy'
# number of folds
config['grid_search_k'] = 2

################################################################################
# classifier
################################################################################
config['clf'] = []
config['param_grid'] = []

# Gradient Boosting
# import classifier
from sklearn.ensemble import GradientBoostingClassifier
# set which classifier to use
config['clf'].append(GradientBoostingClassifier())
# define the parameter grid over which to perform the grid search
config['param_grid'].append({
    'learning_rate': [0.01, 0.1],
    'n_estimators': [50, 100],
    # 'max_depth': [3, 5],
    })

# Logistic Regression
from sklearn.linear_model import LogisticRegression
config['clf'].append(LogisticRegression())
config['param_grid'].append({
    'C': [10, 1.0, 0.1, 0.01, 0.001],
    'tol': [0.1 ** i for i in range(4)],
    # 'fit_intercept': [True, False],
    # 'solver': ['liblinear', 'newton-cg', 'saga'],
    'multi_class': ['ovr'],
    'class_weight': ['balanced'],  # deal with class imbalance of dataset
    })

# Random Forest
from sklearn.ensemble import RandomForestClassifier
config['clf'].append(RandomForestClassifier())
config['param_grid'].append({
    # 'n_estimators': [10, 20],
    # 'criterion': ['gini', 'entropy'],
    # 'max_features': ['auto', 1.0],
    # 'max_depth': [None, 2],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 5, 10],
    'class_weight': ['balanced'],  # deal with class imbalance of dataset
    })

# # SVM
# from sklearn.svm import SVC
# config['clf'].append(SVC(probability=True))
# config['param_grid'].append({
#     'C': [10, 1.0, 0.1, 0.01],
#     'kernel': ['linear', 'rbf'],
#     'tol': [0.1 ** i for i in range(4)],
#     })
