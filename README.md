# Gloat Home Task


## usage:
- install requirements for requirements.txt
- python gloat_integrations.py

## app flow:
the main process, starts 2 subprocesses, and signals them to start pull periodically data from local upload folder, it than goes on and starts the flask server which services authenticated clients for adding users to whitelist

## main module and libs:

- common: common features
- listeners: there are file and client libs, each is intended to contain specific file/client listeners and mapping classes
- mapping: the module that is owner of matching raw data to gloat user fields. each listener should have a mapper implementation
- listener_base.py: owner of scheduling the listening task. abstract logics to be inherited with mapping and raw data fetching capabilities

