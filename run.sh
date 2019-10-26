#!/bin/sh

docker run --rm -it -v $(pwd):/work -v $(pwd)/google-ads.yaml:/root/google-ads.yaml co-ads python -m unittest discover tests
docker run --rm -v $(pwd):/work co-ads autopep8 -r --in-place tests coads 
