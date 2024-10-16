# Hawk - Get a good view into your data pipeline!
Hawk consists of mainly two components: a library for logging data which is processed in your pipeline and an UI which provides insights into a pipeline run.

## Data logging
Clone the repository locally with 
```
git clone https://github.com/bastistrasser/hawk.git
```

To install the library via pip, type
```
pip install <local_hawk_path>
```

An example usage of the logging functionality is demonstrated [here](./examples/data_logging.py). 

## Transparency dashboard
There are three components needed for the dashboard, namely the MongoDB database, the [backend](./server/api) and [frontend](./server/ui). We recommend to use the provided [docker-compose.yml](./docker-compose.yml) file.