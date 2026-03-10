from tinydb import TinyDB, Query
import requests
import json
from ruamel.yaml import YAML
import re
from jproperties import Properties
from pathlib import Path
import time
import os



minecraft_subdomain_url_root = os.environ['EXTERNAL_PROXY_URL']
crafty_container_api_url = os.environ['CRAFTY_API_URL']
crafty_container_ip = os.environ['CRAFTY_CONTAINER_IP']
crafty_api_key = os.environ['CRAFTY_API_KEY']
start_port = os.environ['STARTING_PORT']
db_file_dir = '/app/servers.json'
gate_config_file_dir = '/app/config.yml'
path_to_server_dir = '/app/servers'


def update_gate(external_url, crafty_url,begin_port,gate_dir,servers_dir,db_dir,api_key,container_ip):


    db = TinyDB(db_dir)


    yaml = YAML()
    yaml.preserve_quotes = True
    
    gateconfig = {
        'config': {
            'lite': {
                'enabled': True,
                'routes': []
                }
            }
        }
    
    

    try:
        autheader = {'Authorization': api_key} #save auth token
    except Exception as error:
        print(f'error: {error}')
        #time.sleep(1000)
        exit()
    #print("------------")
    try:
        list_servers = requests.get(f'{crafty_url}/api/v2/servers', headers=autheader)
        servers_json = list_servers.json() #json formatted list of servers
    except Exception as error:
        print("Failed to get server list:", error)


    #setting server ports & saving to db
    index = 0
    servers_sub_dict = []
    for target_srv in servers_json['data']:
        srv_id = target_srv['server_id']
        srv_name = re.sub(r'[^a-zA-Z0-9]', '', target_srv['server_name'].replace(external_url, "")) #sanitise name input
        begin_port = int(begin_port)
        endpoint_url = f"{srv_name}.{external_url}" #combine into subdomain for server
        jconfigfile = Properties() #server.properties object
        print(f"detected {srv_name}")
        
        
        qry = Query()
        #srch = db.search(qry.id == srv_id)
    
        row_id = int(db.upsert({'id': srv_id, 'name': srv_name, 'port': begin_port ,'proxyurl':endpoint_url }, qry.id == srv_id)[0])
        if row_id != 1:
            new_port = begin_port + row_id
            db.update({'port':new_port}, doc_ids=[row_id])
        elif row_id == 1:
            new_port = begin_port

        
        file_path = Path(f"{servers_dir}/{srv_id}/server.properties")
        while file_path.is_file() != True: #wait for config file to exist
            time.sleep(1)

        with open(f"{servers_dir}/{srv_id}/server.properties", 'rb') as readf:
            jconfigfile.load(readf,"utf-8")
            jconfigfile["server-port"] = str(new_port) #update server port in server.properties file
            readf.close()

        with open(f"{servers_dir}/{srv_id}/server.properties", 'wb') as writef:
            jconfigfile.store(writef, encoding="utf-8")
            writef.close()
        
        
    
        
        new_server_name = {'server_name': endpoint_url}  
        try:
            requests.patch(f'{crafty_url}/api/v2/servers/{srv_id}', headers=autheader, data=json.dumps(new_server_name)) #update server name to match subdomain
        except Exception as error:
            print(f"Failed to update server name for {srv_name}:", error)
        
        #print(gateconfig)

        
        
        servers_sub_dict.insert(index,dict(host = endpoint_url, backend = f"{container_ip}:{new_port}")) #create sub dict for server in gate config file
        
      
        index = index + 1
    gateconfig['config']['lite']['routes'] = servers_sub_dict

    try:    
        with open(gate_dir, 'w') as file: #save gate config file
            yaml.dump(gateconfig, file)
            file.close
        print("Gate Config File Updated")
        
    except Exception as error:
        print("Config.yml Error:", error)
        
               
    print("Waiting for new changes...")
    index = 0









dir_depth = len(os.listdir(path_to_server_dir))
#print(dir_depth)
print("waiting for dir changes")
while True:
    if len(os.listdir(path_to_server_dir)) != dir_depth:
        dir_depth = len(os.listdir(path_to_server_dir))
        update_gate(minecraft_subdomain_url_root,crafty_container_api_url,start_port,gate_config_file_dir,path_to_server_dir,db_file_dir,crafty_api_key,crafty_container_ip)
    else:
        time.sleep(1)

