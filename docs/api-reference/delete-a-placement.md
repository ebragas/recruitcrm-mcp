<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/66a18c8b3b6e8-delete-a-placement -->
<!-- title: Delete a placement | API Endpoints -->

# Delete a placement

**DELETE** `/v1/placements/{placement}`

Delete a placement.

## Request

Security: Bearer Auth

### Path Parameters

- `placement` (integer, **required**) — ID of the placement (placement\_srno) to delete

## Responses

200

401

404

### Body

- `message` (string, optional) (example: `Deleted Successfully`)

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/placements/{placement} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```

#### Example response

#### Example response

```
{
  "message": "Deleted Successfully"
}
```
