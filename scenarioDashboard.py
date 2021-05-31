import gspread
import pandas as pd
import pandas_bokeh
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.server.server import Server

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

def run(doc):
    doc.add_root(
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

# configure and run bokeh server
kws = {'port': 5100, 'prefix': '/bokeh', 'allow_websocket_origin': ['167.172.166.169']}
server = Server(run, **kws)
server.start()
if __name__ == '__main__':
    server.io_loop.add_callback(server.show, '/')
    server.io_loop.start()