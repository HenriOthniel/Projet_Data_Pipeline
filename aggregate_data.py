import argparse
import pandas as pd

def sort_count_msg_by_id(messages_file, users_file, output_file):
    """sort_count_msg_by_id

    Args:
        messages_file (string): chemin du fichier csv contenant la liste des messages
        users_file (string): chemin du fichier csv contenant la liste des utilisateurs
        output_file (string): chemin du fichier csv de sortie contenant le compte des messages par id ordonnés en ordre croissant

    Returns:
        _type_: output_csv (string, chemin csv): dataset csv, avec compte des messages par id odonnés en ordres croissant 
    """

    df_messages = pd.read_csv(messages_file)
    df_users = pd.read_csv(users_file)

    user_id = [i for i in df_users['user_id']]
    first_name = [i for i in df_users['first_name']]
    last_name = [i for i in df_users['last_name']]
    author_id = [i for i in df_messages['author_id']]
    total_receipts = [author_id.count(i) for i in user_id]
   
    dict_output = {'user_id' : user_id, 'first_name' : first_name, 'last_name' : last_name, 'total_receipts' : total_receipts}
    
    df_output = pd.DataFrame(dict_output).sort_values(by=['total_receipts'])
    
    
    output_csv = df_output.to_csv(output_file, index=False) 
    
    return output_csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compte des messages par id ordonnés en ordre croissant')
    parser.add_argument('messages_file', metavar='messages', type=str,
                        help='chemin du fichier csv contenant la liste des messages')
    parser.add_argument('users_file', metavar='users', type=str,
                        help='chemin du fichier csv contenant la liste des utilisateurs')
    parser.add_argument('output_file', metavar='output', type=str,
                        help='chemin du fichier csv de sortie contenant le compte des messages par id ordonnés en ordre croissant')
    args = parser.parse_args()
    try:
        sort_count_msg_by_id(args.messages_file, args.users_file, args.output_file)
    except FileExistsError:
        print('Le fichier existe déjà !')
