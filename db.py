import pandas as pd
import os


class DB():
    def __init__(self):
        URL: str = "https://raw.githubusercontent.com/pratik139patell/CS411SP22-Data/main/"
        
        try:
            self.Affiliation_df: pd.DataFrame = pd.read_csv("Data/Affiliation.csv", index_col=False).sort_values(by=["Affiliation_name"])
        except:
            self.Affiliation_df: pd.DataFrame = self.get_df_from_url(URL + "Affiliation.csv").sort_values(by=["Affiliation_name"])
            os.makedirs("Data", exist_ok=True)
            self.Affiliation_df.to_csv("Data/Affiliation.csv", index=False)

        try:
            self.Faculty_keyword_df: pd.DataFrame = pd.read_csv("Data/Faculty_keyword.csv", index_col=False)
        except:
            self.Faculty_keyword_df: pd.DataFrame = self.get_df_from_url(URL + "Faculty_keyword.csv")
            self.Faculty_keyword_df.to_csv("Data/Faculty_keyword.csv", index=False)

        try:
            self.Keyword_df: pd.DataFrame = pd.read_csv("Data/Keyword.csv", index_col=False).sort_values(by=["Keyword_name"])
        except:
            self.Keyword_df: pd.DataFrame = pd.read_csv(URL + "Keyword.csv", index_col=False).sort_values(by=["Keyword_name"])
            self.Keyword_df.to_csv("Data/Keyword.csv", index=False)

        try:
            self.Publication_keyword_df: pd.DataFrame = pd.read_csv("Data/Publication_keyword.csv", index_col=False)
        except:
            self.Publication_keyword_df: pd.DataFrame = pd.concat([self.get_df_from_url(URL + "Publication_keyword_"+str(i+1)+".csv") for i in range(4)])
            self.Publication_keyword_df.to_csv("Data/Publication_keyword.csv", index=False)

        try:
            self.Publication_df: pd.DataFrame = pd.read_csv("Data/Publication.csv", index_col=False)
        except:
            self.Publication_df: pd.DataFrame = pd.concat([self.get_df_from_url(URL + "Publication_"+str(i+1)+".csv") for i in range(4)])
            self.Publication_df.to_csv("Data/Publication.csv", index=False)

        try:
            self.Publish_df: pd.DataFrame = pd.read_csv("Data/Publish.csv", index_col=False)
        except:
            self.Publish_df: pd.DataFrame = self.get_df_from_url(URL + "Publish.csv")
            self.Publish_df.to_csv("Data/Publish.csv", index=False)

        try:
            self.Faculty_df: pd.DataFrame = pd.read_csv("Data/Faculty.csv", index_col=False).sort_values(by=["Faculty_name"])
        except:
            self.Faculty_df: pd.DataFrame = self.get_df_from_url(URL + "Faculty.csv").sort_values(by=["Faculty_name"])
            self.Faculty_df.to_csv("Data/Faculty.csv", index=False)

    
    def get_df_from_url(self, url) -> pd.DataFrame:
        return pd.read_csv(url, index_col=False, on_bad_lines='skip')



    def get_affiliation_df(self) -> pd.DataFrame: return self.Affiliation_df
    def get_faculty_keyword_df(self) -> pd.DataFrame: return self.Faculty_keyword_df
    def get_faculty_df(self) -> pd.DataFrame: return self.Faculty_df
    def get_keyword_df(self) -> pd.DataFrame: return self.Keyword_df
    def get_publication_keyword_df(self) -> pd.DataFrame: return self.Publication_keyword_df
    def get_publication_df(self) -> pd.DataFrame: return self.Publication_df
    def get_publish_df(self) -> pd.DataFrame: return self.Publish_df


    def set_affiliation_df(self, df: pd.DataFrame) -> None: 
        self.Affiliation_df = df
        os.makedirs("Data", exist_ok=True)
        self.Affiliation_df.to_csv("Data/Affiliation.csv", index=False)

    def set_faculty_keyword_df(self, df: pd.DataFrame) -> None: 
        self.Faculty_keyword_df = df
        os.makedirs("Data", exist_ok=True)
        self.Faculty_keyword_df.to_csv("Data/Faculty_keyword.csv", index=False)

    def set_faculty_df(self, df: pd.DataFrame) -> None: 
        self.Faculty_df = df
        os.makedirs("Data", exist_ok=True)
        self.Faculty_df.to_csv("Data/Faculty.csv", index=False)

    def set_keyword_df(self, df: pd.DataFrame) -> None: 
        self.Keyword_df = df
        os.makedirs("Data", exist_ok=True)
        self.Keyword_df.to_csv("Data/Keyword.csv", index=False)

    def set_publication_keyword_df(self, df: pd.DataFrame) -> None: 
        self.Publication_keyword_df = df
        os.makedirs("Data", exist_ok=True)
        self.Publication_keyword_df.to_csv("Data/Publication_keyword.csv", index=False)

    def set_publication_df(self, df: pd.DataFrame) -> None: 
        self.Publication_df = df
        os.makedirs("Data", exist_ok=True)
        self.Publication_df.to_csv("Data/Publication.csv", index=False)
        
    def set_publish_df(self, df: pd.DataFrame) -> None: 
        self.Publish_df = df
        os.makedirs("Data", exist_ok=True)
        self.Publish_df.to_csv("Data/Publish.csv", index=False)
