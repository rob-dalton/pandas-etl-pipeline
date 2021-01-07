from pandas import DataFrame
from typing import List, Union

class Step(object):
    """Step to run in a Pipeline.

    A Step is a function and a set of arguments that
    are called during Pipeline.run().
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        return self.func(*self.args, **self.kwargs)


class Transform(Step):
    """Transform to run in a data pipeline.

    A Transform is a subclass of Step. When run, its function
    is passed Pipeline.data as the first positional argument.
    """
    def run(self, data:DataFrame):
        return self.func(data, *self.args, **self.kwargs)


class Load(Transform):
    """Load to run in a data pipeline.

    A Load is a subclass of Transform. It requires a
    destination keyword argument (indicates where the data will be
    saved or passed to).
    """
    def __init__(self, *args, **kwargs):
        if kwargs.get('destination') is None:
            raise Exception("No destination provided for Load.")
        super(Load, self).__init__(*args, **kwargs)


class Pipeline(object):
    """Class to create and run a data pipeline for a Pandas Dataframe.

    ATTRIBUTES
    - source: The data source for the pipeline. Either a DataFrame object or fpath of CSV file to read.
    - extract: (Optional) The Step to run for extraction.
    - transformations: List of Steps and Transforms to run.
    - load: (Optional) The final Step in a pipeline. Should save or
            pass Pipeline.data somewhere.
    """

    def __init__(self,
                 source:Union[str, DataFrame],
                 steps:List[Union[Step, Transform, Load]],
                 extract:Step=None,
                 load:Load=None):
        self.data = None
        self.source = source
        self.steps = steps
        self.extract = extract
        self.load = load

    def _extract(self)->DataFrame:
        """Run Step for extraction.

        Step is passed Pipeline.source as its first positional arg.
        """
        new_args = [arg for args in self.extract.args]
        new_args.insert(0, self.source)
        self.extract.args = new_args
        return self.extract.run()

    def run(self, load=True):
        # set self.data
        if type(self.source) is DataFrame:
            self.data = self.source
        else:
            # Run extraction step if source is fpath
            # NOTE: Wait til run() to call _extract() in case
            #       source depends on other Pipelines.
            self.data = self._extract()

        # Run steps
        for step in self.steps:
            if isinstance(step, Load):
                step.run(self.data)
            elif isinstance(step, Transform):
                # update self.data with Transform
                self.data = step.run(self.data)
            else:
                step.run()

        # Run load step
        if self.load is not None:
            self.load.run(self.data)


def save_to_csv(df:DataFrame, destination:str):
    df.to_csv(destination, index=False)
