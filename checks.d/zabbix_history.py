#!/usr/bin/env python

import sys

# Please edit under line to point the site-packages directory where `MySQLdb` installed
sys.path.append('/usr/lib64/python2.7/site-packages')

import time
import requests
import MySQLdb

from checks import AgentCheck
from hashlib import md5

SQL_TEMPLATE = """
SELECT item.value, item.clock
FROM (
    SELECT item.name, host.host, item.itemid, item.snmp_oid, history.value, history.clock
    FROM items item
    LEFT OUTER JOIN history_uint history ON history.itemid = item.itemid
    INNER JOIN hosts host
    ON host.name = '%s'
      AND item.hostid = host.hostid
    WHERE item.name = '%s'
    AND (UNIX_TIMESTAMP() - %s) <= history.clock
    UNION
    SELECT item.name, host.host, item.itemid, item.snmp_oid, history.value, history.clock
    FROM items item
    LEFT OUTER JOIN history history ON history.itemid = item.itemid
    INNER JOIN hosts host
    ON host.name = '%s'
      AND item.hostid = host.hostid
    WHERE item.name = '%s'
    AND (UNIX_TIMESTAMP() - %s) <= history.clock
) item
ORDER BY clock DESC
LIMIT 1
"""


class ZabbixHistoryCheck(AgentCheck):

    def check(self, instance):
        if 'zabbix_db_name' not in instance:
            self.log.info("Skipping instance, please set zabbix_db_name.")
            return
        if 'zabbix_db_host' not in instance:
            self.log.info("Skipping instance, please set zabbix_db_host.")
            return
        if 'zabbix_db_user' not in instance:
            self.log.info("Skipping instance, please set zabbix_db_user.")
            return
        if 'zabbix_db_password' not in instance:
            self.log.info("Skipping instance, please set zabbix_db_password.")
            return
        if 'zabbix_items' not in instance:
            self.log.info("Skipping instance, please set zabbix_items.")
            return

        # Load configs
        threshold_sec_getting_old_metrics = self.init_config.get(
            'threshold_sec_getting_old_metrics', 1200)

        db_name = instance['zabbix_db_name']
        db_host = instance['zabbix_db_host']
        db_user = instance['zabbix_db_user']
        db_password = instance['zabbix_db_password']
        items = instance['zabbix_items']

        conn = MySQLdb.connect(
            db=db_name,
            user=db_user,
            passwd=db_password,
            host=db_host
        )

        for item in items:
            c = conn.cursor()

            host                  = item['host']
            zabbix_itemname       = item['zabbix_item']
            datadog_metric = item = item['datadog_item']

            sql = SQL_TEMPLATE % (host, zabbix_itemname, threshold_sec_getting_old_metrics,
                                  host, zabbix_itemname, threshold_sec_getting_old_metrics)

            c.execute(sql)
            row = c.fetchone()

            if row:
                item_value, item_clock = row

                # tags, hostname, device_name
                self.gauge(datadog_metric, item_value, tags=[
                           'zabbix_value', host], device_name=host)

            c.close()
        conn.close()

    if __name__ == '__main__':
        check, instances = ZabbixHistoryCheck.from_yaml('/etc/dd-agent/conf.d/zabbix_history.yaml')
        for instance in instances:
            print "\nRunning the check against host: %s" % (instance['zabbix_db_host'])
            check.check(instance)
            # if check.has_events():
            #     print 'Events: %s' % (check.get_events())
            print 'Metrics: %s' % (check.get_metrics())
