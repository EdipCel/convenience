-- USE Db_name; 
-- GO
BEGIN --Outline  parameters
	DECLARE @TableCatalog NVARCHAR(MAX)	= '%%';
	DECLARE @SchemaName NVARCHAR(MAX) = '%%';
	DECLARE @TableName  NVARCHAR(MAX) = '%%';
	DECLARE @ColName NVARCHAR(MAX)  = '%%';
	DECLARE @TableNameNot NVARCHAR(MAX) = '';
END

BEGIN --Outline ColumnSearch
	SELECT DISTINCT cols.TABLE_SCHEMA, cols.TABLE_NAME, cols.COLUMN_NAME, cols.DATA_TYPE, cols.CHARACTER_MAXIMUM_LENGTH, cols.IS_NULLABLE,cols.COLUMN_DEFAULT,tc.constraint_type as ConstraintType,cols.ORDINAL_POSITION
	FROM INFORMATION_SCHEMA.COLUMNS cols
	LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu ON cols.TABLE_SCHEMA = kcu.TABLE_SCHEMA AND cols.TABLE_NAME = kcu.TABLE_NAME AND cols.COLUMN_NAME = kcu.COLUMN_NAME
	LEFT JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc ON kcu.TABLE_SCHEMA = tc.TABLE_SCHEMA AND kcu.TABLE_NAME = tc.TABLE_NAME
	WHERE cols.TABLE_CATALOG LIKE @TableCatalog
	AND cols.TABLE_SCHEMA LIKE @SchemaName
	AND cols.TABLE_NAME LIKE @TableName
	AND cols.TABLE_NAME NOT LIKE @TableNameNot
	AND cols.COLUMN_NAME LIKE @ColName
	--ORDER BY TABLE_NAME DESC
	ORDER BY cols.TABLE_SCHEMA ASC,cols.TABLE_NAME DESC, cols.ORDINAL_POSITION ASC
END

-- BEGIN --Outline TableSearch
-- 	SELECT DISTINCT TABLE_SCHEMA,TABLE_NAME
-- 	FROM INFORMATION_SCHEMA.COLUMNS
-- 	WHERE 
-- 		TABLE_CATALOG LIKE @TableCatalog
-- 	AND TABLE_SCHEMA LIKE @SchemaName
-- 	AND TABLE_NAME LIKE @TableName
-- 	AND TABLE_NAME NOT LIKE @TableNameNot
-- 	AND COLUMN_NAME LIKE @ColName
-- 	ORDER BY TABLE_SCHEMA,TABLE_NAME DESC
-- END

--exec sp_columns @table_name='TableName', @table_owner = 'dbo' ;

--SELECT TOP 10 TABLE_CATALOG, TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,IS_NULLABLE FROM MasterData_Edip.INFORMATION_SCHEMA.COLUMNS
--WHERE COLUMN_NAME LIKE @ColName

--SELECT TOP 10 * FROM MasterData_Edip.INFORMATION_SCHEMA.COLUMNS