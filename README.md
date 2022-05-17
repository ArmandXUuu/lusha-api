# lusha-api
This script send requests to Lusha API to get client information

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
