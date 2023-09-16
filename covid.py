import requests
from requests.exceptions import HTTPError
from pprint import pp
from configparser import ConfigParser, NoSectionError, NoOptionError
# pp(data,indent=4, width=200)
import argparse
from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt


def get_ninja_api_key():
    
    conf = ConfigParser()
    try:
        
        conf.read("secrets.ini")
        return conf["api_ninja"]["api_key"]
    except (NoSectionError, NoOptionError, FileNotFoundError) as e:
        print(f"An error occurred: {e}")
        return None
    

def read_user_cli_args():
    parser = argparse.ArgumentParser(
        description = "Gets COVID information about a specific country."
    )
    parser.add_argument("country",
                        type=str, help="which country to get info for. ")
    return parser.parse_args() # to get the namespace of the arguments.

def build_query_params(country_name:str) -> Dict:
    return {"country": country_name }
def send_request_to_covid_api(base_url:str, API_KEY:str, q_params:Dict) -> Dict:
    
    try:
        r = requests.get(base_url, params= q_params, headers={'X-Api-Key': API_KEY})
        r.raise_for_status()
        content_type = r.headers.get("Content-Type")
        
        return r.json()
        
    except HTTPError as http_err:
        print(f"HTTPError occurred: {http_error}")
    except Exception as e:
        print(f"Error occurred ... {e}")
    else:
        print("Success!!!")

def visualize_data(data):
    
    
    # df = pd.DataFrame(data)
    # pp(df)
    df = pd.DataFrame(data[0]["cases"]).T
    plt.figure(figsize = (10,6))
    plt.plot(df.index, df["total"], label = "Total")
    plt.xlabel("Dates")
    plt.ylabel("Total Cases")
    plt.title(f"Total number of COVID cases for {data[0]['country']} 2020 - 2023")
    plt.grid(True)
    plt.show()
        

if __name__ == "__main__":
    # if current script is the main program being run...
    # Accepts the name of the country from the command line. 
    user_args = read_user_cli_args()
    q_params = build_query_params(user_args.country)
    API_KEY = get_ninja_api_key()
    BASE_URL = 'https://api.api-ninjas.com/v1/covid19'
    data = send_request_to_covid_api(BASE_URL, API_KEY, q_params)
    visualize_data(data)
    
    
    