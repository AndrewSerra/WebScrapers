import pandas as pd


class Storage:

    def __init__(self):
        self.df = pd.read_csv('colors.csv')

    def add_data(self, data):
        self.df["c1"] = data["c1"]
        self.df["c2"] = data["c2"]
        self.df["c3"] = data["c3"]
        self.df["c4"] = data["c4"]
        self.df["c5"] = data["c5"]

        assert isinstance(data, dict)

    # Export to csv
    def export_csv(self):
        print("Saving...")
        self.df.to_csv("colors.csv")
        print("Saved.")
