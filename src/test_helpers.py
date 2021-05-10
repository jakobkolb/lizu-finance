import pytest
import pandas as pd
from returns.pipeline import pipe
import random
from .helpers import (
    connectToSheet,
    getWorksheet,
    replaceComata,
    mapToFloat,
    mapToFloatWithComata,
    inflationCorrect,
    getField,
    setField,
)


def test_replaceComata():
    assert list(replaceComata(["1,2", "2,2"])) == ["1.2", "2.2"]


def test_mapToFloat():
    assert list(mapToFloat(["1.2", "2.2"])) == [1.2, 2.2]


def test_mapToFloatWithComata():
    assert list(mapToFloatWithComata(["1,2", "2,2"])) == [1.2, 2.2]


def test_inflationCorrect():
    inflation = 0.1
    timeSeries = pd.DataFrame(data=[1, 1, 1, 1, 1], columns=["blub"])

    inflationCorrectedTimeSeries = inflationCorrect(inflation, timeSeries)

    assert inflationCorrectedTimeSeries.columns == timeSeries.columns
    assert inflationCorrectedTimeSeries.values[0] == 1
    assert inflationCorrectedTimeSeries.values[4] == pow(1 - inflation, 4)


def test_sheetConnection():
    testSheetAddress = "1g2YkPCGQiXRhhK0Tf3UlPjhhz0MzXhyxgJO8cxx1GFs"
    value = random.randint(1, 100)
    coordinates = "A1"

    getWorkSheet1 = pipe(connectToSheet("api-credentials.json"), getWorksheet("Sheet1"))

    worksheet = getWorkSheet1(testSheetAddress)

    setField(worksheet, coordinates, value)

    assert int(getField(worksheet, coordinates)) == value
