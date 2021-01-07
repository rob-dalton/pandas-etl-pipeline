# Pandas Pipeline
This package contains the `Pipeline` class - a class for creating and running data pipelines using Pandas DataFrames.

## Overview
### `Pipeline(self, source, extract, transformations, load)`
A data pipeline comprised of a data object (a DataFrame) and a set of Steps.
    - `source`: The data source for the pipeline. Either a DataFrame object or fpath of CSV file to read.
    - `extract`: (Optional) The Step to run for extraction.
    - `transformations`: List of Steps and Transforms to run.
    - `load`: (Optional) The final Step in a pipeline. Should save or pass Pipeline.data somewhere.

### `Step(self, func, *args, **kwargs)`
A function and a set of arguments that are called during Pipeline.run().

### `Transform(self, func, *args, **kwargs)`
A subclass of `Step`. When run, its function is passed `Pipeline.data` as the first positional argument.

### `Load(self, func, *args, **kwargs)`
A subclass of `Transform`. It requires a destination keyword argument (indicates where the data will be saved or passed to).

## Examples
### Example with `Step` 
```
import pandas as pd
from pandas-pipeline import Pipeline, Step

df = pd.DataFrame({
    'Letters': ['a', 'b', 'c'],
    'Numbers': [1, 2, 3]
})
print(df)

pipeline = Pipeline(
    data=df,
    steps=[Step(print, "This step just ran!")]
)

result = pipeline.run()
print(result)

>>
  Letters  Numbers
0       a        1
1       b        2
2       c        3

This step just ran!

  Letters  Numbers
0       a        1
1       b        2
2       c        3
```

### Example with `Transform` 
```
import pandas as pd
from pandas-pipeline import Pipeline, Transform

def add_value_to_numbers(data: pd.DataFrame, value: int)->None:
    data.Numbers += value

df = pd.DataFrame({
    'Letters': ['a', 'b', 'c'],
    'Numbers': [1, 2, 3]
})
print(df)

pipeline = Pipeline(
    data=df,
    steps=[Transform(add_value_to_numbers, 1)]
)

transformed = pipeline.run()
print(transformed)

>>
  Letters  Numbers
0       a        1
1       b        2
2       c        3

  Letters  Numbers
0       a        2
1       b        3
2       c        4
```

### Example with `Load` 
```
import pandas as pd
from pandas-pipeline import Pipeline, Transform, Load, save_to_csv

def add_value_to_numbers(data: pd.DataFrame, value: int)->None:
    data.Numbers += value

df = pd.DataFrame({
    'Letters': ['a', 'b', 'c'],
    'Numbers': [1, 2, 3]
})

pipeline = Pipeline(
    data=df,
    steps=[Transform(add_value_to_numbers, 1)],
    load=Load(save_to_csv, destination="./example.csv")
)

pipeline.run() # saves transformed df from example above to file.
```
