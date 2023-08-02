import requests


def get_location_info(latitude, longitude):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "address" in data:
            city = data["address"].get("city", "")
            address = data["display_name"]
            return city, address
        else:
            return None, None

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None, None
