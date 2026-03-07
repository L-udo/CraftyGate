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
crafty_container_hostname = f"https://{os.environ['CRAFTY_CONTAINER_HOSTNAME']}"
crafty_username = os.environ['CRAFTY_USERNAME']
crafty_password = os.environ['CRAFTY_PASSWORD']
start_port = os.environ['STARTING_PORT']
db_file_dir = 'servers.json'
gate_config_file_dir = 'config.yml'
path_to_server_dir = 'servers'


def update_gate(external_url, crafty_url,username,password,begin_port,gate_dir,servers_dir,db_dir):


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
    
    


    authpayload = {'username':username, 'password':password}

    craftyapi_auth = requests.post(f'{crafty_url}/api/v2/auth/login', data=json.dumps(authpayload)) #request auth token
    try:
        autheader = {'Authorization': craftyapi_auth.json()['data']['token']} #save auth token
    except:
        print(f'error: {craftyapi_auth}')
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

        #gateconfig['config']['lite']['routes'].append(dict(host = endpoint_url, backend = f"{crafty_url}:{srv_port}"))
        
        servers_sub_dict.insert(index,dict(host = endpoint_url, backend = f"{crafty_url}:{new_port}")) #create sub dict for server in gate config file
        
        #gateconfig['config']['lite']['routes'].append(dict(backend = f"{crafty_url}:{srv_port}")) #write to gate config file obj
        index = index + 1
    gateconfig['config']['lite']['routes'] = servers_sub_dict
    #print(servers_sub_dict)
    try:    
        with open(gate_dir, 'w') as file: #save gate config file
            yaml.dump(gateconfig, file)
            file.close
        print("Gate Config File Updated")
        
    except Exception as error:
        print("Config.yml Error:", error)
        
    requests.post(f'{crafty_url}/api/v2/auth/invalidate_tokens', headers=autheader) #invalidate auth token

               
    print("Waiting for new changes...")
    index = 0









dir_depth = len(os.listdir(path_to_server_dir))
#print(dir_depth)
print("waiting for dir changes")
while True:
    if len(os.listdir(path_to_server_dir)) != dir_depth:
        dir_depth = len(os.listdir(path_to_server_dir))
        update_gate(minecraft_subdomain_url_root,crafty_container_hostname,crafty_username,crafty_password,start_port,gate_config_file_dir,path_to_server_dir,db_file_dir)
    else:
        time.sleep(1)


update_gate(minecraft_subdomain_url_root,crafty_container_hostname,crafty_username,crafty_password,start_port,db_file_dir,gate_config_file_dir,path_to_server_dir)
#observer = Observer()
#observer.schedule(event_handler, path_to_server_dir, recursive=True)
#observer.start()
#try:
#    while True:
#        time.sleep(1)
#finally:
#    observer.stop()
#    observer.join()

















"""




index = 0
for target_srv in servers_json['data']:
    srv_id = target_srv['server_id']
    srv_name = re.sub(r'[^a-zA-Z0-9]', '', target_srv['server_name'].replace(external_url, "")) #sanitise name input
    srv_port = target_srv['server_port']
    endpoint_url = f"{srv_name}.{external_url}"
    #print(target_srv)
    #print(gateconfig['config']['lite']['routes'][index]) 
    gateconfig['config']['lite']['routes'][index]['backend'] = f"{crafty_url}:{srv_port}"
    gateconfig['config']['lite']['routes'][index]['host'] = endpoint_url
    index = index + 1
     
    #change_port = requests.patch(f'{crafty_url}/api/v2/servers/{srv_id}', headers=autheader, data=json.dumps()


    #print(change_port.text)
    #qry = Query()
    #srch = db.search(qry.id == srv_id)

    #db.upsert({'id': srv_id, 'name': srv_name, 'port':srv_port,'proxyurl':'urltest' }, qry.id == srv_id)
    
    
    
    
    
    
    
print("###################")
print(gateconfig)
#with open('config.yml', 'w') as file:
#    yaml.dump(gateconfig, file)



#for hostss in gateconfig['config']['lite']['routes']:
#    print(hostss['host'])
#    print(hostss['backend'])

#gateconfig


#gate_template ={'backend': "10.0.0.7:25567",'host': "soakedry.mc.publicsrv.furmegle.com"}


#with open('testTEMPLACE.yaml', 'w') as template_file:
#        yaml.dump_all(gate_template,template_file, sort_keys=False)



invalidate_auth = requests.post(f'{crafty_url}/api/v2/auth/invalidate_tokens', headers=autheader)

print(invalidate_auth.text)


#print("++++++++++++")
#print(len(list_servers.json()['data']))
#print("++++++++++++")



    #if len(srch) == 1:
    #    db.update({'name': srv_name,'port':srv_port,'proxyurl':'url tests'}, srch)
    #else:
        #db.insert({'id':srv_id,'name': srv_name,'port':srv_port,'proxyurl':'url tests'})

    #print(srch , len(srch))
    #db.insert({'id':srv_id,'name': srv_name,'port':srv_port,'proxyurl':'url tests'})
    #db.update({'id':srv_id,'name': srv_name,'port':srv_port,'proxyurl':'url tests'}, db.search( id == srv_id))
    #print(srv_name)

#print(list_servers.json())






#db.insert({'id':'idd test','port':'porttest','proxyurl':'url tests'})



#print(db.all())"""