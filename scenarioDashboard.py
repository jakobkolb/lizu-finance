import gspread
import pandas as pd
import pandas_bokeh
from bokeh.layouts import column, row
from bokeh.io import output_file, show
from bokeh.plotting import figure, curdoc

from src.helpers import connectToSheet
from src.guiElements import createScenario


pandas_bokeh.output_notebook()

sheet = connectToSheet(
    "api-credentials.json", "1tF62R6-lwG6T6G1aSRFhV2Q1GXK3Bu4lK4cu-Y3kpMY"
)


plot = figure(
    x_axis_label="Zeit",
    y_axis_label="Miete pro m2 inflationsbereinigt",
    sizing_mode="stretch_both",
)


curdoc().add_root(
    column(
        row(
            createScenario(sheet, plot, color="green", label="sc1"),
            createScenario(sheet, plot, color="blue", label="sc2"),
            createScenario(sheet, plot, color="grey", label="sc3"),
            sizing_mode="stretch_both",
        ),
        row(plot, sizing_mode="scale_width"),
        sizing_mode="scale_width",
    )
)
