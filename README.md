### How To?

### prerequisites

* docker 
* docker-compose 

### Commands 

```bash
docker-compose build 
docker-compose up -d
```

#### URLS
Airflow url - http://0.0.0.0:19000/home
Spark-cluster - http://0.0.0.0:9010/

#### Screen shots 

**Airflow UI**
![alt text](src/image.png)

**Spark UI**
![alt text](src/spark-ui.png)

**Variable list**

oracle password you can get from dbt_integration/.dbt/profiles.yml

sender_email and sender_password is configured from google smtp settings

![alt text](src/variable_list.png)

**Connection list**
###### dbt-container ssh connection 

![alt text](src/connection-1.png)

###### spark-master ssh connection 

![alt text](src/connection-2.png)

###### oracle db ssh connection 

![alt text](src/connection-3.png)

###### Spark connection 

![alt text](src/spark-conn.png)


###### Postman Connection 

![Postman Collection](src/postman_collection.png)