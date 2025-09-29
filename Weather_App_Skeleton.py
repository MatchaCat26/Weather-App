import os, json, textwrap, pathlib, sys

base = "Data/Weather_App_Skeleton"
os.makedirs(base, exist_ok= True)
os.makedirs(f"{base}/data", exist_ok=True)