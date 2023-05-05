import mysql.connector

def insert_data(data_list):
    # 连接MySQL数据库
    cnx = mysql.connector.connect(user='user_kmsp', password='Tasly_User01!',
                                  host='10.6.3.167', database='kmsp')

    cursor = cnx.cursor()

    # 定义插入数据的SQL语句
    insert_query = "INSERT INTO llm_abstract_extract_info (gene, effect, herb,create_time,state,pmid) VALUES (%s, %s, %s,now(),0,%s)"

    # 批量插入数据
    cursor.executemany(insert_query, data_list)

    # 提交事务
    cnx.commit()

    # 关闭游标和连接
    cursor.close()
    cnx.close()

# 调用insert_data函数，将数据批量插入到MySQL表中
data_list = [('gene1', 'effect1', 'herb1','1'), ('gene2', 'effect2', 'herb2','2'), ('gene3', 'effect3', 'herb3','3')]
insert_data(data_list)
