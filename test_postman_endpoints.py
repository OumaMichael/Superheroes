import requests
import json

BASE_URL = "http://localhost:5555"

def test_postman_collection():
    print("🧪 Testing Postman Collection Endpoints\n")
    
    # Test 1: GET /heroes
    print("1. Testing GET /heroes")
    try:
        response = requests.get(f"{BASE_URL}/heroes")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            heroes = response.json()
            print(f"   ✅ Success: Found {len(heroes)} heroes")
            for hero in heroes[:3]:  # Show first 3
                print(f"      - {hero['name']} ({hero['super_name']})")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: GET /powers
    print("\n2. Testing GET /powers")
    try:
        response = requests.get(f"{BASE_URL}/powers")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            powers = response.json()
            print(f"   ✅ Success: Found {len(powers)} powers")
            for power in powers:
                print(f"      - {power['name']}: {power['description'][:50]}...")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: GET /heroes/1
    print("\n3. Testing GET /heroes/1")
    try:
        response = requests.get(f"{BASE_URL}/heroes/1")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            hero = response.json()
            print(f"   ✅ Success: Found hero '{hero['name']}'")
            print(f"      Super name: {hero['super_name']}")
            print(f"      Powers: {len(hero['hero_powers'])}")
            for hp in hero['hero_powers']:
                print(f"        - {hp['power']['name']} ({hp['strength']})")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: GET /powers/1
    print("\n4. Testing GET /powers/1")
    try:
        response = requests.get(f"{BASE_URL}/powers/1")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            power = response.json()
            print(f"   ✅ Success: Found power '{power['name']}'")
            print(f"      Description: {power['description']}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: POST /hero_powers (from Postman collection)
    print("\n5. Testing POST /hero_powers")
    try:
        payload = {
            "strength": "Average",
            "power_id": 1,
            "hero_id": 3
        }
        response = requests.post(f"{BASE_URL}/hero_powers", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Success: Created relationship")
            print(f"      Hero: {result['hero']['name']}")
            print(f"      Power: {result['power']['name']}")
            print(f"      Strength: {result['strength']}")
        elif response.status_code == 400:
            result = response.json()
            if "validation errors" in str(result.get('errors', [])):
                print("   ⚠️  Validation error (expected if relationship exists)")
            else:
                print(f"   ❌ Failed: {response.text}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: PATCH /powers/1 (from Postman collection)
    print("\n6. Testing PATCH /powers/1")
    try:
        payload = {
            "description": "Valid Updated Description"
        }
        response = requests.patch(f"{BASE_URL}/powers/1", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: Updated power")
            print(f"      Name: {result['name']}")
            print(f"      New Description: {result['description']}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 Postman Collection Testing Completed!")
    print("\n📋 Summary of tested endpoints:")
    print("   ✅ GET  /heroes")
    print("   ✅ GET  /powers")
    print("   ✅ GET  /heroes/<int:id>")
    print("   ✅ GET  /powers/<int:id>")
    print("   ✅ POST /hero_powers")
    print("   ✅ PATCH /powers/<int:id>")
    print("\n💡 These match exactly with your Postman collection!")

if __name__ == "__main__":
    try:
        test_postman_collection()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("   Make sure the server is running: python run.py")
    except Exception as e:
        print(f"❌ Error: {e}")
