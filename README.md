# web-page-analysis

## Usage
```shell
source webanalysis/bin/activate
```

Run server on 127.0.0.1:8000
```python3
python3 manage.py runserver
```
====

## API
Endpoint: 127.0.0.1:8000/analysis/
Method: POST
Parameters:
..* link `(string: query link)`

### Response
..* `200` - OK
..* `400` - Bad request with error message

### API Example
```
POST http://127.0.0.1:8000/analysis/ 
```

====
### Acknowledgement
Failed to use pymemcached


