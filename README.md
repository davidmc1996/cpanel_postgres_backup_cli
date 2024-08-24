CpanelPostgresBackup
====================

Descripción
-----------

CpanelPostgresBackup es una herramienta de línea de comandos (CLI) escrita en Python que permite realizar respaldos de bases de datos PostgreSQL a través de cPanel utilizando su interfaz de phpPgAdmin. Este script facilita el proceso de autenticación, exportación de datos y estructuras, y descarga de respaldos en formatos plano (.sql) o comprimido (.sql.gz).

Características
---------------

*   **Autenticación automática** en cPanel utilizando credenciales de usuario.
    
*   **Exportación de bases de datos** PostgreSQL en diferentes formatos (SQL o COPY).
    
*   **Soporte para múltiples tipos de respaldo**:
    
    *   data (solo datos)
        
    *   structure (solo estructura)
        
    *   structuredata (estructura y datos)
        
*   **Generación de respaldos comprimidos** para una gestión eficiente del almacenamiento.
    
*   **Validación de archivos JSON** que contienen la configuración de conexión a los servidores y bases de datos.
    

Instalación
-----------

1.  Clona el repositorio:

```bash
   git clone https://github.com/tuusuario/cpanel-postgres-backup.git
   cd cpanel-postgres-backup
```

2.  Instala las dependencias necesarias:

```bash
   pip install -r requirements.txt
```

Uso
-----------

Ejecuta la herramienta de línea de comandos pasando los parámetros necesarios:

```bash
python cli.py --json_file <ruta_al_archivo_JSON> --backup_path <ruta_de_respaldo> --output <plain|zip> --type <data|structure|structuredata> --format <sql|copy>
```

### Opciones

*   \--json\_file: Ruta del archivo JSON con los datos de conexión.
    
*   \--backup\_path: Ruta del directorio donde se guardarán los respaldos.
    
*   \--output: Formato de salida del respaldo: plain para archivos .sql o zip para archivos comprimidos .gz.
    
*   \--type: Tipo de respaldo: data para datos, structure para estructura, structuredata para ambos.
    
*   \--format: Formato del respaldo: sql para generar un script de SQL o copy para un archivo de texto con datos delimitados.

Ejemplo de comando
-----------

```bash
python cli.py --json_file configs/connections.json --backup_path backups/ --output plain --type structuredata --format sql
```

Configuración del Archivo JSON
-----------

El archivo JSON debe contener la configuración de conexión a los servidores y bases de datos. A continuación, se muestra un ejemplo de estructura:

```json
{
    "servers": [
        {
            "name": "Servidor 1",
            "host": "host1.ejemplo.com",
            "user": "usuario",
            "password": "contraseña",
            "defaultPortDatabases": 5432,
            "defaultUserDatabases": "usuarioDB",
            "defaultPasswordDatabases": "contraseñaDB",
            "databases": [
                {
                    "name": "nombreDB1",
                    "port": 5432,
                    "user": "usuarioDB",
                    "password": "contraseñaDB"
                }
            ]
        }
    ]
}
```