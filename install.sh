sudo cp CacaRankingBot-Telegram-Bot.service /etc/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable CacaRankingBot-Telegram-Bot.service
sudo systemctl start CacaRankingBot-Telegram-Bot.service
