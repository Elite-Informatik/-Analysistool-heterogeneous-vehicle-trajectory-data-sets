import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.record import DataRecord


class TestData:
    data = [
        DataRecord("Test data", (Column.SPEED.value, Column.TRAJECTORY_ID.value, Column.ACCELERATION.value),
                   pd.DataFrame({
                       Column.SPEED.value: [1, 2, 3, 4, 5],
                       Column.TRAJECTORY_ID.value: ["a", "b", "c", "d", "e"],
                       Column.ACCELERATION.value: [1.1, 2.2, 3.3, 4.4, 5.5]
                   }))
    ]
