import pandas as pd

ex_data = pd.read_csv("expert_details.csv")
ex_job_title = ex_data["job_title"]
ex_name = ex_data["expert_name"]
ex_date = ex_data["expert_date"]
ex_link = ex_data["link"]

#summa = ex_job_title.find_all("Programmer")