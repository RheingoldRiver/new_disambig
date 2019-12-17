from log_into_wiki import *
import mwparserfromhell
import urllib.parse

site = login('bot', 'lol')  # Set wiki
summary = 'Importing skin info from pre-existing pages'  # Set summary

limit = -1

lmt = 0

def get_and_add_info_to_infobox(name, template):
	champion = site.cargoquery(
		tables="SkinImages",
		fields="Champion",
		where='Name=\"%s\"' % name
	)[0]['Champion']
	data_page = site.pages['%s/Skins' % champion]
	locate_old_template_and_add_data_to_new(name, template, data_page)

def locate_old_template_and_add_data_to_new(name, template, data_page):
	for tl in mwparserfromhell.parse(data_page.text()).filter_templates(recursive=False):
		if tl.name == 'ChampionSkinsLine':
			if tl.get('name').value.strip().lower() != name.lower():
				continue
			add_data_from_old_to_new(template, tl)

def add_data_from_old_to_new(template, tl):
	for param in tl.params:
		if not template.has(param.name):
			template.add(param.name, param.value)

passed_startat = True
startat_page = None #'Blood Moon Akali'

for page in site.categories['Skins']:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	print ('Starting page %s....' % page.name)
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if tl_matches(template, ['Infobox Skin']):
			get_and_add_info_to_infobox(page.name, template)
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
