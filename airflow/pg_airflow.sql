create schema reports;

create role report_user with password 'rep_pwd';
GRANT CONNECT ON DATABASE postgres TO report_user;
ALTER ROLE "report_user" WITH LOGIN;
grant usage on schema reports to report_user;

--таблица для витрины
create table if not exists reports.tarificator_by_prod_type_parts
(
    dt_hour           TIMESTAMP NOT NULL,
    prod_type_part_id INTEGER NOT NULL,
    office_id         INTEGER NOT NULL,
    wh_id             INTEGER NOT NULL,
    qty               INTEGER NOT NULL,
    is_credit         BOOLEAN NOT NULL,
    amount_sum        REAL NOT NULL,
    dt_hour_msk       TIMESTAMP NOT NULL,
    dt_load  TIMESTAMP NOT NULL,
    primary key  (dt_hour,office_id,wh_id,prod_type_part_id , is_credit)
);

create schema sync;
grant usage on schema sync to report_user;
--процедура вставки данных в витрину
create or replace procedure sync.tarificator_by_prod_type_parts(_src JSON)
security definer
language plpgsql
as
    $$
    begin
        INSERT into reports.tarificator_by_prod_type_parts as tar
          ( dt_hour           ,
            prod_type_part_id ,
            office_id         ,
            wh_id             ,
            qty               ,
            is_credit         ,
            amount_sum        ,
            dt_hour_msk       ,
            dt_load)
        select distinct on (s.dt_hour ,
                            s.prod_type_part_id ,
                            s.office_id         ,
                            s.wh_id            )
        s.dt_hour,
        s.prod_type_part_id,
        s.office_id,
        s.wh_id,
        s.qty,
        s.is_credit,
        s.amount_sum,
        s.dt_hour_msk,
        s.dt_load
        from json_to_recordset(_src) AS s
           ( dt_hour           TIMESTAMP,
             prod_type_part_id INTEGER ,
             office_id         INTEGER ,
             wh_id             INTEGER ,
             qty               INTEGER ,
             is_credit         BOOLEAN ,
             amount_sum        REAL,
             dt_hour_msk       TIMESTAMP ,
             dt_load           TIMESTAMP)
        order by dt_hour,office_id,wh_id,prod_type_part_id, is_credit
        on conflict (dt_hour,office_id,wh_id,prod_type_part_id, is_credit )
        DO UPDATE
        set
           qty = excluded.qty,
           amount_sum = excluded.amount_sum,
           dt_hour_msk=excluded.dt_hour_msk,
           dt_load=excluded.dt_load
        where tar.dt_load<excluded.dt_load;
    end;
    $$