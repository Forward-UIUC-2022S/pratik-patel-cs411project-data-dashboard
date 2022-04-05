from enum import Flag
import pandas as pd
import os
import zipfile


class DB():
    def __init__(self, flag=False):        
        try:
            self.Affiliation_df: pd.DataFrame = pd.read_csv("Data/Affiliation.csv", index_col=False).sort_values(by=["Affiliation_name"])
            self.Faculty_keyword_df: pd.DataFrame = pd.read_csv("Data/Faculty_keyword.csv", index_col=False)
            self.Keyword_df: pd.DataFrame = pd.read_csv("Data/Keyword.csv", index_col=False).sort_values(by=["Keyword_name"])
            self.Publication_keyword_df: pd.DataFrame = pd.read_csv("Data/Publication_keyword.csv", index_col=False)
            self.Publication_df: pd.DataFrame = pd.read_csv("Data/Publication.csv", index_col=False)
            self.Publish_df: pd.DataFrame = pd.read_csv("Data/Publish.csv", index_col=False)
            self.Faculty_df: pd.DataFrame = pd.read_csv("Data/Faculty.csv", index_col=False).sort_values(by=["Faculty_name"])

            if flag:
                for data_frame in [self.Affiliation_df, self.Keyword_df, self.Publication_df, self.Faculty_df]:
                    for col in data_frame.columns:
                        if "photoUrl" in col: continue
                        try: data_frame[col] = data_frame[col].apply(lambda x: x.title()) 
                        except: continue
                self.save_affiliation_df()
                self.save_faculty_df()
                self.save_keyword_df()
                self.save_publication_df()
        except:
            with zipfile.ZipFile("assets\Data.zip", 'r') as zip_ref:
                zip_ref.extractall("Data")
                self.__init__(True)


    def get_affiliation_df(self) -> pd.DataFrame: return self.Affiliation_df
    def get_faculty_keyword_df(self) -> pd.DataFrame: return self.Faculty_keyword_df
    def get_faculty_df(self) -> pd.DataFrame: return self.Faculty_df
    def get_keyword_df(self) -> pd.DataFrame: return self.Keyword_df
    def get_publication_keyword_df(self) -> pd.DataFrame: return self.Publication_keyword_df
    def get_publication_df(self) -> pd.DataFrame: return self.Publication_df
    def get_publish_df(self) -> pd.DataFrame: return self.Publish_df


    def save_affiliation_df(self) -> None:
        os.makedirs("Data", exist_ok=True)
        self.Affiliation_df.to_csv("Data/Affiliation.csv", index=False)

    def save_faculty_keyword_df(self) -> None:
        os.makedirs("Data", exist_ok=True)
        self.Faculty_keyword_df.to_csv("Data/Faculty_keyword.csv", index=False)

    def save_faculty_df(self) -> None:
        os.makedirs("Data", exist_ok=True)
        self.Faculty_df.to_csv("Data/Faculty.csv", index=False)

    def save_keyword_df(self) -> None:
        os.makedirs("Data", exist_ok=True)
        self.Keyword_df.to_csv("Data/Keyword.csv", index=False)

    def save_publication_keyword_df(self) -> None:
        os.makedirs("Data", exist_ok=True)
        self.Publication_keyword_df.to_csv("Data/Publication_keyword.csv", index=False)

    def save_publication_df(self) -> None:
        os.makedirs("Data", exist_ok=True)
        self.Publication_df.to_csv("Data/Publication.csv", index=False)
        
    def save_publish_df(self) -> None: 
        os.makedirs("Data", exist_ok=True)
        self.Publish_df.to_csv("Data/Publish.csv", index=False)


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
