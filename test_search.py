import requests
import json

BASE_URL = "http://localhost:5555"

def test_search_functionality():
    print("🔍 Testing Search and Filtering Functionality\n")
    
    # Test 1: Search heroes by name
    print("1. Searching heroes by name 'spider':")
    response = requests.get(f"{BASE_URL}/heroes?search=spider")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {data['total']} heroes")
        for hero in data['heroes']:
            print(f"   - {hero['name']} ({hero['super_name']})")
    print()
    
    # Test 2: Filter heroes by power
    print("2. Finding heroes with 'strength' powers:")
    response = requests.get(f"{BASE_URL}/heroes?power=strength")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {data['total']} heroes with strength powers")
        for hero in data['heroes']:
            print(f"   - {hero['name']} (matching powers: {hero.get('matching_powers', 'N/A')})")
    print()
    
    # Test 3: Search powers by description
    print("3. Searching powers by description containing 'fly':")
    response = requests.get(f"{BASE_URL}/powers?search=fly")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {data['total']} powers")
        for power in data['powers']:
            print(f"   - {power['name']}: {power['description'][:50]}...")
    print()
    
    # Test 4: Filter powers by minimum description length
    print("4. Finding powers with descriptions longer than 60 characters:")
    response = requests.get(f"{BASE_URL}/powers?min_desc_length=60")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {data['total']} powers")
        for power in data['powers']:
            print(f"   - {power['name']} (length: {power['description_length']})")
    print()
    
    # Test 5: Get hero-power relationships with filtering
    print("5. Finding 'Strong' hero-power relationships:")
    response = requests.get(f"{BASE_URL}/hero_powers?strength=Strong")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {data['total']} strong relationships")
        for hp in data['hero_powers'][:3]:  # Show first 3
            print(f"   - {hp['hero']['name']} has {hp['power']['name']} (Strong)")
    print()
    
    # Test 6: Advanced universal search
    print("6. Universal search for 'marvel':")
    response = requests.get(f"{BASE_URL}/search?q=marvel")
    if response.status_code == 200:
        data = response.json()
        results = data['results']
        
        if 'heroes' in results:
            print(f"   Heroes found: {len(results['heroes'])}")
            for hero in results['heroes']:
                print(f"   - {hero['name']} ({hero['super_name']})")
        
        if 'powers' in results:
            print(f"   Powers found: {len(results['powers'])}")
            for power in results['powers']:
                print(f"   - {power['name']}")
        
        if 'relationships' in results:
            print(f"   Relationships found: {len(results['relationships'])}")
    print()
    
    # Test 7: Pagination example
    print("7. Testing pagination (first 3 heroes):")
    response = requests.get(f"{BASE_URL}/heroes?limit=3&offset=0")
    if response.status_code == 200:
        data = response.json()
        print(f"   Showing {len(data['heroes'])} of {data['total_heroes']} total heroes")
        for hero in data['heroes']:
            print(f"   - {hero['name']}")
    print()
    
    # Test 8: Complex filtering
    print("8. Complex search: Heroes with 'super' powers at 'Average' strength:")
    response = requests.get(f"{BASE_URL}/heroes?power=super&strength=Average")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {data['total']} heroes matching criteria")
        for hero in data['heroes']:
            print(f"   - {hero['name']} (matching powers: {hero.get('matching_powers', 'N/A')})")
    
    print("\n✅ Search functionality testing completed!")

if __name__ == "__main__":
    try:
        test_search_functionality()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API. Make sure the server is running on localhost:5555")
    except Exception as e:
        print(f"❌ Error: {e}")
