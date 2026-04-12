from aiohttp import web
from config import Definitions
from out_of_process.auth import AuthManager as Auth
from use_cases.db_setup.asyncCreateSchema import SchemaSetupHandler
from use_cases.simple_responses.trace import TraceHandler as Trace
from use_cases.simple_responses.options import OptionsHandler as Options
import logging
import asyncio


class AsyncMasterHandler(Auth, Trace, Options):
    """aiohttp-based handler for HTTP requests."""
    
    def __init__(self):
        self.options = None
    
    async def run_handler(self, handler_name, *args, **kwargs):
        logging.info(f"calling handler: {handler_name}")
        if handler_name and hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            # Support both sync and async handlers
            import inspect
            if inspect.iscoroutinefunction(handler):
                response_data = await handler(*args, **kwargs)
            else:
                response_data = handler(*args, **kwargs)
            return response_data
        else:
            err_msg = f"Handler '{handler_name}' not found"
            logging.error(err_msg)
            raise ValueError(err_msg)
    
    def format_response(self, response_data):
        """Convert response tuple (status, headers, body) to aiohttp Response"""
        logging.info("formatting response")
        if not response_data or len(response_data) < 3:
            return web.Response(status=500, text="Internal Server Error")
        
        status, headers, body = response_data
        return web.Response(
            status=status,
            text=body if isinstance(body, str) else body.decode("utf-8") if body else "",
            headers=headers
        )
    
    async def trace_handler(self, request):
        logging.info(f"TRACE request from {request.remote}")
        try:
            handler_name = self.options.only_TRACE.get(request.path, {}).get("method")
            if isinstance(handler_name, str):
                response_data = await self.run_handler(handler_name)
                return self.format_response(response_data)
            else:
                return web.Response(status=500, text="Invalid handler name")
        except Exception as e:
            logging.error(f"Error in TRACE handler: {e}")
            return web.Response(status=500, text=f"Internal Server Error: {str(e)}")
    
    async def options_handler(self, request):
        logging.info(f"OPTIONS request from {request.remote}")
        try:
            handler_name = self.options.only_OPTIONS.get(request.path, {}).get("method")
            if isinstance(handler_name, str):
                response_data = await self.run_handler(handler_name)
                return self.format_response(response_data)
            else:
                return web.Response(status=500, text="Invalid handler name")
        except Exception as e:
            logging.error(f"Error in OPTIONS handler: {e}")
            return web.Response(status=500, text=f"Internal Server Error: {str(e)}")
    
    async def post_handler(self, request):
        """
        Query example:
            INSERT INTO users (name, email, created_at, last_updated)
            VALUES ('Jane Doe', 'jane.doe@example.com', NOW(), NOW());
        """
        logging.info(f"POST request from {request.remote}")
        try:
            handler_name = self.options.only_POST.get(request.path, {}).get("method")
            if isinstance(handler_name, str):
                response_data = await self.run_handler(handler_name)
                return self.format_response(response_data)
            else:
                return web.Response(status=500, text="Invalid handler name")
        except Exception as e:
            logging.error(f"Error in POST handler: {e}")
            return web.Response(status=500, text=f"Internal Server Error: {str(e)}")
    
    async def get_handler(self, request):
        logging.info(f"GET request from {request.remote}")
        try:
            handler_name = self.options.only_GET.get(request.path, {}).get("method")
            if isinstance(handler_name, str):
                response_data = await self.run_handler(handler_name)
                return self.format_response(response_data)
            else:
                return web.Response(status=500, text="Invalid handler name")
        except Exception as e:
            logging.error(f"Error in GET handler: {e}")
            return web.Response(status=500, text=f"Internal Server Error: {str(e)}")
    
    async def put_handler(self, request):
        """
        Query example:
            INSERT INTO users (user_id, name, email, created_at, last_updated)
            VALUES (42, 'John Doe', 'john.doe@example.com', NOW(), NOW())
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                email = VALUES(email),
                last_updated = NOW();
        """
        logging.info(f"PUT request from {request.remote}")
        try:
            handler_name = self.options.only_POST.get(request.path, {}).get("method")
            if isinstance(handler_name, str):
                response_data = await self.run_handler(handler_name)
                return self.format_response(response_data)
            else:
                return web.Response(status=500, text="Invalid handler name")
        except Exception as e:
            logging.error(f"Error in PUT handler: {e}")
            return web.Response(status=500, text=f"Internal Server Error: {str(e)}")
    
    async def patch_handler(self, request):
        """
        Query example:
            UPDATE users
            SET email = 'new_email@example.com',
                last_updated = NOW()
            WHERE user_id = 42;
        """
        logging.info(f"PATCH request from {request.remote}")
        try:
            handler_name = self.options.only_POST.get(request.path, {}).get("method")
            if isinstance(handler_name, str):
                response_data = await self.run_handler(handler_name)
                return self.format_response(response_data)
            else:
                return web.Response(status=500, text="Invalid handler name")
        except Exception as e:
            logging.error(f"Error in PATCH handler: {e}")
            return web.Response(status=500, text=f"Internal Server Error: {str(e)}")
    
    async def delete_handler(self, request):
        logging.info(f"DELETE request from {request.remote}")
        try:
            handler_name = self.options.only_POST.get(request.path, {}).get("method")
            if isinstance(handler_name, str):
                response_data = await self.run_handler(handler_name)
                return self.format_response(response_data)
            else:
                return web.Response(status=500, text="Invalid handler name")
        except Exception as e:
            logging.error(f"Error in DELETE handler: {e}")
            return web.Response(status=500, text=f"Internal Server Error: {str(e)}")


