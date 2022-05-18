# RedisInsight-reverse-proxy

Sample setup to access RedisInsight behind a reverse proxy. Template project to test different scenarios.
Please notice the following points:

- this is just a skeleton to provide an example
- need to add any custom plugin to integrate Envoy with LDAP
- there is no logout in this example
- TLS/credentials are passed unencrypted

## Setup
Clone the repository and then run `docker-compose up`


## Envoy
Just being used as a reverse proxy for now. You can access RedisInsight at `http://localhost:10000`

> Envoy provides [external autorization](https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/filters/http/ext_authz/v3/ext_authz.proto). Need to find a service that implements this protocol for ldap/AD.

## Nginx Basic Auth

The ldap auth configuration is stored in `nginx-basicauth` folder.

Nginx configured as a  reverse proxy with [basic auth](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/) , user will be prompted for a username and password.

You can access RedisInsight at `http://localhost:9000` username and password is `redis` and `password` configured in [docker-compose file](nginx-basicauth/docker-compose.yml)

## LDAP/AD

The ldap auth configuration is stored in `nginx-ldap` folder.

`./ldap_seed.sh` to seed the open ldap server with users and groups. This is done automatically. In order to prevent this, comment `ol-seed` service in [docker-compose file](nginx-ldap/docker-compose.yml)

### Verify LDAP (Optional)

All the users have the same password: `ldap123`

There is a service which allows you to authenticate a user outside of RS wich is a nice sanity check.

`docker-compose --profile verify run ol-verify`

You can view the users in the nginx-ldap/data/ldif/users.ldif file.

You can also verify ldap using ldap utils. These utils are in the openldap container and also are bundled with Mac OS.

Find user  adamb

`ldapsearch -x -H ldap://localhost:389  -w ldap123 -D "cn=admin,dc=ldap-demo,dc=test" -b ou=users,dc=ldap-demo,dc=test "uid=adamb"`

Find all groups user is member of using user's DN

`ldapsearch -x -H ldap://localhost:389  -w ldap123 -D "cn=admin,dc=ldap-demo,dc=test" -b ou=groups,dc=ldap-demo,dc=test "uniqueMember=cn=Adam Barr,ou=users,dc=ldap-demo,dc=test"` 

Verify user can bind using his credentials

`ldapwhoami -vvvv -x  -H ldap://localhost:389  -w ldap123 -D "cn=Adam Barr,ou=users,dc=ldap-demo,dc=test"`

You can also use [Apache LDAP Studio](https://directory.apache.org/studio/) to browse ldap entries or use `ldapsearch` to get all the entries.

`ldapsearch -x -H ldap://localhost:389  -w ldap123 -D "cn=admin,dc=ldap-demo,dc=test" -b dc=ldap-demo,dc=test "*"`


## Nginx LDAP
Make sure you have seeded ldap. You can access `http://localhost:12000` and use `adamb` or `danj` with password `ldap123`
More details for ldap setup can be found [here](https://github.com/nginxinc/nginx-ldap-auth). 

>IMPORTANT according to [bitnami/nginx-ldap-auth-daemon](https://hub.docker.com/r/bitnami/nginx-ldap-auth-daemon) the image and project is deperecated.
