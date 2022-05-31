# RedisInsight-reverse-proxy

Sample setup to access RedisInsight behind a reverse proxy. Template project to test different scenarios.
Please notice the following points:

- this is just a skeleton to provide an example
- need to add any custom plugin to integrate Envoy with LDAP
- there is no logout in this example
- TLS/credentials are passed unencrypted


## Envoy

### Steps

```bash
cd envoy
docker-compose up
```

The compose file starts the following containers:
- redisinsight
- envoy
- redis-stack


Just being used as a reverse proxy for now. You can access RedisInsight at `http://localhost:10000`. Envoy admin portal can be viewed at `http://localhost:8005`.

> Envoy provides [external autorization](https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/filters/http/ext_authz/v3/ext_authz.proto). Need to find a service that implements this protocol for LDAP/AD.

## NGINX Basic Auth

The basic auth configuration is stored in `nginx-basicauth` folder. NGINX configured as a  reverse proxy with [basic auth](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/) , user will be prompted for a username and password.

### Steps:
```
cd nginx-basicauth
docker-compose up
```

The compose file starts the following containers:
- redisinsight
- nginx reverse proxy
- redis-stack


You can access RedisInsight at `http://localhost:9000` username and password is `redis` and `password`.

The setup has the following environment variables.

| Name             | container           |
|------------------|:-------------------:|
| `RIPORT`         | Redisinsight port   |
| `NGINX_PORT`     | Reverse proxy URL   |
| `BASIC_USERNAME` | Proxy auth username |
| `BASIC_PASSWORD` | Proxy auth password |

#### Example
```bash
NGINX_PORT=10000 docker-compose up # runs reverse proxy at port 10000
```

#### Note
If you are facing "Operation not permitted" on MacOs. Follow the steps mentioned here: https://stackoverflow.com/questions/58482352/operation-not-permitted-from-docker-container-logged-as-root

## NGINX LDAP/AD

The NGINX LDAP auth configuration is stored in the `nginx-ldap` folder.

### Steps (from project root)

```
cd nginx-ldap
docker-compose up
```

The compose file starts the folllowing containers:
- ldap server
- nginx-ldap authentication daemon
- nginx reverse proxy with LDAP support
- redisinsight
- redis-stack
- ldap users seed

You can access RedisInsight at `http://localhost:12000` and use `adamb` or `danj` with password `ldap123`

More details for LDAP setup can be found [here](https://github.com/nginxinc/nginx-ldap-auth). 

>IMPORTANT according to [bitnami/nginx-ldap-auth-daemon](https://hub.docker.com/r/bitnami/nginx-ldap-auth-daemon) the image and project is deperecated.

The setup has the following environment variables.

| Name             | container           |
|------------------|:-------------------:|
| `RIPORT`         | Redisinsight port   |
| `NGINX_PORT`     | Reverse proxy URL   |

#### Example
```bash
NGINX_PORT=10000 docker-compose up # runs reverse proxy at port 10000
```

#### Don't seed users automatically (Optional)

The users are added automatically by a seed container. In order to not perform this operation, you need to comment `ol-seed` service in [docker-compose file](nginx-ldap/docker-compose.yml).

#### Verify LDAP users for sanity check (Optional)

If you want to verify LDAP users run `docker-compose --profile verify run ol-verify`.

This verification service runs a prompt where you can enter the username and password.


### Verify LDAP manually from host for sanity check (Optional)

All the users have the same password: `ldap123`

You can view the users in the nginx-ldap/data/ldif/users.ldif file.

You can also verify LDAP using LDAP utils. These utils are in the openldap container and also are bundled with MacOS.

Find user  adamb

`ldapsearch -x -H ldap://localhost:389  -w ldap123 -D "cn=admin,dc=ldap-demo,dc=test" -b ou=users,dc=ldap-demo,dc=test "uid=adamb"`

Find all groups user is member of using user's DN

`ldapsearch -x -H ldap://localhost:389  -w ldap123 -D "cn=admin,dc=ldap-demo,dc=test" -b ou=groups,dc=ldap-demo,dc=test "uniqueMember=cn=Adam Barr,ou=users,dc=ldap-demo,dc=test"` 

Verify user can bind using his credentials

`ldapwhoami -vvvv -x  -H ldap://localhost:389  -w ldap123 -D "cn=Adam Barr,ou=users,dc=ldap-demo,dc=test"`

You can also use [Apache LDAP Studio](https://directory.apache.org/studio/) to browse ldap entries or use `ldapsearch` to get all the entries.

`ldapsearch -x -H ldap://localhost:389  -w ldap123 -D "cn=admin,dc=ldap-demo,dc=test" -b dc=ldap-demo,dc=test "*"`

#### Note
If you are facing "Operation not permitted" on MacOs. Follow the steps mentioned here: https://stackoverflow.com/questions/58482352/operation-not-permitted-from-docker-container-logged-as-root
