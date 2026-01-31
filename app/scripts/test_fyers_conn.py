import requests
import sys

def test_connectivity(url="https://www.fyers.in", user_agent=None):
    headers = {}
    if user_agent:
        headers["User-Agent"] = user_agent
    else:
        # Default requests UA is often blocked
        pass

    print(f"Testing connectivity to {url} with headers: {headers}")
    try:
        # Use a timeout of 10 seconds
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Successfully connected!")
        elif response.status_code == 403:
            print("Access Blocked (403 Forbidden) - Likely Cloudflare")
            if "Cloudflare" in response.text or "ray-id" in response.text.lower():
                print("Confirmed: Blocked by Cloudflare Security.")
        else:
            print(f"Received unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"Error connecting: {e}")

if __name__ == "__main__":
    print("--- Test 1: Default (Requests UA) ---")
    test_connectivity()
    
    print("\n--- Test 2: Chrome User-Agent ---")
    chrome_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    test_connectivity(user_agent=chrome_ua)
