- Run skill clean code --minimal after feature implementation
- You can take a look at the deployment with command:

Windows:

```
ssh ubuntu@89.168.90.195
```

In WSL you can omit the -i argument.

- Note that on the server there is a pihole instance running and another Telegram bot service deployed, also using nginx. Do not interfere with them.

- Prefer deploying via image rebuild on server, instead of hot-deploying into container. As this uses more disk space, prune occasionally.