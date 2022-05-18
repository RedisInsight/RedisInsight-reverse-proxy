import ldap

from prompt_toolkit import prompt

admin_dn = 'cn=admin,dc=ldap-demo,dc=test'
admin_pwd = 'ldap123'

try:
        l = ldap.initialize("ldap://ol:389")

except ldap.LDAPError as e:
    for key, value in e.items():
	    print(value, key)

while True:
        username = prompt("Username: ")
        password = prompt("Password: ", is_password=True)
        try:
	        l.simple_bind_s(admin_dn,admin_pwd)
	        query_user = l.search_s('dc=ldap-demo,dc=test',ldap.SCOPE_SUBTREE, 'uid={}'.format(username))
	        if len(query_user) == 0 or len(query_user[0]) == 0:
	        	print("User not found!")
	        	continue
	        udn = query_user[0][0]
	        print('found DN for user: {}'.format(udn))

	        query_group = l.search_s('dc=ldap-demo,dc=test',ldap.SCOPE_SUBTREE, 'uniquemember={}'.format(udn))
	        for gdn, entry in query_group:
		        print('member of group: {}'.format(gdn))
	
	        l.simple_bind_s(udn, password)
	        print('{} password validated'.format(username))

        except ldap.INVALID_CREDENTIALS:
  	        print('password failed')
