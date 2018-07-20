import yaml

# assign env yaml file
env_filename = "./config/env.yml"

# if run from console, then
if __name__ == "__main__":
    env_filename = "env.yml"
    #print(env_filename)

with open(env_filename, 'r') as envfile:
    cfg = yaml.load(envfile)

#for section in cfg:
#    print(section)
#print(cfg['ENV'])

################# API URL #################
download_url = "https://data.cityofnewyork.us/resource/9w7m-hzhe.json?inspection_date="

################# App Data Download Location #################
download_root_folder = "/opt/app/python/app/restaurant_recommendation"

download_restaurant_file_pattern = "restaurant_data"
download_restaurant_log_pattern = "restaurant_log"

find_restaurant_file_pattern = "find_rest_data"
save_restaurant_log_pattern = "save_rest_data"


################# Environment #################
db_config = None
if cfg['ENV'] == "PROD":
    db_config = {
    "host": "",
    "database_name" : "",
    "username" : "",
    "password" : "",
    "port" : ""
    }
elif cfg['ENV'] == "STAGING":
    db_config = {
    "host": "",
    "database_name" : "",
    "username" : "",
    "password" : "",
    "port" : ""
    }
elif cfg['ENV'] == "CI":
    db_config = {
    "host": "",
    "database_name" : "",
    "username" : "",
    "password" : "",
    "port" : ""
    }
else:
    db_config = {
    "host": "rest_recomm_dev",
    "database_name": "restaurantdb",
    "username": "restuser",
    "password": "restuser",
    "port": "3306"
}
    #print(db_config)
