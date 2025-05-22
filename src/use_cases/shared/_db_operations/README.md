# _db_operations  
This directory contains shared database logic (CRUD operations).  

## Purpose  
- To centralize general insert, select, and update operations.  
- Only use case implementations within `use_cases/` may access this module.  

## Restrictions  
- Do NOT expose this module to external calls.  
- External services should rely on the use case modules instead.  
