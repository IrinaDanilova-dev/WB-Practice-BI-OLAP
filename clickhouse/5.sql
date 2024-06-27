CREATE TABLE stage.tareTransfer
(
    `tare_id` Int64,
    `tare_type` LowCardinality(String),
    `employee_id` Int64,
    `dt` DateTime,
    `place_cod` UInt64,
    `dt_load` datetime materialized now()
)
engine = MergeTree()
partition by toYYYYMMDD(dt)
order by (tare_type,tare_id)
ttl toStartOfDay(dt) + interval 5 day
settings ttl_only_drop_parts=1;



CREATE TABLE direct_log.tareTransfer_buf
(
    `tare_id` Int64,
    `tare_type` LowCardinality(String),
    `employee_id` Int64,
    `dt` DateTime,
    `place_cod` UInt64
)
ENGINE = Buffer('stage', 'tareTransfer',  1, 10, 100, 10000, 1000000, 10000000, 100000000);

