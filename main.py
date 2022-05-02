import pandas as pd
import os, json, requests

vra_directory = os.fsencode("./VRA")
air_cia_directory = os.fsencode("./AIR_CIA")
airport_url = "https://airport-info.p.rapidapi.com/airport"

headers = {
	"X-RapidAPI-Host": "airport-info.p.rapidapi.com",
	"X-RapidAPI-Key": "dummy_key"
}



def snake_case(text, sep='_'):

    new_text = ""

    for i, letter in enumerate(text):
        if i and letter.isupper():
            new_text += sep
        
        new_text += letter
    
    return new_text

def rename_columns(df):

    for col in df.columns:

        if col[0:4] == "ICAO":
            renamed_col = col[0:4].lower() + col[4::]

        else:
            renamed_col = col[0].lower() + col[1::]

        renamed_col = snake_case(renamed_col)
        df.rename(columns={col:renamed_col}, inplace=True)
    
    return df

def treat_vra():

    for file in os.listdir(vra_directory):

        filename = os.fsdecode(file)
        directory = os.fsdecode(vra_directory)

        data = pd.read_json(f"{directory}/{filename}", orient="records",  encoding = 'utf-8-sig')
        data = rename_columns(data)

        data.to_json(f"{directory}_FIX/{filename}", orient="records", force_ascii=False)


def create_save_folder(dir):
    dir = os.fsdecode(dir)
    dir = dir + "_FIX"
    try:
        os.mkdir(dir)
    except:
        print(f'Diretório: {dir} já criado, continuando')

def replace_characters(df):

    for col in df.columns:
        renamed_col = col.replace(" ", "_")
        df.rename(columns={col:renamed_col}, inplace=True)

    return df

def split_col(df):

    df[['ICAO', 'IATA']] = df['ICAO_IATA'].str.split(' ', 1, expand=True)
    df.drop(columns="ICAO_IATA", inplace=True)

    return df

def treat_air_cia():
    
    for file in os.listdir(air_cia_directory):

        filename = os.fsdecode(file)
        directory = os.fsdecode(air_cia_directory)

        data = pd.read_csv(f"{directory}/{filename}",  encoding = 'utf-8-sig', sep=";")
        data = replace_characters(data)
        data = split_col(data)
        
        data.to_csv(f"{directory}_FIX/{filename}", index=False)

def get_icao_list():
    icao_list = []

    for file in os.listdir("./VRA_FIX"):
        data = pd.read_json(f"./VRA_FIX/{file}", orient="records",  encoding = 'utf-8-sig')

        icao_vra = list(data['icao_Aeródromo_Origem'].unique())

        icao_list = icao_list + icao_vra

    return remove_duplicates(icao_list)

def remove_duplicates(item_list):

    return list(dict.fromkeys(item_list))

def get_icao_data(icao_list):
    icao_data = []

    for icao in icao_list:

        params = {"icao":icao}
        response = requests.get(airport_url, headers=headers, params=params)

        icao_info = json.loads(response.text)

        #if there is info about the airport
        if icao_info.get("id") != None:
            icao_data.append(icao_info)

    return icao_data

def save_icao_data(data):

    df = pd.DataFrame(data)

    df.to_json(f"ICAO_FIX/icao_data", orient="records", force_ascii=False)

def treat_icao():

    icao_list = get_icao_list()
    #icao_list = icao_list[0:4]

    data = get_icao_data(icao_list)
    save_icao_data(data)

if __name__ == "__main__":
    if headers["X-RapidAPI-Key"] == "dummy_key" :
        print("change api key, exiting...")
        quit()
    else:
        create_save_folder(vra_directory)
        create_save_folder(air_cia_directory)
        create_save_folder(os.fsencode("./ICAO"))

        treat_vra()
        treat_air_cia()
        treat_icao()

    
    


