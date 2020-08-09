# 设置说明

可以通过修改`pekobot-config.yaml`配置文件调整佩可机器人的设置。

```yaml
discord_token：
cogs:
  - nicknames
  - gacha
  - clanbattles
  - news
  - peko
  - setu
```

- `discord_token`: 你的Discord机器人Token
- `cogs`: 佩可机器人需要加载的插件。如果你不想加载某个插件（例如：setu），把它从配置文件中删掉即可。
