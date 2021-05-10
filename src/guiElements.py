from src.helpers import (
    mapToFloatWithComata,
    inflationCorrect,
    mapToFloat,
    setField,
)
from bokeh.layouts import column
from src.constants import inputSheetLocations
from returns.pipeline import pipe
from returns.curry import partial
from bokeh.models import Button, Slider
import pandas as pd


def getRentTimeseries(sheet):
    rent = sheet.row_values(6)
    years = sheet.row_values(1)
    return pd.DataFrame(
        columns=[rent[1]],
        data=mapToFloatWithComata(rent[3:]),
        index=pd.Index(data=mapToFloat(years[3:]), name="Year"),
    )


def updateGuiStateCallback(guiState, name):
    def callback(attr, old, new):
        guiState[name] = new
        print(name, new)

    return callback


def fetchAndUpdate(dataSource, sheetConnection):
    data = pipe(getRentTimeseries, partial(inflationCorrect, 0.01))(
        sheetConnection.worksheet("Prognose")
    )
    newData = {"y": data.values.T[0], "x": data.index.values}
    dataSource.data = newData


def send(dataSource, guiState, sheetConnection):
    def callback():
        print(guiState)
        for key, value in guiState.items():
            setField(
                sheetConnection.worksheet("BankFinanzierung"),
                inputSheetLocations[key]["location"],
                value,
            )
        fetchAndUpdate(dataSource, sheetConnection)

    return callback


def createSlider(guiState, fieldName):
    slider = Slider(
        **inputSheetLocations[fieldName]["config"],
        title=fieldName,
    )
    slider.on_change("value", updateGuiStateCallback(guiState, fieldName))
    return slider


def createFetchButton(dataSource, guiState, sheetConnection, label):
    fetchButton = Button(label=f"Update {label}")
    fetchButton.on_click(send(dataSource, guiState, sheetConnection))
    return fetchButton


def createDatasource(plot, color, label):
    r1 = plot.line(y=[], x=[], color=color, legend_label=label)
    return r1.data_source


def createScenario(sheetConnection, plot, color, label):
    guiState = {
        key: inputSheetLocations[key]["config"]["value"]
        for key in inputSheetLocations.keys()
    }
    dataSource = createDatasource(plot, color, label=label)
    return column(
        *[
            createSlider(guiState, fieldName)
            for fieldName in inputSheetLocations.keys()
        ],
        createFetchButton(dataSource, guiState, sheetConnection, label),
    )
