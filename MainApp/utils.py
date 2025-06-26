import requests

def get_location_info():
    try:
        #response = requests.get("http://ip-api.com/json/")
        # response.raise_for_status()
        # data = response.json()

        # country_code = data.get("countryCode", "N/A")

        # currency_map = {
        #     'US': '$',
        #     'IN': '₹',
        #     'NP': 'रु',
        #     'GB': '£',
        #     'EU': '€',
        #     'CA': 'C$',
        #     'AU': 'A$',
        #     'CN': '¥',
        #     'JP': '¥',
        #     'BD': '৳',
        # }

        # currency_symbol = currency_map.get(country_code, '$')

        location = {
            "city":'ktm',
            "region":'kathmandu',
            "country":'NP',
            "currency_symbol": 'रु'
        }

        return location

    except requests.RequestException as e:
        print("Error fetching location:", e)
        return {
            "city": "N/A",
            "region": "N/A",
            "country": "N/A",
            "currency_symbol": "$"
        }
