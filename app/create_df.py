import pandas as pd
import re
import torchvision
from PIL import Image
import clip
import torch
import os
from torch.utils.data import Dataset, DataLoader
from transformers import CLIPTokenizer, CLIPProcessor
# import pandas as pd
# gtin_mapping=pd.read_csv(os.path.join(os.getcwd(),"dvc-manual/520_gtin_product_name.csv"))
# [gtin_mapping[gtin_mapping["gtin"]==gtin_mapping["gtin"].value_counts().index[1]]["product_name"].iloc[i] for i in range(0,4)]


def cleanhtml(raw_html):
    CLEANR = re.compile("<.*?>")  # remove html tags
    cleantext = re.sub(CLEANR, "", raw_html)
    pattern = r"\d*\.\d+"  # r'[0-9]' # remove decimal numbers
    cleantext = re.sub(pattern, "", cleantext)
    pattern = r"[0-9]"  # remove any digits
    cleantext = re.sub(pattern, "", cleantext)
    return cleantext


def get_mapping():
    gtin_mapping = pd.read_csv("/home/jupyter/dvc-manual/gtin_attr.csv")
    desc_columns = [
        col
        for col in gtin_mapping.columns
        if "desc" in col.lower() or "name" in col.lower() or "date" in col.lower()
    ]
    desc_columns = [
        "gtin",
        "KARF Picker Description",
        "Product Long Description",
        "Short Description",
        "Product Name",
    ]
    gtin_mapping = gtin_mapping.loc[:, desc_columns]
    gtin_mapping["Product Long Description"] = gtin_mapping.apply(
        lambda x: cleanhtml(str(x["Product Long Description"])), axis=1
    )
    gtin_mapping["Short Description"] = gtin_mapping.apply(
        lambda x: cleanhtml(str(x["Short Description"])), axis=1
    )
    gtin_mapping["Product Name"] = gtin_mapping.apply(
        lambda x: cleanhtml(str(x["Product Name"])), axis=1
    )
    gtin_mapping = gtin_mapping.rename(
        columns={
            "Product Long Description": "desc_long",
            "Short Description": "desc_short",
            "Product Name": "name",
            "KARF Picker Description": "desc_karf",
        }
    )
    gtin_mapping["desc_long"] = gtin_mapping.apply(
        lambda x: str(x["desc_long"]).replace("|", ""), axis=1
    )
    gtin_mapping["desc_short"] = gtin_mapping.apply(
        lambda x: str(x["desc_short"]).replace("|", ""), axis=1
    )
    gtin_mapping["desc_karf"] = gtin_mapping.apply(
        lambda x: str(x["desc_karf"]).replace("|", ""), axis=1
    )
    gtin_mapping["name"] = gtin_mapping.apply(
        lambda x: str(x["name"]).replace("|", ""), axis=1
    )
    gtin_mapping["gtin"] = gtin_mapping["gtin"].apply(lambda x: str(x).zfill(14))
    return gtin_mapping


def create_dataframe(path, label_col):
    loader = torchvision.datasets.ImageFolder(root=path)

    df = pd.DataFrame(loader.imgs, columns=["img_path", "label"])
    df["gtin"] = df.apply(lambda x: x["img_path"].split("/")[-2], axis=1)
    df["gtin"] = df["gtin"].apply(lambda x: str(x).zfill(14))

    gtin_mapping = get_mapping()

    df = df.merge(gtin_mapping, left_on=["gtin"], right_on=["gtin"], how="left")
    # no_desc_gtin = df[df["name"].isna()].gtin.unique()
    # print(f"Gtin's with no description: {no_desc_gtin}")
    # print(f"Shape before removing gtin's{df.shape[0]}")
    # df = df[~df["gtin"].isin(no_desc_gtin)]
    # print(f"Shape after removing gtin's{df.shape[0]}")
    # df = df[df[label_col].notna()]
    # print(f"Shape after removing na from product name column {df.shape[0]}")
    # key_list=[k for k in range(df.shape[0])]
    # df["key"]= key_list
    return df