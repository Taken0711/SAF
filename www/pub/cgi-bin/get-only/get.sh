#!/bin/bash

echo "Content-type: text/html\n"
echo "<html>
    <head>
        <title>Junac - GET</title>
    </head>
    <body><h3>GET "
echo $QUERY_STRING
echo "</h3></body>
</html>"