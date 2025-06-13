import requests
import json

BASE_URL = "http://localhost:5555"

def test_validation_scenarios():
    print("🔍 Testing Validation Scenarios\n")
    
    # Test 1: Hero not found
    print("1. Testing GET /heroes/999 (non-existent hero)")
    response = requests.get(f"{BASE_URL}/heroes/999")
    print(f"   Status: {response.status_code}")
    if response.status_code == 404:
        result = response.json()
        print(f"   ✅ Correct: {result['error']}")
    else:
        print(f"   ❌ Unexpected: {response.text}")
    
    # Test 2: Power not found
    print("\n2. Testing GET /powers/999 (non-existent power)")
    response = requests.get(f"{BASE_URL}/powers/999")
    print(f"   Status: {response.status_code}")
    if response.status_code == 404:
        result = response.json()
        print(f"   ✅ Correct: {result['error']}")
    else:
        print(f"   ❌ Unexpected: {response.text}")
    
    # Test 3: Invalid hero_power creation
    print("\n3. Testing POST /hero_powers with invalid data")
    payload = {
        "strength": "Invalid",  # Invalid strength
        "power_id": 1,
        "hero_id": 1
    }
    response = requests.post(f"{BASE_URL}/hero_powers", json=payload)
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        result = response.json()
        print(f"   ✅ Correct validation error: {result['errors']}")
    else:
        print(f"   ❌ Unexpected: {response.text}")
    
    # Test 4: Missing required fields
    print("\n4. Testing POST /hero_powers with missing fields")
    payload = {
        "strength": "Strong"
        # Missing power_id and hero_id
    }
    response = requests.post(f"{BASE_URL}/hero_powers", json=payload)
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        result = response.json()
        print(f"   ✅ Correct validation error: {result['errors']}")
    else:
        print(f"   ❌ Unexpected: {response.text}")
    
    # Test 5: Invalid power description (too short)
    print("\n5. Testing PATCH /powers/1 with invalid description")
    payload = {
        "description": "Too short"  # Less than 20 characters
    }
    response = requests.patch(f"{BASE_URL}/powers/1", json=payload)
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        result = response.json()
        print(f"   ✅ Correct validation error: {result['errors']}")
    else:
        print(f"   ❌ Unexpected: {response.text}")
    
    print("\n✅ Validation testing completed!")

if __name__ == "__main__":
    try:
        test_validation_scenarios()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("   Make sure the server is running: python run.py")
    except Exception as e:
        print(f"❌ Error: {e}")
