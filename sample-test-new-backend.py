import requests
import json

# Function to fetch Firebase Remote Config
def fetch_firebase_config():
    url = "https://firebaseremoteconfig.googleapis.com/v1/projects/golf-blitz-1/namespaces/firebase:fetch?key=AIzaSyDITwReyJWEpyldvWkIeBKizoyziCDTlvQ"
    headers = {'Content-Type': 'application/json'}
    
    # Include the payload as per your requirements
    payload = {
        "app_instance_id": 'cV6rgj2Qek1ZoaVSfgH_h0',
        "app_instance_id_token": 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IjE6NTk3NDU1NTU4ODk2Omlvczo3YjQ4MDA2MjEzNjZiNDYwIiwiZXhwIjoxNzI1NDg0NTQ1LCJmaWQiOiJjVjZyZ2oyUWVrMVpvYVZTZmdIX2gwIiwicHJvamVjdE51bWJlciI6NTk3NDU1NTU4ODk2fQ.AB2LPV8wRQIgeEHFKR7P1f6lIUoMV_Ew6HAdNr8KYTY6I8JB0lN_9v0CIQDydzdVhZXd38Xe-tYM7ugIEfxfSfHrYVNEZkQuE0UCIQ',
        "app_id": '1:597455558896:ios:7b4800621366b460',
        "country_code": 'mk',
        "language_code": 'en_GB',
        "platform_version": '17.5.1',
        "time_zone": 'Europe/Skopje',
        "package_name": 'com.noodlecake.ssg4',
        "app_version": '3.8.11',
        "app_build": '475',
        "sdk_version": '10.9.0',
        "first_open_time": '2024-08-28T22:00:00Z',
        "analytics_user_properties": {
            "bux_by_basket": "100-1k",
            "level": "1.000000",
            "gem_by_basket": "100-500",
            "starpass_purchased_count": "0",
            "trophies_by_basket": "0-249"
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        print("Fetched Firebase config:", data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch Firebase config: {e}")
        return None

# Function to authenticate with BrainCloud
def authenticate_with_braincloud():
    url = "https://api.braincloudservers.com/dispatcherv2"
    headers = {
        'Content-Type': 'application/json',
        # Add any required Authorization headers here if needed
        # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
    }
    payload = {
        "gameId": "13726",
        "messages": [{
            "data": {
                "anonymousId": "cf53f717-e817-4af9-a9e2-226781741e30",
                "authenticationToken": "",  # Ensure this is correctly populated if needed
                "authenticationType": "Anonymous",
                "clientLib": "cpp",
                "clientLibVersion": "4.14.0",
                "countryCode": "MK",
                "externalId": "cf53f717-e817-4af9-a9e2-226781741e30",
                "extraJson": {
                    "client_version": 242,
                    "game_version": 1,
                    "gamesparks_auth_data": {
                        "device_id": "FB969A95-93A1-4D5A-87A5-D2A6C4C46FDA",
                        "device_os": "IOS",
                        "user_id": ""
                    }
                },
                "forceCreate": False,
                "gameId": "13726",
                "gameVersion": "3.8.11 (475)",
                "languageCode": "en",
                "profileId": "30a4cee8-116e-4793-ac56-00f6fb3807d4",
                "releasePlatform": "IOS",
                "timeZoneOffset": 2
            },
            "operation": "AUTHENTICATE",
            "service": "authenticationV2"
        }],
        "packetId": 0,
        "sessionId": ""
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print("Authentication response:", data)
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.text:
            print("Response text:", response.text)
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return None

# Main function to coordinate both operations
def main():
    # Fetch Firebase Remote Config
    firebase_config = fetch_firebase_config()
    
    if firebase_config:
        # Perform BrainCloud Authentication if Firebase config is successfully fetched
        authenticate_with_braincloud()

if __name__ == "__main__":
    main()
