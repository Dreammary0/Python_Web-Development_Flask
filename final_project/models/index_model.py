import sqlite3
import pandas as pd

#функция изменения базы данных
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


#Вывести услуги для процедур
def Service(con):
    return pd.read_sql("""SELECT IDProcedureList, ProcedureListName , ProcedurePrice, P.ProcedureName  
    FROM ProcedureList
    JOIN "Procedure" P on P.IDProcedure = ProcedureList.Procedure_IDProcedure 
    order by ProcedurePrice ASC 
    """,con)


#Вывести мастеров для выбранных процедур
def Masters_for_procedure(conn, procedures_list):
    df = pd.read_sql("""
    SELECT IDMaster, MasterName , P.ProcedureName
    FROM Master
    JOIN "Procedure" P on P.IDProcedure = Master.Procedure_IDProcedure
    ORDER BY P.ProcedureName """, conn)
    if procedures_list:
        df = df[df.ProcedureName.isin(procedures_list)]
    return df


# Какие окошки есть у мастера
def Master_records(con,master):
    df = pd.read_sql(f'''
    select IDOrder, OrderData as Дата, OrderTime as Время, Client_IDClient as Запись, M.MasterName, P.ProcedureName
    from OrderList
    JOIN Schedule S on Schedule_IDSchedule=S.IDSchedule
    JOIN Master M on S.Master_IDMaster=M.IDMaster 
    join Procedure P on M.Procedure_IDProcedure = P.IDProcedure
    where Master_IDMaster={master}
    ''',con)
    # if master_list:
    #     m_list=[]
    #     for elem in master_list:
    #         m_list.append(int(elem))
    #     print(m_list)
    #     df = df[df.Master_IDMaster.isin(list(m_list))]
    df['Запись'] = df['Запись'].fillna(0)
    return df

#Окошки в выбранные даты (с указанным мастером для перебора в цикле контроллера)
def Find_time_date(con,dateStart, dateEnd, name):
        df=pd.read_sql(f'''
        select IDOrder, OrderData as Дата, OrderTime as Время, Client_IDClient as Запись, M.MasterName, P.ProcedureName, M.IDMaster
        from OrderList
        JOIN Schedule S on Schedule_IDSchedule=S.IDSchedule
        JOIN Master M on S.Master_IDMaster=M.IDMaster 
        join Procedure P on M.Procedure_IDProcedure = P.IDProcedure
        WHERE OrderData>='{dateStart}' and OrderData<='{dateEnd}' and MasterName='{name}'
    ''',con)
        df['Запись'] = df['Запись'].fillna(0)
        return df


#информация по записи при нажатии кнопки времени OrderList
def OrderListRegPage(con, id_order_list, procedure_name):
    print(id_order_list)
    df = pd.read_sql(f'''SELECT IDOrder, OrderData, OrderTime, M.MasterName, P.ProcedureName
    FROM OrderList
    join Schedule S on OrderList.Schedule_IDSchedule = S.IDSchedule
    join Master M on M.IDMaster = S.Master_IDMaster
    join Procedure P on OrderList.Procedure_IDProcedure = P.IDProcedure
    where P.ProcedureName='{procedure_name}'
    ''',con)
    if id_order_list:
        m_list=[]
        for elem in id_order_list:
            m_list.append(int(elem))
        df = df[df.IDOrder.isin(list(m_list))]
        indx = pd.Index(range(0, len(df), 1))
        df = df.set_index(indx)
    return df


def Check_sum(conn, service_list):
    df = pd.read_sql("""
    SELECT ProcedureListName,ProcedurePrice
    from ProcedureList """, conn)
    df=df.loc[df['ProcedureListName'].isin(service_list), 'ProcedurePrice'].sum()
    return df

# Добавить нового клиента
def AddNewClient(con, name,phone):
    
    Add_Client='''
    INSERT INTO Client ("IDClient","ClientName","ClientPhone") 
    VALUES (null, 'Марина','574374')
    
/*    DELETE FROM Client where IDClient>10;
    UPDATE SQLITE_SEQUENCE SET seq = 1 WHERE name = 'Client';*/
    '''
    execute_query(con, Add_Client)


# Записать клиента
def RecordClient (con, CLientID, OrderID):
    Reg_for_proc='''
    UPDATE OrderList SET Client_IDClient = 1 WHERE IDOrder=1
    '''
    execute_query(con, Reg_for_proc)


def Task6(con):
    print("3.2 Вывести доступные варианты записи на процедуру 1 после 18:00 и мастеров")
    return pd.read_sql('''
    with night as (select * from OrderList where Procedure_IDProcedure=1 and OrderTime>=18 and Client_IDClient is NULL)
    select IDOrder, P.ProcedureName, OrderData, OrderTime,M.MasterName, M.MasterPhone 
    from night
    join Schedule S on night.Schedule_IDSchedule=S.IDSchedule
    join Master M on S.Master_IDMaster=M.IDMaster
    join Procedure P on M.Procedure_IDProcedure=P.IDProcedure
    ''',con)



