from returns.pipeline import pipe
import numpy as np
import pandas as pd
import gspread
from returns.curry import curry


@curry
def connectToSheet(apiSecrets, address):
    account = gspread.service_account(apiSecrets)
    return account.open_by_key(address)


@curry
def getWorksheet(sheetName: str, sheet):
    return sheet.worksheet(sheetName)


@curry
def setField(worksheet, coordinates, value):
    worksheet.update(coordinates, value)


@curry
def getField(worksheet, coordinates):
    return worksheet.acell(coordinates).value


def replaceComata(listOfStrings):
    return map(lambda x: x.replace(",", "."), listOfStrings)


def mapToFloat(listOfStrings):
    return map(float, listOfStrings)


def inflationCorrect(inflation, timeSeries: pd.DataFrame) -> pd.DataFrame:
    calculateInflation = lambda i, d, x: x * pow(1 - i, d)
    prices = timeSeries.values
    inflationCorrectedPrices = np.ones(len(prices))
    for year, price in enumerate(prices):
        inflationCorrectedPrices[year] = calculateInflation(inflation, year, price)
    return pd.DataFrame(
        data=inflationCorrectedPrices,
        index=timeSeries.index,
        columns=timeSeries.columns,
    )


mapToFloatWithComata = pipe(replaceComata, mapToFloat)
