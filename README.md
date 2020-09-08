# scylla-search-demoapp

Demonstrate how to apply search feature to scylla 

## Setup

* make sure docker is install and working (we'll run scylla in docker)

```bash
# install python3.8 via pyenv
curl https://pyenv.run | bash
exec $SHELL
# go to: https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites
# and follow the instructions for your distribution, to install the prerequisites
# for compiling python from source
pyenv install 3.8.3

# create a virtualenv for SCT
pyenv virtualenv 3.8.3 sct38
pyenv activate sct38
pip install -r requirements.txt
```

Starting Scylla:
```bash
docker run -d -p 8080:8080 -p 9042:9042 --cpus="1" scylladb/scylla:4.1.0 --alternator-port 8080 --alternator-write-isolation always_use_lwt --smp 1
```

## Ingest imdb data
```bash
wget https://datasets.imdbws.com/title.basics.tsv.gz
wget https://datasets.imdbws.com/title.principals.tsv.gz
gunzip title.*

python ingest.py
```

# Run the app

```bash
python app.py
# browse to http://0.0.0.0:8000
```


