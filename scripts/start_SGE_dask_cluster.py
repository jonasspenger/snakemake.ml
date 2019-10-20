################################################################################
# author: Jonas Spenger
# date: 07.2018
################################################################################

import dask.distributed
import dask_jobqueue


def start_SGE_dask_cluster(n_workers=20, queue='all.q', walltime='04:00:00', n_cores=16, memory='30G', project=None, resource_spec=None, adaptivity=False, demo=False):
    """ Starting a Dask distributed cluster on a SGE cluster.
    Info:
        dask_jobqueue is under development and expected to change (ver. 0.3.0)
    Args:
        n_workers (int): Number of dask workers to launch on SGE.
        queue (str): SGE queue.
        walltime (str): Maximum run time <hh:mm:ss> (hours, minutes and seconds).
        n_cores (int): Number of cores run using shared memory (smp).
        memory (str): Maximum memory required (e.g. 2G, 500M etc.) (per worker).
        project (str): Project name.
        resource_spec (str): Further resource specification appended to the qsub submission script as a string (e.g. "#$ -o <output_logfile> \n #$ -e <error_logfile>).
        demo (bool): Start a local cluster if set to true.
    Returns:
        client: Client registered to the Dask scheduler
        cluster: Dask cluster stop workers through: cluster.stop_workers(cluster.jobs))
    """
    # start a local cluster if demo
    if demo == True:
        cluster = dask.distributed.LocalCluster()
        client = dask.distributed.Client(cluster)
        return client, cluster
    # current dask_jobqueue does not pass memory and cores to SGE, so we do it manually
    r_spec = ""
    r_spec += "h_vmem=%s \n" % memory  # first one is preprended by #$ -l by dask_jobqueue
    r_spec += "#$ -pe smp %s \n" % n_cores
    if resource_spec != None:
        r_spec += resource_spec
    # start the cluster
    cluster = dask_jobqueue.SGECluster(
        cores=n_cores,
        memory=memory,
        queue=queue,
        walltime=walltime,
        project=project,
        resource_spec=r_spec,
        )
    # scale cluster to num_workers new workers
    cluster.scale(n_workers)
    # turn on cluster adaptivity
    if adaptivity == True:
        cluster.adapt()
    # get a client registered to the cluster
    client = dask.distributed.Client(cluster)
    return client, cluster
