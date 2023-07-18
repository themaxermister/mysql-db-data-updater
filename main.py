import csv
import yaml
import pandas as pd
import mysql.connector
from errno import errorcode
from editor import exportQnsTableValues, removeInlineCSS

def readConfig():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def connToDatabase(db_conn_var):
    try:
        return mysql.connector.connect(user=db_conn_var['USERNAME'], password=db_conn_var['PASSWORD'],
                                        host=db_conn_var['HOST'],
                                        port=db_conn_var['PORT'],
                                        database=db_conn_var['DATABASE']
                                    )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    
    return None


def replaceQuestionsConfig(cnx):
    try:
        data = exportQnsTableValues(cnx, ['id', 'question_configuration'], 'STROOP')
        df = pd.DataFrame(data, columns=['id', 'question_configuration'])
        df.to_csv('old_stroop.csv', index=False)
        df['question_configuration'] = df['question_configuration'].apply(removeInlineCSS)
        df.to_csv('new_stroop.csv', index=False)
        print("Questions data edited and exported to CSV successfully!")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    config = readConfig()
    cnx = connToDatabase(config['DB_CONNECTION'])
    if (cnx.is_connected()):
       replaceQuestionsConfig(cnx)
    exit()