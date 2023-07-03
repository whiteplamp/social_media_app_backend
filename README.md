# Webtronics test task solution

## How to deploy
### Linux
#### Install [Docker]("https://docs.docker.com/engine/install/ubuntu/") and [Docker compose]("https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04") (Step 1 from link)
#### Add [Docker to sudo]("https://docs.docker.com/engine/install/linux-postinstall/")(Step: manage docker as non-root user)

### Clone repository
```sh
git clone https://github.com/whiteplamp/test_task_for_webtronics
cd test_task_for_webtronics/
```

### Specify .env variables

```sh
touch .env
```
### Generate random hex

```sh
openssl rand -hex 32
```

<p>Then open .env file with vim/nano/any text redactor u prefer and specify DB_NAME, DB_USER, DB_PASS
and JWT_SECRET_KEY with generated random hex. </p>
<p>DB_HOST=localhost</p>
<p>DB_PORT=5432</p>

DB_HOST and DB_PORT can be specified by u, but now solution implies that database is located in the same place as the backend


# Deploy it

```sh
chmod +x deploy.sh
./deploy.sh
```


# Test it

Connect to http://localhost/docs and try Swagger ui
<p>To login into system registrate and get Bearer token then press lock image near the secure routes and place</p>
<p>Bearer token in empty space in format "Bearer {your_token}"</p>
<p>U dont need to place curl brackets. Just remove it when u will place token</p>


