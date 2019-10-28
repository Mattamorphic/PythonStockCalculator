'''
    Constants
    A central class for all of our constants

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''


class Constants:
    DATE_FORMAT = "yyyy-MM-dd"
    PY_DATE_FORMAT = '%Y-%m-%d'
    STOCK_LABEL_REGEX = "[A-Za-z]{0,6}"

    class GraphOptions:
        LOW = 'low'
        HIGH = 'high'
        AVERAGE = 'average'
        DIFF = 'diff'
        GAIN = 'gain'

        LOW_LABEL = 'Low Price'
        HIGH_LABEL = 'High Price'
        AVERAGE_LABEL = 'Average Price'
        DIFF_LABEL = 'High/Low Price Diff'
        GAIN_LABEL = 'Percentage Gain'

        @staticmethod
        def all():
            '''
                Fetch all of the constants

                Returns:
                    List[str]
            '''
            return [
                Constants.GraphOptions.LOW,
                Constants.GraphOptions.HIGH,
                Constants.GraphOptions.AVERAGE,
                Constants.GraphOptions.DIFF,
                Constants.GraphOptions.GAIN
            ]

        @staticmethod
        def getLabels():
            '''
                Return a mapping of option to labels

                Returns:
                    (Dict(string, string))
            '''
            return {
                Constants.GraphOptions.LOW: Constants.GraphOptions.LOW_LABEL,
                Constants.GraphOptions.HIGH: Constants.GraphOptions.HIGH_LABEL,
                Constants.GraphOptions.AVERAGE: Constants.GraphOptions.AVERAGE_LABEL,
                Constants.GraphOptions.DIFF: Constants.GraphOptions.DIFF_LABEL,
                Constants.GraphOptions.GAIN: Constants.GraphOptions.GAIN_LABEL
            }

        @staticmethod
        def getOptionOrLabel(value: str):
            '''
                Get a label from the option

                Args:
                    label (str): option

                Returns:
                    str
            '''
            for option, label in Constants.GraphOptions.getLabels().items():
                if label == value:
                    return option
                elif option == value:
                    return label
            return None
