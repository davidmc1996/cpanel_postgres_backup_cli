import click
import os
import json
import time
from pathlib import Path
from datetime import datetime
from handler import Handler

def validate_json(data):
    if 'servers' not in data:
        return False, "'servers' es requerido."
    if not isinstance(data['servers'], list) or not data['servers']:
        return False, "'servers' debe ser una lista no vacía."
    
    for server in data['servers']:
        if 'name' not in server:
            return False, "Cada 'server' debe tener un 'name'."
        if not isinstance(server['name'], str):
            return False, "'name' debe ser una cadena de texto."
        
        if 'host' not in server:
            return False, "Cada 'server' debe tener un 'host'."
        if not isinstance(server['host'], str):
            return False, "'host' debe ser una cadena de texto."
        
        default_port = server.get('defaultPortDatabases')
        default_user = server.get('defaultUserDatabases')
        default_password = server.get('defaultPasswordDatabases')
        
        if default_port is not None and not isinstance(default_port, int):
            return False, "'defaultPortDatabases' debe ser un entero."
        if default_user is not None and not isinstance(default_user, str):
            return False, "'defaultUserDatabases' debe ser una cadena de texto."
        if default_password is not None and not isinstance(default_password, str):
            return False, "'defaultPasswordDatabases' debe ser una cadena de texto."
        
        if 'databases' not in server:
            return False, "Cada 'server' debe tener una lista de 'databases'."
        if not isinstance(server['databases'], list) or not server['databases']:
            return False, "'databases' debe ser una lista no vacía."
        
        for db in server['databases']:
            if 'name' not in db:
                return False, "Cada 'database' debe tener un 'name'."
            if not isinstance(db['name'], str):
                return False, "'name' debe ser una cadena de texto."

            if default_port is not None and db.get('port') is not None and not isinstance(db.get('port'), int):
                return False, "'port' debe ser un entero"
            elif default_port is None and db.get('port') is not None and not isinstance(db.get('port'), int):
                return False, "'port' debe ser un entero"
            elif default_port is None and db.get('port') is None:
                return False, "Cada 'database' debe tener un 'port'."

            if default_user is not None and db.get('user') is not None and not isinstance(db.get('user'), str):
                return False, "'user' debe ser un entero"
            elif default_user is None and db.get('user') is not None and not isinstance(db.get('user'), str):
                return False, "'user' debe ser un entero"
            elif default_user is None and db.get('user') is None:
                return False, "Cada 'database' debe tener un 'user'."

            if default_password is not None and db.get('password') is not None and not isinstance(db.get('password'), str):
                return False, "'password' debe ser un entero"
            elif default_password is None and db.get('password') is not None and not isinstance(db.get('password'), str):
                return False, "'password' debe ser un entero"
            elif default_password is None and db.get('password') is None:
                return False, "Cada 'database' debe tener un 'password'."
    
    return True, "El JSON es válido."


@click.command()
@click.option('--json_file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True), required=True, help="Ruta del archivo JSON que se va a respaldar.")
@click.option('--backup_path', type=click.Path(file_okay=False, dir_okay=True, writable=True), required=True, help="Ruta del directorio donde se guardará el respaldo.")
@click.option('--output', type=click.Choice(['plain', 'zip'], case_sensitive=False), default='plain', required=True, help="Formato de salida del respaldo: 'plain' para archivos .sql o 'zip' para archivos comprimidos.")
@click.option('--type', type=click.Choice(['data', 'structure', 'structuredata'], case_sensitive=False), default='structuredata', required=True, help="Tipo de respaldo: 'data' para datos, 'structure' para estructura o 'structuredata' para datos y estructura")
@click.option('--format', type=click.Choice(['sql', 'copy'], case_sensitive=False), default='structuredata', required=True, help="Tipo de formato: 'sql' para generar un script de secuencias sql o 'copy' para un archivo de texto con los datos en un formato delimitado")
def cli(json_file, backup_path, output, type, format):
    """
    Comando que realiza un respaldo de bases de datos postgres.

    --json_file: Ruta del archivo JSON con los datos de conexión.
    --backup_path: Ruta del directorio donde se guardarán los respaldos.
    --output: Formato de salida del respaldo: plain para archivos .sql o zip para archivos comprimidos .gz.
    --type: Tipo de respaldo: data para datos, structure para estructura, structuredata para ambos.
    --format: Formato del respaldo: sql para generar un script de SQL o copy para un archivo de texto con datos delimitados.
    
    """
    
    start_time = time.time()

    json_file = Path(json_file)
    backup_path = Path(backup_path)

    if not json_file.exists():
        click.echo(f"Error: La ruta '{json_file}' no existe.")
        return

    if not backup_path.exists():
        click.echo(f"Error: La ruta '{backup_path}' no existe.")
        return

    try:
        with open(json_file, 'r') as file:
                data = json.load(file)
            
        is_valid, message = validate_json(data)

        if not is_valid:
            click.echo(f"Error: {message}")
            return

        for server in data['servers']:
            default_port = server.get('defaultPortDatabases', '')
            default_user = server.get('defaultUserDatabases', '')
            default_password = server.get('defaultPasswordDatabases', '')

            conn = {
                "hostname": server['host'],
                "username": server['user'],
                "password": server['password'],
                "database": "",
            }

            handler_instance = Handler(conn)
            handler_instance.set_output(output)
            handler_instance.set_what(type)
            handler_instance.set_format(format)

            if handler_instance.login():
                click.echo(f"Inicio de sesión exitoso en ({server['host']}).")

                for db in server['databases']:
                    conn["username"] = db.get('user', default_user)
                    conn["password"] = db.get('password', default_password)
                    conn["database"] = db['name']
                    database = conn["database"]
                    
                    handler_instance.set_conn(conn)
                    exported_data = handler_instance.export()

                    extension = ".sql" if output == "plain" else ".sql.gz"
                    
                    if exported_data:
                        formatted_date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                        backup_file_name = (f"{backup_path}/{type}_{format}_{database}_{formatted_date_time}{extension}")
                        
                        if output == "plain":
                            with open(backup_file_name, "w", encoding="utf-8",) as file:
                                file.write(exported_data)
                        else:
                            with open(backup_file_name, "wb") as file:
                                file.write(exported_data)

                        click.echo(f"Backup guardado en '{backup_file_name}'")
                    else:
                        click.echo(f"Error en {database}: {handler_instance.get_error_msg()}")
            else:
                click.echo(f"Error: {handler_instance.get_error_msg()}")
                return
            
    except json.JSONDecodeError:
        click.echo("Error: El archivo no contiene un JSON válido.")

    end_time = time.time()
    total_time = end_time - start_time
    click.echo(f"Tiempo total de ejecución: {total_time:.2f} segundos")
    
if __name__ == '__main__':
    cli()

