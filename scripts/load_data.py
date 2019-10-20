################################################################################
# author: Jonas Spenger
# date: 09.2018
################################################################################

import dask.array
import sklearn.datasets


def load_data(input, output, config):
    """ Load data, extract and save data ready for analysis.
    Args:
        input: Snakemake input with keywords csv.
        output: Snakemake output with keywords x and y.
        config (dict): Configuration dictionary with keywords x_cols and y_col.
    Returns:
        None
    """
    if config['demo']:  # generate sample data if demo
        x, y = sklearn.datasets.make_classification(
            n_samples=1000,
            n_features=100,
            n_informative=80,
            n_clusters_per_class=10,
            n_classes=4,
            )
        x = dask.array.from_array(x, chunks=(1000,-1))
        y = dask.array.from_array(y, chunks=(1000))
    else:  # load ,preprocess and save real data
        # load data
        ddf = dask.dataframe.read_csv(input)
        # make x and y
        x = dask.array.from_array(ddf.compute().values[:, config['x_cols']], chunks=(2000000, -1))
        y = dask.array.from_array(ddf.compute().values[:, config['y_col']], chunks=(2000000,))
    # save data
    dask.array.to_npy_stack(dirname=output.x, x=x)
    dask.array.to_npy_stack(dirname=output.y, x=y)
