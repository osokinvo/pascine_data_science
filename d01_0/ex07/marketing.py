import sys

def list_to_set(l:list):
    return set(l)

def set_to_list(s:set):
    return list(s)

def set_difference(s:set, o:set):
    """
    set - other
    """
    return s - o

def set_union(s:set, other:set):
    """
    set | other
    """
    return s | other

def all_email_accounts(clients:set, participants:set):
    return(set_union(clients, participants))

def not_seen_promotional_email(all_email_accounts:set, recipients:set):
    return(set_difference(all_email_accounts, recipients))

def participants_not_clients(participants:set, clients:set):
    return(set_difference(participants, clients))

def clients_not_participants(clients:set, participants:set):
    return(set_difference(clients, participants))

def marketing():
    if len(sys.argv) == 2:

        clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com', 'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com', 'elon@paypal.com', 'jessica@gmail.com']
        participants = ['walter@heisenberg.com', 'vasily@mail.ru', 'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com', 'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
        recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

        if sys.argv[1] == "call_center":
            clients_set = list_to_set(clients)
            participants_set = list_to_set(participants)
            recipients_set = list_to_set(recipients)
            all_email_accounts_set = all_email_accounts(clients_set, participants_set)
            print(set_to_list(not_seen_promotional_email(all_email_accounts_set, recipients_set)))
        elif sys.argv[1] == "potential_clients":
            clients_set = list_to_set(clients)
            participants_set = list_to_set(participants)
            print(set_to_list(participants_not_clients(participants_set, clients_set)))
        elif sys.argv[1] == "loyalty_program":
            clients_set = list_to_set(clients)
            participants_set = list_to_set(participants)
            print(set_to_list(clients_not_participants(clients_set, participants_set)))
        else:
            raise Exception("Wrong argument input!\nPlease enter one of three:\n'call_center' or 'potential_clients' or 'loyalty_program'.")

if __name__ == '__main__':
    marketing()
