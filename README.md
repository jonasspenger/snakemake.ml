# About
This snakemake project is for running grid search machine learning tasks on an SGE cluster.
The classifier and parameters can be set in the `config.py` file.
The analysis is carried out on a user provided csv file.

# How to get started
## Install packages and environment
1. You might need to append the following two channels to install the required packages
```
conda config --append channels conda-forge
conda config --append channels bioconda
```
2. Install packages
```
conda create --yes -n snakemakeml --file requirements.txt
```
3. Activate environment
```
conda activate snakemakeml
```

## How to configure the `config.py` file

multiclass
http://scikit-learn.org/dev/modules/multiclass.html

The following parameters can be set and configured
* `config['demo'] = True` for test running the installation, else set it as False.
* `config['filename'] = 'data/raw/preprocessed.csv'` the input file provided by the user
* `config['x_cols'] = [1, 2, 3]` the columns of the predictor variables
* `config['y_col'] = 0` the column of the target variable
* `config['cv_repeats'] = 2` the number of repeats of the
random permutation cross-validator, if 2 then the data will be randomly shuffled and validated two times
* `config['grid_scorer'] = 'accuracy'` set the grid scorer, i.e. the score which will be used for selecting the best model during the grid search.
* `config['grid_search_k'] = 3` number of folds used for grid search
* `config['clf'] = GradientBoostingClassifier()` choose which classifier to use. Here, a Gradient Boosting model is used for classification. For more classifiers and methods refer to http://scikit-learn.org/stable/modules/classes.html.
* `config['param_grid'] = {'learning_rate': [0.01, 0.1], 'n_estimators': [50, 100]` the grid search will be run over this parameter grid. For this example, all (four) combinations of `learning_rate` and `n_estimators` will be evaluated in the grid search. The parameter names can be found in the documentation, e.g. http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html.
* `config['scorers'] = {'accuracy': accuracy_score}` chose which score and performance metrics to report in the final results.

## How to run
1. Run snakemake
```
snakemake
```
2. Inspect results in `reports/report.html`
3. Clean up after running snakemake by removing all generated files
```
snakemake clean
```

# How to view Dask Dashboard (web interface)
1. Connect to the notebook on your local browser
   * `localhost:8787/status`
