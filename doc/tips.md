
### make app.run serve static files
#### related issues
* app.static_url_path  
* app.static_folder  
* app.add_url_rule (for static)  
* app.send_static_file  
* app.send_from_directory  
* app.url_map  
    default Rule for static files is "<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>]"


##### solution 1
> app = Flask(__name__, static_url_path='static', static_folder='static')  


