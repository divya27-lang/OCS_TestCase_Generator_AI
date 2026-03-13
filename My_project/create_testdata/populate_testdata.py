import pandas as pd
from create_testdata.testdata_automation import create_test_data
import openpyxl 
path = r'C:\Users\dgv290\ollama\My_project\testcases.xlsx'
import pandas as pd

def populate_eachtestdata(testdata_path, price_data_path, api_endpoint):
    df = pd.read_excel(testdata_path)

    for idx, row in df.iterrows():

        tc_id = row["TC_ID"]
        a_party = row["A_Party"]
        call_type = row["Call_Type"]
        duration = row["Duration_BytesUsed"]
        roaming_location = row["Roaming_Location"]
        called_country = row["Called_Country"]
        b_party_type = row["B_Party_Type"]

        b_party, exp_rating, exp_free_units = create_test_data(
            price_data_path,
            tc_id,
            a_party,
            call_type,
            duration,
            roaming_location,
            called_country,
            b_party_type,
            api_endpoint
        )

        # Populate results back
        df.at[idx, "B_Party"] = b_party
        df.at[idx, "Expected_Results"] = exp_rating
        df.at[idx, "Expected_Data_Free_Units"] = exp_free_units

    # Save updated file
    df.to_excel("testdata.xlsx", index=False)

    print("Excel updated successfully.")
