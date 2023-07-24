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

def cleanCSV(file_path, edited_file_name):
    curr_file = open(file_path, 'r')
    curr_file = ''.join([i for i in curr_file]) 
    curr_file = curr_file.replace("\"\"", "\"")
    edited_file = open(edited_file_name, "w")
    for row in curr_file.split("\n"):
        edited_file.write(row)
        edited_file.write("\n\n")
    edited_file.close()
    
def replaceQuestionsConfig(cnx):
    try:
        data = exportQnsTableValues(cnx, ['id', 'question_family_id', 'question_configuration'], 'color_stroop')
        df = pd.DataFrame(data, columns=['id', 'question_family_id', 'question_configuration'])
        #df.to_csv('data/old_stroop.csv', index=False)
        df['question_configuration'] = df['question_configuration'].apply(removeInlineCSS)
        df.to_csv('data/new_stroop.csv', index=False)
        cleanCSV('data/new_stroop.csv', 'data/edit_new_stroop.csv')
        print("Questions data edited and exported to CSV successfully!")
    except Exception as e:
        print("Failed to output new date: ", e)

if __name__ == '__main__':
    config = readConfig()
    cnx = connToDatabase(config['DB_CONNECTION'])
    if (cnx.is_connected()):
        replaceQuestionsConfig(cnx)
    exit()