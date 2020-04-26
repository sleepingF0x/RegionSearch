## benchmark

**record summary**

| table_name | record counts |
| ---------- | ------------- |
| phone      | 450155        |
| ip         | 648831        |

**fields of records (phone)**

| field name |
| ---------- |
| phone      |
| province   |
| city       |
| isp        |

**fields of records (IP)**

| field name   |
| ------------ |
| ip_start_num |
| country      |
| province     |
| city         |
| isp          |


**performance**

*search 10000 records*

|                  | time | memory usage |
| ---------------- | ---------------------- | -------- |
| PhoneRegionMem   |                        | 372MB    |
| IPRegionMem      |                        | 458MB    |
| PhoneRegionRedis |                        | N/A |
| IPRegionRedis |                        | N/A |
| PhoneRegion |                        | N/A |
| IPRegion |                        | N/A |

------


ip search:

```
ipr = IPRegionRedis()
ipr.lookup("ipaddr")

{'country': '中国', 'province': '广东', 'city': '深圳', 'district': '南山', 'isp': '电信'}
```

phone search:

```
prr = PhoneRegionRedis()
prr.lookup("phoneNumber")

{'province': '广东', 'city': '深圳', 'isp': '移动'}
```
