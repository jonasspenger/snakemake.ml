################################################################################
# author: Jonas Spenger
# date: 10.2018
################################################################################

import jinja2
import glob
import os
import pandas
import datetime


def generate_report(input):
    """ Generate report of csv and png files in input directory.
    Args:
        input (str): Input directory.
    Returns:
        None
    """
    # HTML template for the report
    tmplt = """
    <!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="UTF-8">
        <title>{{ title }}</title>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <br/>
        {{ datetime }}
        <br/>
        <h2>Results:</h2>
        {% for result in results %}
        <br/>
        <br/>
        {{ result }}
        {% endfor %}
        <h2>Figures:</h2>
        {% for figure in figures %}
        <br/>
        <br/>
        {{ figure }}
        <br/>
        <img src="{{ figure }}">
        {% endfor %}
    </body>
    </html>
    """
    # change directory to the folder
    owd = os.getcwd()
    os.chdir(input)
    # collect figures and results
    figures = sorted(glob.glob("**/*.png", recursive=True))
    csv_files = sorted(glob.glob("**/*.csv", recursive=True))
    csv_df = [pandas.read_csv(r) for r in csv_files]
    csv_html = [r.to_html() for r in csv_df]
    # set template variables
    template_vars = {"title" : "Snakemake ML Report",
                     "figures": figures,
                     "results": csv_html,
                     "datetime": datetime.datetime.now().strftime("%I:%M%p, %B %d, %Y")}
    # make html and save to file
    jinja2.Template(tmplt).stream(template_vars).dump('report.html')
    os.chdir(owd)
