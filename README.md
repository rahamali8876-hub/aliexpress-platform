

876-hub ➜ /workspaces/aliexpress-platform (master) $ docker compose up
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] /workspaces/aliexpress-platform/docker-compose.yaml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
Attaching to aliexpress_api, aliexpress_db, aliexpress_elasticsearch, aliexpress_kafka, aliexpress_redis, aliexpress_zookeeper
aliexpress_redis  | 1:C 24 Dec 2025 14:13:19.887 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
aliexpress_redis  | 1:C 24 Dec 2025 14:13:19.888 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
aliexpress_redis  | 1:C 24 Dec 2025 14:13:19.888 * Redis version=7.4.7, bits=64, commit=00000000, modified=0, pid=1, just started
aliexpress_redis  | 1:C 24 Dec 2025 14:13:19.888 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.888 * Increased maximum number of open files to 10032 (it was originally set to 1024).
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.888 * monotonic clock: POSIX clock_gettime
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.889 * Running mode=standalone, port=6379.
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.889 * Server initialized
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.889 * Loading RDB produced by version 7.4.7
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.890 * RDB age 4 seconds
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.890 * RDB memory usage when created 0.90 Mb
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.890 * Done loading RDB, keys loaded: 0, keys expired: 0.
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.890 * DB loaded from disk: 0.000 seconds
aliexpress_redis  | 1:M 24 Dec 2025 14:13:19.890 * Ready to accept connections tcp
aliexpress_zookeeper  | ===> User
aliexpress_zookeeper  | uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
aliexpress_zookeeper  | ===> Configuring ...
aliexpress_db         | 
aliexpress_db         | PostgreSQL Database directory appears to contain a database; Skipping initialization
aliexpress_db         | 
aliexpress_db         | 2025-12-24 14:13:20.347 UTC [1] LOG:  starting PostgreSQL 15.15 (Debian 15.15-1.pgdg13+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
aliexpress_db         | 2025-12-24 14:13:20.348 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
aliexpress_db         | 2025-12-24 14:13:20.349 UTC [1] LOG:  listening on IPv6 address "::", port 5432
aliexpress_db         | 2025-12-24 14:13:20.353 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
aliexpress_db         | 2025-12-24 14:13:20.375 UTC [28] LOG:  database system was shut down at 2025-12-24 14:13:15 UTC
aliexpress_db         | 2025-12-24 14:13:20.438 UTC [1] LOG:  database system is ready to accept connections
aliexpress_kafka      | ===> User
aliexpress_kafka      | uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
aliexpress_kafka      | ===> Configuring ...
aliexpress_kafka      | Running in Zookeeper mode...
aliexpress_api        | Traceback (most recent call last):
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/core/checks/urls.py", line 136, in check_custom_error_handlers
aliexpress_api        |     handler = resolver.resolve_error_handler(status_code)
aliexpress_api        |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py", line 743, in resolve_error_handler
aliexpress_api        |     callback = getattr(self.urlconf_module, "handler%s" % view_type, None)
aliexpress_api        |                        ^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/utils/functional.py", line 47, in __get__
aliexpress_api        |     res = instance.__dict__[self.name] = self.func(instance)
aliexpress_api        |                                          ^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py", line 722, in urlconf_module
aliexpress_api        |     return import_module(self.urlconf_name)
aliexpress_api        |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/importlib/__init__.py", line 90, in import_module
aliexpress_api        |     return _bootstrap._gcd_import(name[level:], package, level)
aliexpress_api        |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
aliexpress_api        |   File "<frozen importlib._bootstrap_external>", line 999, in exec_module
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
aliexpress_api        |   File "/app/config/urls.py", line 21, in <module>
aliexpress_api        |     from core.shared.adapters.http.metrics_view import metrics_view
aliexpress_api        |   File "/app/core/shared/adapters/http/metrics_view.py", line 1, in <module>
aliexpress_api        |     from prometheus_client import generate_latest
aliexpress_api        | ModuleNotFoundError: No module named 'prometheus_client'
aliexpress_api        | 
aliexpress_api        | During handling of the above exception, another exception occurred:
aliexpress_api        | 
aliexpress_api        | Traceback (most recent call last):
aliexpress_api        |   File "/app/manage.py", line 50, in <module>
aliexpress_api        |     main()
aliexpress_api        |   File "/app/manage.py", line 46, in main
aliexpress_api        |     execute_from_command_line(sys.argv)
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 443, in execute_from_command_line
aliexpress_api        |     utility.execute()
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 437, in execute
aliexpress_api        |     self.fetch_command(subcommand).run_from_argv(self.argv)
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/core/management/base.py", line 416, in run_from_argv
aliexpress_api        |     self.execute(*args, **cmd_options)
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/core/management/base.py", line 457, in execute
aliexpress_api        |     self.check(**check_kwargs)
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/core/management/base.py", line 492, in check
aliexpress_api        |     all_issues = checks.run_checks(
aliexpress_api        |                  ^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/core/checks/registry.py", line 89, in run_checks
aliexpress_api        |     new_errors = check(app_configs=app_configs, databases=databases)
aliexpress_api        |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/core/checks/urls.py", line 138, in check_custom_error_handlers
aliexpress_api        |     path = getattr(resolver.urlconf_module, "handler%s" % status_code)
aliexpress_api        |                    ^^^^^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/utils/functional.py", line 47, in __get__
aliexpress_api        |     res = instance.__dict__[self.name] = self.func(instance)
aliexpress_api        |                                          ^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py", line 722, in urlconf_module
aliexpress_api        |     return import_module(self.urlconf_name)
aliexpress_api        |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "/usr/local/lib/python3.12/importlib/__init__.py", line 90, in import_module
aliexpress_api        |     return _bootstrap._gcd_import(name[level:], package, level)
aliexpress_api        |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
aliexpress_api        |   File "<frozen importlib._bootstrap_external>", line 999, in exec_module
aliexpress_api        |   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
aliexpress_api        |   File "/app/config/urls.py", line 21, in <module>
aliexpress_api        |     from core.shared.adapters.http.metrics_view import metrics_view
aliexpress_api        |   File "/app/core/shared/adapters/http/metrics_view.py", line 1, in <module>
aliexpress_api        |     from prometheus_client import generate_latest
aliexpress_api        | ModuleNotFoundError: No module named 'prometheus_client'
aliexpress_api exited with code 1
aliexpress_zookeeper  | ===> Running preflight checks ... 
aliexpress_zookeeper  | ===> Check if /var/lib/zookeeper/data is writable ...
aliexpress_zookeeper  | ===> Check if /var/lib/zookeeper/log is writable ...
aliexpress_kafka      | ===> Running preflight checks ... 
aliexpress_kafka      | ===> Check if /var/lib/kafka/data is writable ...
aliexpress_zookeeper  | ===> Launching ... 
aliexpress_zookeeper  | ===> Launching zookeeper ... 
aliexpress_kafka      | ===> Check if Zookeeper is healthy ...
aliexpress_elasticsearch  | Dec 24, 2025 2:13:30 PM sun.util.locale.provider.LocaleProviderAdapter <clinit>
aliexpress_elasticsearch  | WARNING: COMPAT locale provider will be removed in a future release
aliexpress_zookeeper      | [2025-12-24 14:13:30,452] INFO Reading configuration from: /etc/kafka/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,484] INFO clientPortAddress is 0.0.0.0:2181 (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,484] INFO secureClientPort is not set (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,484] INFO observerMasterPort is not set (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,484] INFO metricsProvider.className is org.apache.zookeeper.metrics.impl.DefaultMetricsProvider (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,506] INFO autopurge.snapRetainCount set to 3 (org.apache.zookeeper.server.DatadirCleanupManager)
aliexpress_zookeeper      | [2025-12-24 14:13:30,506] INFO autopurge.purgeInterval set to 0 (org.apache.zookeeper.server.DatadirCleanupManager)
aliexpress_zookeeper      | [2025-12-24 14:13:30,506] INFO Purge task is not scheduled. (org.apache.zookeeper.server.DatadirCleanupManager)
aliexpress_zookeeper      | [2025-12-24 14:13:30,506] WARN Either no config or no quorum defined in config, running in standalone mode (org.apache.zookeeper.server.quorum.QuorumPeerMain)
aliexpress_zookeeper      | [2025-12-24 14:13:30,515] INFO Log4j 1.2 jmx support not found; jmx disabled. (org.apache.zookeeper.jmx.ManagedUtil)
aliexpress_zookeeper      | [2025-12-24 14:13:30,518] INFO Reading configuration from: /etc/kafka/zookeeper.properties (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,522] INFO clientPortAddress is 0.0.0.0:2181 (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,523] INFO secureClientPort is not set (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,524] INFO observerMasterPort is not set (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,524] INFO metricsProvider.className is org.apache.zookeeper.metrics.impl.DefaultMetricsProvider (org.apache.zookeeper.server.quorum.QuorumPeerConfig)
aliexpress_zookeeper      | [2025-12-24 14:13:30,524] INFO Starting server (org.apache.zookeeper.server.ZooKeeperServerMain)
aliexpress_zookeeper      | [2025-12-24 14:13:30,579] INFO ServerMetrics initialized with provider org.apache.zookeeper.metrics.impl.DefaultMetricsProvider@40cb8df7 (org.apache.zookeeper.server.ServerMetrics)
aliexpress_zookeeper      | [2025-12-24 14:13:30,592] INFO ACL digest algorithm is: SHA1 (org.apache.zookeeper.server.auth.DigestAuthenticationProvider)
aliexpress_zookeeper      | [2025-12-24 14:13:30,596] INFO zookeeper.DigestAuthenticationProvider.enabled = true (org.apache.zookeeper.server.auth.DigestAuthenticationProvider)
aliexpress_zookeeper      | [2025-12-24 14:13:30,607] INFO zookeeper.snapshot.trust.empty : false (org.apache.zookeeper.server.persistence.FileTxnSnapLog)
aliexpress_zookeeper      | [2025-12-24 14:13:30,666] INFO  (org.apache.zookeeper.server.ZooKeeperServer)
aliexpress_zookeeper      | [2025-12-24 14:13:30,666] INFO   ______          