class AsyncWakeUp():
    def __init__(self):
        self.config = Definitions()
        self.http_handler = AsyncMasterHandler()
        self.app = None
    
    async def database_setup_with_retry(self, max_retries=5, base_delay=2):
        """
        Initialize database with exponential backoff retry logic.
        
        Args:
            max_retries: Maximum number of connection attempts
            base_delay: Initial delay in seconds (doubles each retry)
        """
        for attempt in range(1, max_retries + 1):
            try:
                logging.info(f"Database setup attempt {attempt}/{max_retries}...")
                db = SchemaSetupHandler()
                await db.initialize()
                await db.schema_setup()
                logging.info("Database setup completed successfully")
                return True
            except Exception as e:
                if attempt < max_retries:
                    delay = base_delay * (2 ** (attempt - 1))
                    logging.warning(
                        f"Database setup failed (attempt {attempt}): {str(e)}. "
                        f"Retrying in {delay} seconds..."
                    )
                    await asyncio.sleep(delay)
                else:
                    logging.error(
                        f"Database setup failed after {max_retries} attempts: {str(e)}"
                    )
                    raise

    async def startup_app(self, app):
        """Startup handler for aiohttp app"""
        await self.database_setup_with_retry()
        # Suppress aiomysql query logs
        logging.getLogger('aiomysql').setLevel(logging.WARNING)

    async def hello(self, request):
        """Root health check endpoint"""
        return web.Response(text="Hello, world")

    async def post_dispatcher(self, request):
        """Dispatch POST requests based on path"""
        path = request.path
        # Route based on path to appropriate handler
        if path.startswith('/api'):
            # TRACE or OPTIONS or POST based on actual method detection in handler
            return await self.http_handler.post_handler(request)
        return await self.http_handler.post_handler(request)

    def startup_routine(self):
        """Main startup routine for async server"""
        self.app = web.Application()
        
        # Add routes
        self.app.router.add_get('/', self.hello)
        self.app.router.add_post('/{path_info:.*}', self.post_dispatcher)
        self.app.router.add_get('/{path_info:.*}', self.http_handler.get_handler)
        self.app.router.add_put('/{path_info:.*}', self.http_handler.put_handler)
        self.app.router.add_patch('/{path_info:.*}', self.http_handler.patch_handler)
        self.app.router.add_delete('/{path_info:.*}', self.http_handler.delete_handler)
        self.app.router.add_route('OPTIONS', '/{path_info:.*}', self.http_handler.options_handler)
        self.app.router.add_route('TRACE', '/{path_info:.*}', self.http_handler.trace_handler)
        
        # Register startup handler
        self.app.on_startup.append(self.startup_app)
        
        logging.info(f"Starting server on port {self.config.SERVER_PORT}...")
        web.run_app(self.app, port=self.config.SERVER_PORT)

if __name__ == "__main__":
    print("You are calling the Controller. Call main.py instead.")