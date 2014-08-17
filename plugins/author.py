from whiffle import wikidotapi
from util import hook
import random 

@hook.command
def author(inp,nick = None):
	".author <Author Name> -- Will return details regarding the author"
	api = wikidotapi.connection()
	api.Site = "scp-wiki"
	pages = api.refresh_pages()
	authpages = []
	totalrating = 0
	taletotal = 0
	scptotal = 0
	pagerating = 0
	author = inp
	multimatch = []
	authorpage = ""
	found = 0
	exact = 0
	rewrite =0
	orgauth = ""
	newauth = ""
	rewriteauthor =0
	try:
		for page in pages:
			if "scp" in taglist[page] or "tale" in taglist[page]: #makes sure only articles are counted
				if ":rewrite:" in authorlist[page]: 
					bothauths = authorlist[page].split(":rewrite:")
					orgauth = bothauths[0]
					newauth = bothauths[1]
					if author == newauth: 
						rewriteauthor = 1
				if author == authorlist[page] or rewriteauthor ==1:
					found =1 
					rewriteauthor = 0
					authpages.append(page)
					pagetitle = titlelist[page]
					pagerating = ratinglist[page]
					totalrating = totalrating + pagerating
					if "scp" in taglist[page]:
						scptotal +=1
					if  "tale" in taglist[page]:
						taletotal+=1
				try:
					if inp.lower() in authorlist[page].lower(): #this just matches the author with the first author match
						if inp.lower() == authorlist[page].lower():
							exact +=1
						if exact == 1:
							author = authorlist[page]
							authpages = []
							multimatch = [authorlist[page]]
						elif exact < 1:
							multimatch.append(authorlist[page])
						if inp.lower() in authorlist[page].lower() and found == 0:
							author = authorlist[page]
							if ":rewrite:" in authorlist[page]:
								bothauths = authorlist[page].split(":rewrite:")
								orgauth = bothauths[0]
								newauth = bothauths[1]
								if inp.lower() in orgauth.lower():
									author = orgauth
								if inp.lower() in newauth.lower():
									author = newauth 
								rewrite = 1
							found = 1
							authpages.append(page)
							pagetitle = titlelist[page]
							pagerating = ratinglist[page] 
							totalrating = totalrating + pagerating
							if "scp" in taglist[page]:
								scptotal +=1
							if  "tale" in taglist[page]:
								taletotal+=1
				except AttributeError:
					pass
			else:
				if "author" in taglist[page]:
					if ":rewrite:" in authorlist[page]:
						bothauths = authorlist[page].split(":rewrite:")
						orgauth = bothauths[0]
						newauth = bothauths[1]
						if newauth == author:
							authorpage = "http://scp-wiki.net/"+page+" - "
					if author == authorlist[page]:
						authorpage = "http://scp-wiki.net/"+page+" - "
	except KeyError:
		pass
	plusauth = []
	moreauthors = 1
	plusauth.append(author)
	for authors in multimatch: #checks to see if multiple authors found 
		z =0 
		if ":rewrite:" in authors:
			continue 
		for foundauthor in plusauth:
			if foundauthor ==authors:
				z =1
		if authors != author:
			if z == 0:
				moreauthors +=1
				plusauth.append(authors)
	if moreauthors>1:
		x = 0
		final = "Did you mean "
		for auth in plusauth:
			x+=1
			if x ==1:
				final+=auth+""
			if x ==2 and moreauthors ==2:
				final+=" or "+auth+"?"
			if x==2 and moreauthors >2:
				final+=", "+auth+""
			if x==3 and moreauthors ==3:
				final += ", or "+auth+"?"
			if x==3 and moreauthors >3:
				final += ", or "+auth+"? With " + str(moreauthors) + " more authors matching your query."
		randval = random.randint(0,5)
		if randval == 1:
			final += " So be more specific, jerk. >:|"
		if randval == 2:
			final += " Hey "+nick+"! Know what you want!"
		return final
	avgrating = 0
	if taletotal+scptotal is not 0: #just so no division by zero
		avgrating = totalrating/(taletotal+scptotal)
	if not authpages: #if no author pages are added 
		randint = random.randint(0,8)
		if randint ==0:
			return "Maybe you should take some time to remember their name, because I didn't find anything."
		if randint == 1:
			return "I got nothing buddy."
		return "Author not found."
	final = authorpage+""+author +" has written " + str(scptotal) + " SCPs and "+str(taletotal)+" tales. They have " + str(totalrating)+ " net upvotes with an average rating of " + str(avgrating) + ". Their most recent article is " + pagetitle + "(Rating:" + str(pagerating) + ")"
	randint = random.randint(0,7)
	if randint==2:
		final = authorpage+"buttlord("+author +") has written " + str(scptotal) + " SCPs and "+str(taletotal)+" tales. They have " + str(totalrating)+ " net upvotes with an average rating of " + str(avgrating) + ". Their most recent article is " + pagetitle + "(Rating:" + str(pagerating) + ")"
	if randint==1:
		final += " They're also a "+random.choice(["jerk","goofball","butt"])
	if author == "Pixeltasim":
		tempauth = random.choice(["Botlord","Cool Guy Numero Uno","Pixeltasim","Bestest guy ever","Why don't you love him?","Pixelspasm"])
		return authorpage+""+tempauth+" has written " + str(scptotal) + " SCPs and "+str(taletotal)+" tales. They have " + str(totalrating)+ " net upvotes with an average rating of " + str(avgrating) + ". Their most recent article is " + pagetitle + "(Rating:" + str(pagerating) + ")"
	return final