from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta




default_args = {
    'owner': 'Ira',
    'start_date': datetime(2024, 8, 2)
}

dag = DAG(
    dag_id='report_tarificator_by_prod_type_parts',
    default_args=default_args,
    schedule_interval='5-55/20 * * * *',
    description='тарификатор по участкам работ',
    catchup=False,
    max_active_runs=1
)

def main():
    import json
    from Utils.Connect_DB import connect_CH, connect_PG


    client_ch=connect_CH()
    client_pg = connect_PG()
    client_ch.execute("""insert into reports.tarificator_by_prod_type_parts
                            ( dt_hour, office_id, wh_id, prod_type_part_id, is_credit, qty, amount_sum, dt_hour_msk )
                        select dt_hour
                             , office_id
                             , wh_id
                             , prod_type_part_id
                             , is_credit
                             , sum(qty)        qty
                             , sum(amount_sum) amount_sum
                             , dt_hour_msk
                        from default.tarificator_by_wh_hour_emp_ptype final
                        where dt_hour >= (
                                             select max(dt_hour)
                                             from default.tarificator_by_wh_hour_emp_ptype
                                         ) - interval 6 hour
                        group by dt_hour, office_id, wh_id, prod_type_part_id, is_credit, dt_hour_msk
                        """)
    print('inserted into ch')

    sql_data= """select  dt_hour
                       , office_id
                       , wh_id
                       , prod_type_part_id
                       , is_credit
                       , qty
                       , amount_sum
                       , dt_hour_msk
                       , dt_load
                from reports.tarificator_by_prod_type_parts final
                where dt_hour >= (   select max(dt_hour)
                                     from reports.tarificator_by_prod_type_parts
                                 ) - interval 6 hour"""

    df=client_ch.query_dataframe(sql_data)
    client_ch.disconnect()
    df_json=df.to_json(orient='records',date_format='iso')
    cursor_pg=client_pg.cursor()
    cursor_pg.execute(f"""CALL sync.tarificator_by_prod_type_parts(_src:='{df_json}')""")
    client_pg.commit()
    client_pg.close()

task_tarificator_by_prod_type_parts = PythonOperator(
    task_id='rep_tarificator_by_prod_type_parts', python_callable=main, dag=dag)


