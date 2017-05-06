## TODO

#### New features
* Return type when ftp mode
* Directory navigation

#### Improvements
* Split to regex ? especially when split first line in GET
* OO and tests
* Headers and response body must be handle by cgi-bin
* Clean way to handle \n after headers when not cgi

## Configuration
### Property file
* **HTTP_ROOT**: Define the server HTTP_ROOT
* **BUFFER_SIZE**: The buffer size of the socket used to read client request
* **ADDRESS**: The address used by the server (keep localhost in the most of case)
* **PORT**: The port used by the server. If the port is lower than 1024, the server must run 
    with privilege
* **CGI-BIN_DIRECTORY**: The name of the cgi-bin directory. Outside this directory, cgi-bin will not be executed
    /!\ This directory must be inside HTTP_ROOT directory /!\
* **GET_ONLY_DIRECTORY**: The name of the GET only cgi-bin directory
    /!\ This directory must be inside CGI-BIN_DIRECTORY /!\
* **POST_ONLY_DIRECTORY**: The name of the POST only cgi-bin directory 
    /!\ This directory must be inside CGI-BIN_DIRECTORY /!\
* **DIRECTORY_INDEX**: The default file served if a directory is requested
* **INDEX_REDIRECT**: If the DIRECTORY_INDEX must be served when a directory is requested (True/False) 