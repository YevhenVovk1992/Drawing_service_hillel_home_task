import psycopg2


def update_file_status(filename):
    print(filename)
    con = psycopg2.connect(
        database='dr_service_db', user='postgres',
        password='example', host='localhost', port=5432
    )
    cursor = con.cursor()
    cursor.execute(f"""UPDATE task_queue SET status='Done' 
                    where filename='{filename}'""")
    con.commit()
    con.close()

update_file_status('Hillel_Video_Conf_Background.jpg')