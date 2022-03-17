import pandas as pd
import os

class DB():
    def __init__(self):
        try: self.Affiliation_df: pd.DataFrame = pd.read_csv("Data/Affiliation.csv", index_col=False).sort_values(by=["Affiliation_name"])
        except: 
            self.Affiliation_df: pd.DataFrame = pd.read_csv("https://drive.google.com/uc?id=1ATro5A4xBrEa6q8qL0dyXGKN2RRb0JYe", index_col=False).sort_values(by=["Affiliation_name"])
            os.makedirs("Data", exist_ok=True)
            self.Affiliation_df.to_csv("Data/Affiliation.csv", index=False)
            
        try: self.Faculty_keyword_df: pd.DataFrame = pd.read_csv("Data/Faculty_keyword.csv", index_col=False)
        except: 
            self.Faculty_keyword_df: pd.DataFrame = pd.read_csv("https://drive.google.com/uc?id=1lwS8gY9j56b-FmJ5UMp1m7tU-r6y7t-d", index_col=False)
            self.Faculty_keyword_df.to_csv("Data/Faculty_keyword.csv", index=False)

        try: self.Keyword_df: pd.DataFrame = pd.read_csv("Data/Keyword.csv", index_col=False).sort_values(by=["Keyword_name"])
        except: 
            self.Keyword_df: pd.DataFrame = pd.read_csv("https://drive.google.com/uc?id=1P5GHcvkr-o9uvjGoU-2QlXeCwl4x7K7m", index_col=False).sort_values(by=["Keyword_name"])
            self.Keyword_df.to_csv("Data/Keyword.csv", index=False)

        try: self.Publication_keyword_df: pd.DataFrame = pd.read_csv("Data/Publication_keyword.csv", index_col=False)
        except: 
            self.Publication_keyword_df: pd.DataFrame = pd.read_csv("https://drive.google.com/uc?id=1WNeM1KSUsQcHvom_Iy-b6KyrCejc4yhM", index_col=False)
            self.Publication_keyword_df.to_csv("Data/Publication_keyword.csv", index=False)

        try: self.Publication_df: pd.DataFrame = pd.read_csv("Data/Publication.csv", index_col=False)
        except: 
            self.Publication_df: pd.DataFrame = pd.read_csv("https://drive.google.com/uc?id=1nU9-5crsJPuUTbBnVLGpki0RhOWp_WXH", index_col=False)
            self.Publication_df.to_csv("Data/Publication.csv", index=False)

        try: self.Publish_df: pd.DataFrame = pd.read_csv("Data/Publish.csv", index_col=False)
        except: 
            self.Publish_df: pd.DataFrame = pd.read_csv("https://drive.google.com/uc?id=1DkYpHYqB7OH9iLy2F0_ivWs2IG5yuw5m", index_col=False)
            self.Publish_df.to_csv("Data/Publish.csv", index=False)

        try: self.Faculty_df: pd.DataFrame = pd.read_csv("Data/Faculty.csv", index_col=False).sort_values(by=["Faculty_name"])
        except: 
            self.Faculty_df: pd.DataFrame = pd.read_csv("https://drive.google.com/uc?id=1sBlfG5vI83rAIhcGpKGOT2HAI3DTHmAL", index_col=False).sort_values(by=["Faculty_name"])
            self.Faculty_df.to_csv("Data/Faculty.csv", index=False)


    def get_affiliation_df(self) -> pd.DataFrame: return self.Affiliation_df
    def get_faculty_keyword_df(self) -> pd.DataFrame: return self.Faculty_keyword_df
    def get_faculty_df(self) -> pd.DataFrame: return self.Faculty_df
    def get_keyword_df(self) -> pd.DataFrame: return self.Keyword_df 
    def get_publication_keyword_df(self) -> pd.DataFrame: return self.Publication_keyword_df
    def get_publication_df(self) -> pd.DataFrame: return self.Publication_df 
    def get_publish_df(self) -> pd.DataFrame: return self.Publish_df
    
    def set_affiliation_df(self, df: pd.DataFrame) -> None: self.Affiliation_df = df
    def set_faculty_keyword_df(self, df: pd.DataFrame) -> None: self.Faculty_keyword_df = df
    def set_faculty_df(self, df: pd.DataFrame) -> None: self.Faculty_df = df
    def set_keyword_df(self, df: pd.DataFrame) -> None: self.Keyword_df = df
    def set_publication_keyword_df (self, df: pd.DataFrame) -> None: self.Publication_keyword_df = df
    def set_publication_df(self, df: pd.DataFrame) -> None: self.Publication_df = df 
    def set_publish_df(self, df: pd.DataFrame) -> None: self.Publish_df = df
