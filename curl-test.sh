#!/bin/bash

curl --request GET 127.0.0.1:5000/api/timeline_post

curl --request POST http://localhost:5000/api/timeline_post -d 'name=Carlitos&email=cs@gmail.com&content=testingbash'

curl --request POST http://localhost:5000/api/timeline_post -d 'name=Dummy&email=ds@gmail.com&content=Another content'

curl --request GET 127.0.0.1:5000/api/timeline_post