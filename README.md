# lusha-api
This script send requests to [Lusha Person API](https://www.lusha.com/docs/#person-api) to get client information

## Before
Install required dependencies :
```python
pip install -r requirements.txt
```

## Run the script
```python
python3 main.py /path/to/csv/file.csv
```

The `/path/to/csv/file.csv` should only contain 3 columns, in the required order :
```csv
company1,firstname1,lastname1
company2,firstname2,lastname2
...
```

The output format will be 
```csv
company1,firstname1,lastname1,phone1,
company2,firstname2,lastname2,phone1,phone2
...
```


## Update on July 18 2022
Recently Lusha updated their API with a bulk feature: [Lusha Person Bulk API](https://www.lusha.com/docs/#person-bulk-api)

Instead of `GET https://api.lusha.com/person?firstName=:firstName&lastName=:lastName&company=:company&property=phoneNumbers`,
`POST` request is used :
```python
POST https://api.lusha.com/person  -H api_key:API_KEY
{
 "filters":{
   "property": (optional, one of ("emailAddresses", "phoneNumbers"))
 },
 "contacts":[
  {
   "contactId": (required, unique, type string)
   "firstName": (required, type string),
   "lastName": (required, type string),
   "location": (optional, type object),
   "linkedinUrl": (optional, type string), 
   "companies": (required) [
    {
     "name": (required , type string, min_length=2),
     "domain": (optional, type string, min_length=4),
     "isCurrent":  (required, type bool),
     "jobTitle": (optional, type string, min_length=2)
     "fqdn": (optional, type string)
    }
   ]
  }
 ]
}
```