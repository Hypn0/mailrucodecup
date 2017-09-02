#!/bin/bash

sudo docker build --tag=mailru .
sudo docker tag mailru stor.highloadcup.ru/travels/wombat_runner
sudo docker push stor.highloadcup.ru/travels/wombat_runner

