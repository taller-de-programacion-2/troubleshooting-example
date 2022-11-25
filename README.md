# Ejemplo de troubleshooting
Ejemplo para ver tipos de métricas de aplicación y cómo varían en el tiempo según el tráfico entrante.



## Setup
* Setear ```DD_API_KEY``` en el archivo ```docker-compose.yml```
* Instalar ```make```, ```docker``` y ```docker-compose```

## Uso
1. ```make start_api``` levanta la aplicación.
2. ```make start_traffic``` levanta locust, la cual nos permite setear cuantos usuarios queremos simular y el tiempo de arribo de cada uno de ellos.

3. ```make stop_api``` para detener la aplicacion

## Dashboard
El dashboard de datadog se puede importar del archivo ```/datadog/dashboard.json```

