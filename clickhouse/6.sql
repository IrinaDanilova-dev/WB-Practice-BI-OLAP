create table history.tareTransfer
(
    tare_id     Int64,
    tare_type   LowCardinality(String),
    employee_id Int64,
    dt          DateTime,
    place_cod   UInt64,
    dt_load     datetime materialized now()
) engine = MergeTree() partition by toYYYYMM(dt) order by ( tare_type, tare_id, dt );

create materialized view mv_tareTransfer_to_history to history.tareTransfer as
select *
from stage.tareTransfer;

    CREATE table current.tareTransfer
(
    `tare_id` Int64,
    `tare_type` lowcardinality(string),
    `employee_id` Int64,
    `dt` datetime,
    `place_cod` UInt64,
    `dt_load` datetime materialized now()
)
engine = ReplacingMergeTree()
order by (tare_type,tare_id);


create materialized view mv_tareTransfer_to_current to current.tareTransfer as
select *
from stage.tareTransfer;

