# Search and Filtering API Documentation

This document describes the advanced search and filtering capabilities of the Superhero API.

## Overview

The API supports comprehensive search and filtering across all endpoints using query parameters. You can search by text, filter by relationships, and combine multiple criteria.

## Heroes Endpoint (`/heroes`)

### Basic Search
- `search` - Search heroes by name or super_name
- `power` - Filter heroes who have powers containing this text
- `strength` - Filter heroes by power strength level (Strong, Weak, Average)

### Pagination
- `limit` - Maximum number of results to return
- `offset` - Number of results to skip

### Examples
\`\`\`
GET /heroes?search=spider
GET /heroes?power=flight&strength=Strong
GET /heroes?search=marvel&limit=5&offset=0
\`\`\`

### Response Format
\`\`\`json
{
  "heroes": [...],
  "total": 3,
  "total_heroes": 10,
  "filters_applied": {
    "search": "spider",
    "power": "",
    "strength": "",
    "limit": null,
    "offset": 0
  }
}
\`\`\`

## Individual Hero Endpoint (`/heroes/<id>`)

### Filters
- `power` - Filter hero's powers containing this text
- `strength` - Filter hero's powers by strength level

### Examples
\`\`\`
GET /heroes/1?power=flight
GET /heroes/1?strength=Strong
\`\`\`

## Powers Endpoint (`/powers`)

### Search and Filters
- `search` - Search powers by name or description
- `hero` - Filter powers possessed by heroes matching this text
- `strength` - Filter powers by strength level when possessed
- `min_desc_length` - Filter powers with description longer than specified length

### Pagination
- `limit` - Maximum number of results
- `offset` - Number of results to skip

### Examples
\`\`\`
GET /powers?search=strength
GET /powers?hero=spider&strength=Strong
GET /powers?min_desc_length=50&limit=10
\`\`\`

### Response Format
\`\`\`json
{
  "powers": [...],
  "total": 2,
  "total_powers": 4,
  "filters_applied": {
    "search": "strength",
    "hero": "",
    "strength": "",
    "min_desc_length": null,
    "limit": null,
    "offset": 0
  }
}
\`\`\`

## Individual Power Endpoint (`/powers/<id>`)

### Options
- `include_heroes` - Set to "true" to include heroes who have this power
- `hero` - Filter included heroes by name/super_name
- `strength` - Filter included heroes by strength level

### Examples
\`\`\`
GET /powers/1?include_heroes=true
GET /powers/1?include_heroes=true&strength=Strong
GET /powers/1?include_heroes=true&hero=spider
\`\`\`

## Hero Powers Endpoint (`/hero_powers`)

### New GET Endpoint for Filtering Relationships
- `hero_id` - Filter by specific hero ID
- `power_id` - Filter by specific power ID
- `strength` - Filter by strength level
- `hero_search` - Search heroes by name/super_name
- `power_search` - Search powers by name/description

### Pagination
- `limit` - Maximum number of results
- `offset` - Number of results to skip

### Examples
\`\`\`
GET /hero_powers?strength=Strong
GET /hero_powers?hero_search=spider&power_search=strength
GET /hero_powers?hero_id=1&limit=5
\`\`\`

### Response Format
\`\`\`json
{
  "hero_powers": [...],
  "total": 5,
  "total_relationships": 15,
  "filters_applied": {
    "hero_id": null,
    "power_id": null,
    "strength": "Strong",
    "hero_search": "",
    "power_search": "",
    "limit": null,
    "offset": 0
  }
}
\`\`\`

## Advanced Search Endpoint (`/search`)

### Universal Search Across All Entities
- `q` - Search query (required)
- `type` - Search type: "all", "heroes", "powers", "relationships"
- `limit` - Maximum results per category (default: 10)

### Examples
\`\`\`
GET /search?q=spider
GET /search?q=flight&type=powers
GET /search?q=strong&type=relationships&limit=5
\`\`\`

### Response Format
\`\`\`json
{
  "query": "spider",
  "search_type": "all",
  "results": {
    "heroes": [
      {
        "id": 3,
        "name": "Gwen Stacy",
        "super_name": "Spider-Gwen",
        "powers_count": 2
      }
    ],
    "powers": [],
    "relationships": [
      {
        "id": 5,
        "hero_name": "Gwen Stacy",
        "hero_super_name": "Spider-Gwen",
        "power_name": "super strength",
        "strength": "Average"
      }
    ]
  }
}
\`\`\`

## Search Tips

1. **Case Insensitive**: All text searches are case-insensitive
2. **Partial Matching**: Searches use partial matching (contains)
3. **Combine Filters**: Most endpoints support combining multiple filters
4. **Pagination**: Use limit and offset for large result sets
5. **Metadata**: Responses include filter information and totals

## Common Use Cases

### Find all heroes with flight powers
\`\`\`
GET /heroes?power=flight
\`\`\`

### Search for powers related to strength
\`\`\`
GET /powers?search=strength
\`\`\`

### Find strong relationships for Spider heroes
\`\`\`
GET /hero_powers?hero_search=spider&strength=Strong
\`\`\`

### Universal search for anything related to "marvel"
\`\`\`
GET /search?q=marvel
\`\`\`

### Get heroes with pagination
\`\`\`
GET /heroes?limit=5&offset=10
