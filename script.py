import requests

def fetch_substations(north, east, south, west):
    url = "https://overpass-api.de/api/interpreter"
    
    query = f"""
    [out:json][timeout:25];
    (
      node["power"="substation"]({south},{west},{north},{east});
      way["power"="substation"]({south},{west},{north},{east});
      relation["power"="substation"]({south},{west},{north},{east});
    );
    out center;
    """
    
    response = requests.post(url, data=query)
    
    if response.status_code == 200:
        data = response.json()
        return data["elements"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

north = input("Enter north-bound coordinate:")
east = input("Enter east-bound coordinate:")
south = input("Enter south-bound coordinate:")
west = input("Enter west-bound coordinate:")
provider = input("Is the provider AESO or ERCOT").upper()

if (provider is not "AESO" or provider is not "ERCOT"):
    return "Provider must be AESO or ERCOT"

substations = fetch_substations(north, east, south, west)

for item in substations:
    print(item["type"], item.get("id"), item.get("lat", item.get("center", {}).get("lat")), item.get("lon", item.get("center", {}).get("lon")))
