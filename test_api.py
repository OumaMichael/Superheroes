import requests
import json

BASE_URL = "http://localhost:5555"

def test_basic_endpoints():
    print("🧪 Testing Basic API Endpoints\n")
    
    # Test 1: Get all heroes
    print("1. Testing GET /heroes")
    try:
        response = requests.get(f"{BASE_URL}/heroes")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: Found {len(data.get('heroes', data))} heroes")
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get all powers
    print("\n2. Testing GET /powers")
    try:
        response = requests.get(f"{BASE_URL}/powers")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: Found {len(data.get('powers', data))} powers")
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Get specific hero
    print("\n3. Testing GET /heroes/1")
    try:
        response = requests.get(f"{BASE_URL}/heroes/1")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: Found hero '{data.get('name')}' with {len(data.get('hero_powers', []))} powers")
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Search functionality
    print("\n4. Testing GET /heroes?search=marvel")
    try:
        response = requests.get(f"{BASE_URL}/heroes?search=marvel")
        if response.status_code == 200:
            data = response.json()
            heroes_count = len(data.get('heroes', []))
            print(f"   ✅ Success: Found {heroes_count} heroes matching 'marvel'")
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Create hero power relationship
    print("\n5. Testing POST /hero_powers")
    try:
        payload = {
            "strength": "Average",
            "power_id": 1,
            "hero_id": 3
        }
        response = requests.post(f"{BASE_URL}/hero_powers", json=payload)
        if response.status_code in [200, 201]:
            print("   ✅ Success: Created hero-power relationship")
        elif response.status_code == 400:
            data = response.json()
            if "already exists" in str(data.get('errors', [])):
                print("   ✅ Success: Relationship already exists (expected)")
            else:
                print(f"   ❌ Failed: {data}")
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_basic_endpoints()
