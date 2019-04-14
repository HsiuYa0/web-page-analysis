# web-page-analysis

## Usage
```shell
source webanalysis/bin/activate
```

Run server on 127.0.0.1:8000
```python3
python3 manage.py runserver
```
------

## API
Endpoint: 127.0.0.1:8000/analysis/  
Method: POST  
Parameters:  
* link `(string: query link)`

### Response
* `200` - OK, result dictionary  
* `400` - Bad request, error message  

### API Example
![alt text](https://github.com/HsiuYa0/web-page-analysis/blob/master/result1.png)  

![alt text](https://github.com/HsiuYa0/web-page-analysis/blob/master/result2.png)  

------
### Assumption and Solution 
Assume the valid input format is starting either http:// or https://.  
The server first try to connect the provided link, if failed, return 400.  
Otherwise, use BeautifulSoup to parse the html document.  

------
### Acknowledgement
Failed to use pymemcache to implement cache in django. Instead, use a dictionary to implement cache. Whenever there is a API call, service will update the cache first.



