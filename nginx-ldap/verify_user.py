import argparse
import ldap

# create parser
parser = argparse.ArgumentParser()
 
# add arguments to the parser
parser.add_argument('-u', '--username', type=str)
parser.add_argument('-p', '--password', type=str)
args = parser.parse_args()

admin_dn = 'cn=admin,dc=ldap-demo,dc=test'
admin_pwd = 'ldap123'

try:
	l = ldap.initialize("ldap://localhost:389")


except ldap.LDAPError as e:
    for key, value in e.items():
	    print(value, key)

try:

	l.simple_bind_s(admin_dn,admin_pwd)
	query_user = l.search_s('dc=ldap-demo,dc=test',ldap.SCOPE_SUBTREE, 'uid={}'.format(args.username))
	udn = query_user[0][0]
	print('found DN for user: {}'.format(udn))

	query_group = l.search_s('dc=ldap-demo,dc=test',ldap.SCOPE_SUBTREE, 'uniquemember={}'.format(udn))
	for gdn, entry in query_group:
		print('member of group: {}'.format(gdn))
	
	l.simple_bind_s(udn, args.password)
	print('{} password validated'.format(args.username))

except ldap.INVALID_CREDENTIALS:
  	print('password failed')

