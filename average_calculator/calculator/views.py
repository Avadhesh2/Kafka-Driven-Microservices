from django.http import JsonResponse
import requests

WINDOW_SIZE = 10
TIMEOUT = 0.5

numbers_window = []

TEST_SERVER_URLS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}

# Replace 'your_existing_token_here' with your actual authorization token
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE3MjE5MjE2LCJpYXQiOjE3MTcyMTg5MTYsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjUwMGJhMjRlLTEwNWQtNGRkOC1hN2NiLWMwZGE4ODU4YmE5ZiIsInN1YiI6ImF5dXNoaS4yMTI1Y3NhaTEwNjRAa2lldC5lZHUifSwiY29tcGFueU5hbWUiOiJnb01hcnQiLCJjbGllbnRJRCI6IjUwMGJhMjRlLTEwNWQtNGRkOC1hN2NiLWMwZGE4ODU4YmE5ZiIsImNsaWVudFNlY3JldCI6InNiUXZvZnluc3FwaXdNZUgiLCJvd25lck5hbWUiOiJBeXVzaGkgQ2hvdWhhbiIsIm93bmVyRW1haWwiOiJheXVzaGkuMjEyNWNzYWkxMDY0QGtpZXQuZWR1Iiwicm9sbE5vIjoiMjEwMDI5MTUyMDAyNCJ9.nBps2UY6kDtqbE3J6g6OxOSKE3FLDp_r0Y8lFhhfb18"

def fetch_numbers(numberid):
    url = TEST_SERVER_URLS.get(numberid)
    if not url:
        return []

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        print("Response from test server:", data) 
        return data.get('numbers', [])
    except (requests.RequestException, ValueError) as e:
        print("Error fetching numbers:", e) 
        return []
def calculate_average(numbers):
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

def get_numbers(request, numberid):
    if numberid not in ['p', 'f', 'e', 'r']:
        return JsonResponse({"error": "Invalid number ID"}, status=400)

    new_numbers = fetch_numbers(numberid)
    unique_new_numbers = list(set(new_numbers))

    window_prev_state = numbers_window.copy()

    # Add new numbers while maintaining window size
    for number in unique_new_numbers:
        if number not in numbers_window:
            if len(numbers_window) >= WINDOW_SIZE:
                numbers_window.pop(0)
            numbers_window.append(number)

    window_curr_state = numbers_window.copy()
    average = calculate_average(numbers_window)

    return JsonResponse({
        "numbers": new_numbers,
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "avg": round(average, 2)
    }, status=200)
