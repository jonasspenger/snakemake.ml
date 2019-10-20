################################################################################
# author: Jonas Spenger
# date: 07.2018
# TODO: add more classifiers
################################################################################

include: "config.py"

# target rule
rule all:
    input:
        directory("reports"),

# generate figures, results and final report
rule figures_and_results:
    input:
        results="data/interim/results.pickle"
    output:
        reportdir=directory('reports'),
    run:
        from scripts.figures_and_results import figures_and_results
        figures_and_results(input, output, config)
        from scripts.generate_report import generate_report
        generate_report(input=output.reportdir)

# fit and score the classifier
rule fit_and_score:
    input:
        x="data/interim/x",
        y="data/interim/y",
    output:
        results="data/interim/results.pickle",
    run:
        from scripts.fit_and_score import fit_and_score
        fit_and_score(input, output, config)

# load the data to correct format
rule load_data:
    input:
        csv=config['filename'],
    output:
        x=directory("data/interim/x"),
        y=directory("data/interim/y"),
    run:
        from scripts.load_data import load_data
        load_data(input, output, config)

# preprocess the data
rule preprocessing:
    output:
        touch(config['filename']),
    run: pass

# clean the generated data
rule clean:
    shell:
        "rm -rf data/interim/*;\
        rm -rf reports;\
        rm -rf .snakemake;\
        rm -rf dask-worker-space;\
        rm -rf scripts/*__pycache__;\
        rm -rf dask-worker.o*;\
        rm -rf notebooks/*.png;\
        rm -rf notebooks/*.tex;\
        rm -rf notebooks/.ipynb_checkpoints;"
