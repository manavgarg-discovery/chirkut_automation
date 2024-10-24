import hvac as hvac
import yaml

config = yaml.safe_load(open("config.yaml"))

for env in config['environments'].keys():
    print("---",env,"---")
    client = hvac.Client(url=config['environments'][env]['url'], verify=False)

    login_response = client.auth.ldap.login(
        username=config['username'],
        password=config['password'],
    )

    result = client.read(config['environments'][env]['path'])

    print("Username: ", result['data']['username'])
    print("Password: ", result['data']['password'])