"""
This module is a convenience module and logging wrapper.

It provides a convenient way to log the process. Follows python's logging library conventions.
Uses the convenience/logging.ini file to create the loggers, handlers and formatters.

# See the notes at the end of the script for database logging
# An example create-table script for database log table is at the end of the script.
# The table name must be specified in the LOG section of the config.ini file.
"""

import logging
from datetime import datetime
from sqlalchemy import text as sqlalchemytext
from convenience.db_helper import DbConnection
from convenience.email_helper import send_activity_email
from convenience.config_helper import Config


class Logger:
    """
    This class is for convenience and is a wrapper around python's logging library.
    """

    _current_config = Config()

    try:

        _is_logging_enabled = bool(_current_config.get_setting_value("logging", "enabled"))

        if _is_logging_enabled:
            _file_name = _current_config.get_setting_value("logging", "file_name")
        else:
            _file_name = None
    except Exception as exc:
        print("""Check if logging section exists in the ini file.
              Sample section below:
                [logging]
                enabled = True
                file_name = log.txt
                db_log_table = process_logs
              """)
        print(exc.message)

    def __init__(
        self, logger_name="process", logging_level=logging.DEBUG, file_name=_file_name
    ) -> None:
        # Check if logging is enabled don't log otherwise.
        if self._is_logging_enabled:
            # first create the formatter
            generic_formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%m/%d/%Y %H:%M:%S",
            )

            # Then create the handlers
            stream_handler = logging.StreamHandler()
            file_handler = logging.FileHandler(file_name)

            # Then set the logging levels in the handlers
            stream_handler.setLevel(logging_level)
            file_handler.setLevel(logging_level)

            # Then set the formatters for the handlers
            stream_handler.setFormatter(generic_formatter)
            file_handler.setFormatter(generic_formatter)

            # Then Create the logger
            self._logger = logging.getLogger(logger_name)

            # Then add handlers to the logger.
            self._logger.addHandler(stream_handler)
            self._logger.addHandler(file_handler)

    def _db_log(self, msg):
        """
        This function is used to log the msg to the database.
        The table name is specified in the ini file.
        The table needs to be created in the schema before using it.
        The schema is specified in the db section of the ini file.
        """
        # If the database logging is requested:
        schema = self._current_config.get_setting_value("database", "schema")
        db_log_table = self._current_config.get_setting_value("log", "db_log_table")
        log_datetime = datetime.now()

        try:
            dbcon = DbConnection()
            with dbcon.engine.begin() as conn:
                conn.execute(
                    sqlalchemytext(
                        f"INSERT INTO [{schema}].[{db_log_table}](LogDateTime,Description) Values (:LogDateTime,:Description)"
                    ),
                    {"LogDateTime": log_datetime, "Description": msg},
                )
        except Exception as exc:
            msg = " An exception occured while logging the current exception to the log table in the database."
            send_activity_email(msg + '/n ' + exc.message)

    def log_info(self, msg, db_log=False):
        """Log the msg in the ifo level.
        Set db_log to true if you would like to
        log the message to the db as well.
        """
        self._logger.info(msg=msg)
        if db_log:
            self._db_log(msg=msg)


# /*
#  * Database:	Selected Database
#  * Script:		Create_Activity_Log_Table.sql
#  * Author:		Edip Celebioglu
#  * Date:		11 October 2023
#  * Description:	This script creates the ETL process logging table. This table needs to be created before the python script is executed.
#  */

# -- Run this file using the CMD mode.

# -- The settings below must be inline with the config.ini file [LOG] and [DATABASE] sections.
# :setvar UsedDb "db_name_here"
# :setvar SchemaName "schema_name_here"
# :setvar ActivityLogTableName "log_table_name_here"


# USE [$(UsedDb)]
# GO

# DROP TABLE IF EXISTS [$(SchemaName)].[$(ActivityLogTableName)]
# GO

# CREATE TABLE [$(SchemaName)].[$(ActivityLogTableName)](
# 	[LogId] [int] IDENTITY(1,1) NOT NULL,
# 	[LogDateTime] datetime2(7) NULL,
# 	[Description] nvarchar(200) NULL

#     CONSTRAINT [PK_$(ActivityLogTableName)] PRIMARY KEY CLUSTERED
# 	(
# 		[LogId] ASC
# 	)WITH (
#           PAD_INDEX = OFF,
#           STATISTICS_NORECOMPUTE = OFF,
#           IGNORE_DUP_KEY = OFF,
#           ALLOW_ROW_LOCKS = ON,
#           ALLOW_PAGE_LOCKS = ON,
#           OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
# ) ON [PRIMARY]
# GO
