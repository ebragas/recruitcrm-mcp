<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/26c003db63ed6-show-field-dependencies-for-all-entities -->
<!-- title: Show Field Dependencies for all Entities | API Endpoints -->

# Show Field Dependencies for all Entities

**GET** `/v1/nested-custom-fields`

Returns a list of all field dependencies associated with your account.

**Note** :
The parent field ID should be included in the payload of the Add/Edit endpoints for all entities to validate nested custom fields.

## Request

Security: Bearer Auth

### Query Parameters

- `dependency_id` (integer, optional) — Main (Top most) Parent Field ID to fetch the dependencies
- `entity_type` (string, optional) — Accepts 'contacts', 'candidates', 'companies', 'jobs', and 'deals'
- `field_id` (integer, optional) — Custom Field ID to fetch the related field dependencies

## Responses

200

401

### Body

array of:

- `field_id` (integer, optional) — Field ID (example: `1`)
- `field_name` (string, optional) — Field Name (example: `Industry`)
- `field_type` (string, optional) — Field Type (example: `dropdown`)
- `children` (optional) — array\[object\] Children of the Custom Field (example: `\[{"1":{"field\_id":7,"field\_name":"Sub Industry","field\_type":"dropdown","dependency":{"Health Care":"Hospitals, Clinics, Medical Labs"},"visibility":\[\],"children":\[\]}}\]`)
- `field_id` (integer, optional) — Field ID (example: `1`)
- `field_name` (string, optional) — Field Label (example: `Sub Industry`)
- `field_type` (string, optional) — Field Type (example: `dropdown`)
- `dependency` (object, optional)
- `Dependency` (optional) (example: `{"Health Care":"Hospitals, Clinics, Medical Labs"}`)
- `visibility` (object, optional)
- `Visibility` (optional) (example: `\[\]`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/nested-custom-fields \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
[
  {
    "field_id": 1,
    "field_name": "Industry",
    "field_type": "dropdown",
    "children": [
      {
        "1": {
          "field_id": 7,
          "field_name": "Sub Industry",
          "field_type": "dropdown",
          "dependency": {
            "Health Care": "Hospitals, Clinics, Medical Labs"
          },
          "visibility": [],
          "children": []
        }
      }
    ]
  }
]
```
