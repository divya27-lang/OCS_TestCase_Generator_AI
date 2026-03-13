
import http
from create_testdata.populate_testdata import populate_eachtestdata
path = r'C:\Users\dgv290\ollama\My_project\testcases.xlsx'
pricelist_path=r'C:\Users\dgv290\ollama\My_project\pricelist.xlsx'
api_endpoint= 'http://127.0.0.1:9981'
def main():
    print("creating test data with testdata automation")
    populate_eachtestdata(path,pricelist_path,api_endpoint)

if __name__ == "__main__":
    main()