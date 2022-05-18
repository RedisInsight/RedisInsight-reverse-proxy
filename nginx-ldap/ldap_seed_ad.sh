OPEN_LDAP_CONTAINER=ol

docker exec $OPEN_LDAP_CONTAINER ldapadd \
-a -x -h localhost -p 389 \
-D "cn=admin,dc=ldap-demo,dc=test" \
-f /data/ldif/overlay.ldif \
-w ldap123 \
-c

docker exec $OPEN_LDAP_CONTAINER ldapadd \
-a -x -h localhost -p 389 \
-D "cn=admin,dc=ldap-demo,dc=test" \
-f /data/ldif/referential.ldif \
-w ldap123 \
-c

docker exec $OPEN_LDAP_CONTAINER ldapmodify \
-a -x -h localhost -p 389 \
-D "cn=admin,dc=ldap-demo,dc=test" \
-f /data/ldif/ad.ldif \
-w ldap123 \
-c
