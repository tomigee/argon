INSERT INTO {table_name} ({columns}) VALUES ({values})
ON CONFLICT ({conflict_columns}) DO UPDATE SET {updates};