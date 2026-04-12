class RandomAnalyzer:
    def __init__(self, numbers):
        self.numbers = numbers

    def to_dataframe(self):
        import pandas as pd
        return pd.DataFrame({"Random Numbers": self.numbers})
