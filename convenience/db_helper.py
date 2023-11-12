"""
Contains the database connectivity class.
"""
import sqlalchemy as sa
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool
from convenience.wdp_api_helper import read_wdp_api_xml
from convenience.config_helper import Config



class DbConnection:
    """
    Convenience class for database connection.
    """
    _current_config = Config()

    # Get the db configuration from config.ini
    def __init__(
        self,
        app_name = _current_config.get_setting_value('database', 'app_name'),
        server = _current_config.get_setting_value('database', 'server'),
        database = _current_config.get_setting_value('database', 'database'),
        schema = _current_config.get_setting_value('database', 'schema'),
        driver = _current_config.get_setting_value('database', 'driver'),
        timeout = _current_config.get_setting_value('database', 'timeout'),
        auth_xml_file = _current_config.get_setting_value('database', 'auth_xml_file')
    ):

        self._app_name = app_name
        self._server = server
        self._database = database
        self._schema = schema
        self._driver = driver
        self._timeout = timeout
        self._auth_xml_file = auth_xml_file

        self._user, self._password = read_wdp_api_xml(self._auth_xml_file) 

        self._con_string = f"""
                            DRIVER={self._driver};
                            Server={self._server};
                            Database={self._database};
                            APP={self._app_name};
                            UID={self._user};
                            PWD={self._password};
                            Connection Timeout={self._timeout};
                            """
        self.connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": self._con_string})
        self.meta = sa.MetaData()
        self.engine = sa.create_engine(self.connection_url, poolclass=NullPool, future=True)

