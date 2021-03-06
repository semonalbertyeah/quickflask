### specific configs
* SQLALCHEMY_DATABASE_URI     The database URI that should be used for the connection. Examples:

    - sqlite:////tmp/test.db
    - mysql://username:password@server/db

* SQLALCHEMY_BINDS    A dictionary that maps bind keys to SQLAlchemy connection URIs. For more information about binds see Multiple Databases with Binds.
* SQLALCHEMY_ECHO     If set to True SQLAlchemy will log all the statements issued to stderr which can be useful for debugging.
* SQLALCHEMY_RECORD_QUERIES   Can be used to explicitly disable or enable query recording. Query recording automatically happens in debug or testing mode. See get_debug_queries() for more information.
* SQLALCHEMY_NATIVE_UNICODE   Can be used to explicitly disable native unicode support. This is required for some database adapters (like PostgreSQL on some Ubuntu versions) when used with improper database defaults that specify encoding-less databases.
* SQLALCHEMY_POOL_SIZE    The size of the database pool. Defaults to the engine’s default (usually 5)
* SQLALCHEMY_POOL_TIMEOUT     Specifies the connection timeout for the pool. Defaults to 10.
* SQLALCHEMY_POOL_RECYCLE     Number of seconds after which a connection is automatically recycled. This is required for MySQL, which removes connections after 8 hours idle by default. Note that Flask-SQLAlchemy automatically sets this to 2 hours if MySQL is used.
* SQLALCHEMY_MAX_OVERFLOW     Controls the number of connections that can be created after the pool reached its maximum size. When those additional connections are returned to the pool, they are disconnected and discarded.
* SQLALCHEMY_TRACK_MODIFICATIONS  If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None, which enables tracking but issues a warning that it will be disabled by default in the future. This requires extra memory and should be disabled if not needed.
