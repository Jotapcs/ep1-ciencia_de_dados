import requests
from bs4 import BeautifulSoup
import json

def extract_pokemon_info(pokemon_url):
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        pokemon_info = {
            "Número": soup.find("span", class_="num").text.strip("#"),  # Remove o símbolo # do número
            "URL da página": pokemon_url,
            "Nome": soup.find("h1").text,
            "Tamanho": soup.find(text="Height").find_next("td").text.strip(),
            "Peso": soup.find(text="Weight").find_next("td").text.strip(),
            "Tipos": [type.text.strip() for type in soup.find_all("a", class_="itype")],
            # Extrair outras informações aqui...
        }
        
        # Extrair habilidades
        abilities_section = soup.find(text="Abilities").find_next("table")
        abilities = []
        for ability_row in abilities_section.find_all("tr")[1:]:
            ability_data = ability_row.find_all("td")
            ability_info = {
                "URL da página": base_url + ability_data[0].find("a")["href"],
                "Nome": ability_data[0].find("a").text.strip(),
                "Descrição do efeito": ability_data[1].text.strip(),
            }
            abilities.append(ability_info)
        
        pokemon_info["Habilidades"] = abilities
        
        return pokemon_info
    else:
        print("Falha ao obter a página do Pokémon:", response.status_code)

base_url = "https://pokemondb.net"
page_url = base_url + "/pokedex/all"
response = requests.get(page_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    pokemon_links = []

    for link in soup.find_all("a", class_="ent-name"):
        pokemon_links.append(base_url + link.get("href"))

    pokemon_data_list = []

    for pokemon_url in pokemon_links:
        pokemon_data = extract_pokemon_info(pokemon_url)
        pokemon_data_list.append(pokemon_data)

    with open("pokemon_data.json", "w") as json_file:
        json.dump(pokemon_data_list, json_file, indent=4)
else:
    print("Falha ao obter a página:", response.status_code)