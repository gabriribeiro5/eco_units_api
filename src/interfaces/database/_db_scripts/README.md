# _db_scripts  
This directory contains shared database scripts (CRUD operations).  

## Purpose  
- To avoid ORM complexity in the code
- To centralize general insert, select, and update operations.  
- Only interface implementations within `interfaces/db_connector` may access this module.  

## Restrictions  
- Do NOT expose this module to external calls.
- External services should rely on the interface modules instead.  
