### config from app.config
* SESSION_COOKIE_NAME     the name of the session cookie
* SESSION_COOKIE_DOMAIN   the domain for the session cookie. If this is not set, the cookie will be valid for all subdomains of SERVER_NAME.
* SESSION_COOKIE_PATH     the path for the session cookie. If this is not set the cookie will be valid for all of APPLICATION_ROOT or if that is not set for '/'.
* SESSION_COOKIE_HTTPONLY     controls if the cookie should be set with the httponly flag. Defaults to True.
* SESSION_COOKIE_SECURE   controls if the cookie should be set with the secure flag. Defaults to False.
* PERMANENT_SESSION_LIFETIME  the lifetime of a permanent session as datetime.timedelta object. Starting with Flask 0.8 this can also be an integer representing seconds.

### Flask-Session specific configs
* SESSION_TYPE   Specifies which type of session interface to use. Built-in session types:

    null: NullSessionInterface (default)
    redis: RedisSessionInterface
    memcached: MemcachedSessionInterface
    filesystem: FileSystemSessionInterface
    mongodb: MongoDBSessionInterface
    sqlalchemy: SqlAlchemySessionInterface

* SESSION_PERMANENT   Whether use permanent session or not, default to be True
* SESSION_USE_SIGNER  Whether sign the session cookie sid or not, if set to True, you have to set flask.Flask.secret_key, default to be False
* SESSION_KEY_PREFIX  A prefix that is added before all session keys. This makes it possible to use the same backend storage server for different apps, default “session:”
* SESSION_REDIS   A redis.Redis instance, default connect to 127.0.0.1:6379
* SESSION_MEMCACHED   A memcache.Client instance, default connect to 127.0.0.1:11211
* SESSION_FILE_DIR    The directory where session files are stored. Default to use flask_session directory under current working directory.
* SESSION_FILE_THRESHOLD  The maximum number of items the session stores before it starts deleting some, default 500
* SESSION_FILE_MODE   The file mode wanted for the session files, default 0600
* SESSION_MONGODB     A pymongo.MongoClient instance, default connect to 127.0.0.1:27017
* SESSION_MONGODB_DB  The MongoDB database you want to use, default “flask_session”
* SESSION_MONGODB_COLLECT     The MongoDB collection you want to use, default “sessions”
* SESSION_SQLALCHEMY  A flask.ext.sqlalchemy.SQLAlchemy instance whose database connection URI is configured using the SQLALCHEMY_DATABASE_URI parameter
* SESSION_SQLALCHEMY_TABLE    The name of the SQL table you want to use, default “sessions”
