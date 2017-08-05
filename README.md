# Datadog checks for Zabbix history

To Datadog, from zabbix.

This checks zabbix database, and send metrics to datadog.

# Motivation

There are many Zabbix users.  It's hard to migrate entirely them into Datadog.  They might include critical target hosts, or switches, maybe using discovery.  We want to use Datadog's beautiful dashboard, but continue to use zabbix and so on...

So, we collect metrics from Zabbix's database, and throw it into Datadog.

# Attension

This only supports Zabbix using MySQL database, Postgres support isn't aimed,  But pull requests are welcome!

# Usage

Before using this, the python installed and `MySQL-python` package (for Python 2.x) or `mysqlclient` package (for Python 3) needs to be installed.  and fix `sys.path.append(...)` of `checks.d/zabbix.py`

Before install, `MySQL-python` or `mysqlclient` requires:

- Debian / Ubuntu / ... : `apt intall -y libmysqlclient-dev`
- CentOS / RHEL / ... : `yum install -y mysql-devel`

After that, follow these steps:

- Place the `checks.d/zabbix.py` file to the checks directory (default is `/etc/dd-agent/checks.d`)
- Copy the `conf.d/zabbix.yaml.example` file to the config directory and rename to `zabbix.yaml` (default is `/etc/dd-agent/conf.d`)
- Restart the agent and run `/etc/init.d/datadog-agent info` to verify that the plugin is working.
  - You can use check command: `sudo -u dd-agent dd-agent check zabbix`


# Config

This checks supports multiple Zabbix's databases, items.

Currently, datadog checks supports only putting latest value, so the only last history of Zabbix can check.
The threshold seconds how old Zabbix data is inserted can set using `threshold_sec_getting_old_metrics`.

Each item are to be set on `zabbix_items`:

- `host`: Host in Zabbix
- `zabbix_item`: Item name in Zabbix
- `datadog_item`: Datadog metric name (don't use spaces!)

```yaml
init_config:
#    max_age_sec_getting_metrics_from_now: 1200

instances:
    - zabbix_db_name: 'ZABBIX_DB_NAME'
      zabbix_db_host: 'ZABBIX_DB_HOST'
      zabbix_db_user: 'ZABBIX_DB_USER'
      zabbix_db_password: 'ZABBIX_DB_PASSWORD'
      zabbix_items:
         - host: 'lovery_switch'
           zabbix_item: 'Incoming Traffic'
           datadog_item: 'net.traffic.incoming'
#    - zabbix_db_name: 'SECOND_ZABBIX_DB_NAME'
#      zabbix_db_host: 'SECOND_ZABBIX_DB_HOST'
#      zabbix_db_user: 'SECOND_ZABBIX_DB_USER'
#      zabbix_db_password: 'SECOND_ZABBIX_DB_PASSWORD'
#      zabbix_items:
#          - host: 'my_server'
#            zabbix_item: 'Disk Usage'
#            datadog_item: 'disk.used'
#          - host: 'my_little_server'
#            zabbix_item: 'Load Average'
#            datadog_item: 'cpu.load.1'
```

## Contributing

Any questions, bug reports, patches are welcome on GitHub at [kyontan/datadog-zabbix-history](https://github.com/kyontan/datadog-zabbix-history)

## LICENCE

Refer LICENCE.md.  Also, this library is licenced as [![SUSHI-WARE LICENSE](https://img.shields.io/badge/license-SUSHI--WARE%F0%9F%8D%A3-blue.svg)](https://github.com/MakeNowJust/sushi-ware)
