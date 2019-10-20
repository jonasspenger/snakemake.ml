################################################################################
# author: Jonas Spenger
# date: 07.2018
################################################################################

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas
import pickle
import os


def format_results(results):
    tidy_results = pandas.concat([
        pandas.concat([
            pandas.DataFrame(row['gridsearch']).add_prefix('gridsearch_').T,
            pandas.Series(row['best_params']).add_prefix('best_params_'),
            pandas.Series(row['scores']).add_prefix('scores_'),
            row.drop(['scores', 'best_params', 'gridsearch']),
            ]).T.fillna(method='ffill')
        for idx, row in results.iterrows()], sort=True)
    tidy_results.index.name = 'gridsearch_repeat'
    tidy_results = tidy_results.reset_index()
    return tidy_results.astype(object)

def boxplot(results, filedir):
    """Make boxplot of items columns of results.
    """
    fig = plt.figure()
    columns = list(results.filter(regex=r'scores_').columns)
    results.filter(items=columns + ['clf', 'cv_repeat']).drop_duplicates().boxplot(column=columns, by='clf')
    plt.savefig(filedir + '/boxplot.png')

def gridsearch_curves(results, filedir):
    # for each gridsearch
    for idx, row in results.filter(regex=r'best_params_|clf|cv_repeat').drop_duplicates().dropna(how='all').iterrows():
        # for each parameter of that search
        for param, value in row.filter(regex='best_params_').dropna().iteritems():
            # filter dataframe for this repeat and classifier where other params are fixated
            other_params = pandas.DataFrame(row.filter(regex='best_params_|repeat|clf').drop(param)).T
            other_params_renamed = other_params.rename(columns=lambda x: x.replace('best_params_', 'gridsearch_param_'))
            merged_df = pandas.merge(results, other_params, how='inner').merge(other_params_renamed, how='inner')
            # prepare dataframe for plot
            p = param.replace('best_params_', 'gridsearch_param_')
            filtered_df = merged_df.filter(regex='mean_test|' + p).dropna(axis=1)
            if len(filtered_df.index) > 1:
                fname = filedir + '/gridsearch_' + row.clf + '_repeat_' + str(row['cv_repeat']) + '.png'
                ax = filtered_df.plot(x=p, title=fname, ylim=(0,1))
                ax.axvline(value, color='r', linestyle='--')
                fig = ax.get_figure()
                fig.savefig(fname)

def figures_and_results(input, output, config):
    # make directories
    os.makedirs(os.path.join(output.reportdir, 'csv'), exist_ok=True)
    os.makedirs(os.path.join(output.reportdir, 'figures'), exist_ok=True)
    # load and format results
    results = pandas.DataFrame(pandas.read_pickle(input.results))
    tidy_results = format_results(results)
    # save results to csv
    csvdir = os.path.join(output.reportdir, 'csv')
    tidy_results.to_csv(csvdir + '/results.csv')
    # save condensed results to csv
    cols = ['clf', 'cv_repeat'] + list(tidy_results.filter(regex=r'scores_').columns)
    tidy_results.filter(items=cols).drop_duplicates().to_csv(csvdir + '/results_condensed.csv')
    # generate and save figures
    boxplot(
        results=tidy_results,
        filedir=os.path.join(output.reportdir, 'figures')
        )
    gridsearch_curves(
        results=tidy_results,
        filedir=os.path.join(output.reportdir, 'figures')
        )
