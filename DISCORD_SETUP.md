# Phi Discord Bot Setup

## Quick Start

1. **Create Discord Application**
   - Go to https://discord.com/developers/applications
   - Click "New Application" → Name it "Phi"
   - Go to "Bot" → Click "Add Bot"
   - Copy the **Token**

2. **Enable Intents**
   - In Bot settings, enable:
     - ✅ Message Content Intent
     - ✅ Server Members Intent

3. **Invite Bot to Server**
   - Go to OAuth2 → URL Generator
   - Select scopes: `bot`, `applications.commands`
   - Select permissions: `Send Messages`, `Read Message History`
   - Copy URL and open in browser to invite

4. **Set Environment Variables**
   ```bash
   export DISCORD_BOT_TOKEN="your-token-here"
   export ANTHROPIC_API_KEY="your-anthropic-key"
   ```

5. **Run the Bot**
   ```bash
   cd phi-autonomous
   pip install discord.py anthropic
   python phi_bot.py discord
   ```

## Usage

In any Discord channel where the bot is present:

```
@Phi what is the Cofree comonad?
```

```
@Phi show me how to define a tensor in Phi
```

```
Phi, explain linear types for quantum computing
```

## Running as a Service

Create `/etc/systemd/system/phi-discord.service`:

```ini
[Unit]
Description=Phi Discord Bot
After=network.target

[Service]
Type=simple
User=patrick
WorkingDirectory=/home/patrick/IdeaProjects/phi-autonomous
Environment=DISCORD_BOT_TOKEN=your-token
Environment=ANTHROPIC_API_KEY=your-key
ExecStart=/usr/bin/python3 phi_bot.py discord
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable phi-discord
sudo systemctl start phi-discord
```

## Create a Phi Discord Server

1. Create server at https://discord.com/
2. Name it "Phi Language"
3. Create channels:
   - #general - General discussion
   - #help - Ask @Phi questions
   - #showcase - Share Phi code
   - #announcements - Release notes

Invite link (once bot is set up):
```
https://discord.gg/YOUR_INVITE_CODE
```
