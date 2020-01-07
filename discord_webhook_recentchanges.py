import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from log_into_wiki import *

site = login('bot', 'lol')

with open('webhook_leona.txt') as f:
	webhook_url = f.read().strip()

webhook = DiscordWebhook(url=webhook_url)

def check_recent_revisions(site):
	then_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
	then = then_time.isoformat()
	now = datetime.datetime.utcnow().isoformat()
	revisions = site.api('query', format='json',
						 list='logevents',
						 lestart=now,
						 leend=then,
						 leprop='details',
						 leimit='max',
						 ledir='older'
						 )
	titles = []
	for log in revisions['query']['logevents']:
		send_event(log['params']['custom-1'])

def send_event(text):
	embed = DiscordEmbed(
		title="News RefreshOverview",
		description=text
	)
	webhook.add_embed(embed)
	webhook.execute()

if __name__ == '__main__':
	site = login('me', 'lol')
	check_recent_revisions(site)
