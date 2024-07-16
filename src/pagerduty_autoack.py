import pdpyras, time, re, os

def get_user(session):
    id = None
    response = session.get('users/me')

    if response.ok:
        print(f"The API key belongs to {response.json()['user']['email']}.")
        id = response.json()['user']['id']
    else:
        raise Exception('Failed to get user.')

    return id

def get_incidents(session, user):
    query_string = {"date_range":"all","user_ids[]":user,"statuses[]":"triggered"}
    response = session.list_all('incidents', params=query_string)

    return response

def update_incidents(session, incidents, regex, status):
    for i in incidents:
        id = i['id']
        title = i['title']

        if re.search(regex, title, re.IGNORECASE):
            print(f"Matched triggered incident: {id} - {title}")

            payload = [{"id":id,"type":"incident_reference","status":status}]
            session.rput('incidents', json=payload)
            
            print(f"{status.capitalize()} incident ID {id}.")
        else:
            print(f"Skipping triggered incident: {id} - {title}")

def main():
    API_KEY = os.environ.get('API_KEY')
    session = pdpyras.APISession(API_KEY)

    u_id = get_user(session)
    q_interval = int(os.environ.get('QUERYINTERVAL'))
    regex = os.environ.get('REGEX')
    desired_status = os.environ.get('UPDATESTATUS','acknowledged').lower()

    try:
        while True:
            print('Checking for triggered incidents...')
            incidents = get_incidents(session, u_id)

            if incidents:
                update_incidents(session, incidents, regex, desired_status)
            else:
                print('No new triggered incidents.')

            print(f"Sleeping for {q_interval} seconds.")
            time.sleep(q_interval)
    except Exception as e:
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

if __name__ == '__main__':
    main()
