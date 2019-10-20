################################################################################
# author: Jonas Spenger
# date: 07.2018
################################################################################

import pickle
import dask.array
from scripts.start_SGE_dask_cluster import start_SGE_dask_cluster
from dask import compute
from dask.delayed import delayed
from dask_ml.model_selection import ShuffleSplit
from dask_ml.model_selection import GridSearchCV
from dask_ml.model_selection._split import _blockwise_slice
from sklearn.model_selection._validation import _multimetric_score
from sklearn.base import clone


@delayed
def __fit_and_score(x_train, y_train, x_test, y_test, clf, cv_repeat=None, grid_search_k=None, param_grid=None, grid_scorer=None, scorers=None):
    """Fitting and scoring a classifier through crossvalidated gridsearch over
    a parameter grid.
    """
    # copy classifier
    clf = clone(clf)
    # grid search
    grid_search_clf = GridSearchCV(
        estimator=clf,
        param_grid=param_grid,
        scoring=scorers,
        cv=grid_search_k,
        refit=grid_scorer,
        )
    grid_search_clf = grid_search_clf.fit(x_train, y_train)
    # save to results
    result = {}
    result['gridsearch'] = grid_search_clf.cv_results_
    result['best_params'] = grid_search_clf.best_params_
    result['scores'] = _multimetric_score(grid_search_clf, x_test, y_test, scorers)
    result['cv_repeat'] = cv_repeat
    result['clf'] = clf.__class__.__name__
    return result

def _fit_and_score(x, y, clf, cv_repeats=None, grid_search_k=None, param_grid=None, grid_scorer=None, scorers=None):
    """Fitting and scoring a list of classifiers over a list of parameter grids.
    """
    # save results as a list of dicts
    results = []
    # cross validation
    cv = ShuffleSplit(n_splits=cv_repeats, test_size=0.3, train_size=0.7)  # random_state bug
    # shuffle split data
    for i, (train_index, test_index) in enumerate(cv.split(X=x, y=y)):
        x_train = _blockwise_slice(x, train_index)
        x_test = _blockwise_slice(x, test_index)
        y_train = _blockwise_slice(y, train_index)
        y_test = _blockwise_slice(y, test_index)
        # run classifier on data
        if type(clf) is list and type(param_grid) is list:
            for c, p in zip(clf, param_grid):
                result = __fit_and_score(x_train, y_train, x_test, y_test, c, i ,grid_search_k, p, grid_scorer, scorers)
                results.append(result)
        else:
            result = __fit_and_score(x_train, y_train, x_test, y_test, clf, i, grid_search_k, param_grid, grid_scorer, scorers)
            results.append(result)
    # compute and return results
    return list(compute(*results))

def fit_and_score(input, output, config):
    # start Dask cluster
    client, cluster = start_SGE_dask_cluster(
        demo=config['demo'],
        **config['SGE_dask']
        )
    # load data
    x = dask.array.from_npy_stack(input.x)
    y = dask.array.from_npy_stack(input.y)
    # fit and score
    results = _fit_and_score(
        x=x,
        y=y,
        clf=config['clf'],
        cv_repeats=config['cv_repeats'],
        grid_search_k=config['grid_search_k'],
        param_grid=config['param_grid'],
        grid_scorer=config['grid_scorer'],
        scorers=config['scorers'],
        )
    # save results to file
    with open(output.results, "wb") as f:
        pickle.dump(results, f)
    # stop Dask cluster
    try:
        client.close()
        cluster.finished()
        cluster.close()
    except Exception as e:
        print(e)
