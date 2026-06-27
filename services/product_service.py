import pandas as pd


class ProductService:

    def __init__(self):

        # Load dataset
        self.df = pd.read_csv("data/products.csv")

        # Rename columns
        self.df.rename(
            columns={
                "brand_name": "brand",
                "model": "name"
            },
            inplace=True
        )

        # Convert numeric columns
        self.df["price"] = pd.to_numeric(
            self.df["price"],
            errors="coerce"
        )

        self.df["rating"] = pd.to_numeric(
            self.df["rating"],
            errors="coerce"
        )

        self.df["ram"] = pd.to_numeric(
            self.df["ram"],
            errors="coerce"
        )

        self.df["memory_size"] = pd.to_numeric(
            self.df["memory_size"],
            errors="coerce"
        )

        # Remove invalid rows
        self.df.dropna(subset=["price"], inplace=True)

        # Fill missing values
        self.df["rating"] = self.df["rating"].fillna(0)

        # Fill numeric columns
        self.df["rating"] = self.df["rating"].fillna(0)
        self.df["ram"] = self.df["ram"].fillna(0)
        self.df["memory_size"] = self.df["memory_size"].fillna(0)

        # Fill only text columns
        text_columns = [
            "brand",
            "name",
            "processor",
            "processor_brand",
            "gpu_brand",
            "gpu_type",
            "os",
            "display_size",
            "warrenty"
        ]

        for col in text_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna("")
        # Create searchable description
        self.df["description"] = (
                self.df["brand"].astype(str) + " " +
                self.df["name"].astype(str) + " " +
                self.df["processor_brand"].astype(str) + " " +
                self.df["processor"].astype(str) + " " +
                self.df["gpu_brand"].astype(str) + " " +
                self.df["gpu_type"].astype(str) + " " +
                self.df["ram"].astype(int).astype(str) + " GB RAM " +
                self.df["memory_size"].astype(int).astype(str) + " GB SSD " +
                self.df["os"].astype(str)
        )

    # -----------------------------------------

    def get_all_products(self):

        return self.df

    # -----------------------------------------

    def get_brands(self):

        return sorted(
            self.df["brand"].unique().tolist()
        )

    # -----------------------------------------

    def get_statistics(self):

        return {
            "total_laptops": len(self.df),
            "total_brands": self.df["brand"].nunique(),
            "average_price": self.df["price"].mean(),
            "average_rating": self.df["rating"].mean()
        }

    # -----------------------------------------

    def filter_products(
        self,
        brand="All",
        max_price=None,
        min_rating=0,
        processor_brand="All",
        ram="All"
    ):

        data = self.df.copy()

        if brand != "All":

            data = data[
                data["brand"] == brand
            ]

        if processor_brand != "All":

            data = data[
                data["processor_brand"] == processor_brand
            ]

        if ram != "All":

            data = data[
                data["ram"].astype(int).astype(str) == str(ram)            ]

        if max_price is not None:

            data = data[
                data["price"] <= max_price
            ]

        data = data[
            data["rating"] >= min_rating
        ]

        return data

    # -----------------------------------------

    def search_products(self, query):

        return self.df[

            self.df["description"].str.contains(
                query,
                case=False,
                na=False
            )

        ]