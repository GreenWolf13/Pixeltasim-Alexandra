from util import hook
import random 
from whiffle import wikidotapi

@hook.command("au")
@hook.command("author")
def author(inp,nick = None):
	".author <Author Name> -- Will return details regarding the author"
	authpages = []
	totalrating = 0
	taletotal = 0
	scptotal = 0
	goitotal = 0
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
	pagetitle = ""
	try:
		for page in scppages:
			if "scp" in taglist[page] or "tale" in taglist[page] or "goi-format" in taglist[page]: #makes sure only articles are counted
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
					if  "goi-format" in taglist[page]:
						goitotal+=1
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
							if  "goi-format" in taglist[page]:
								goitotal+=1
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
		return final
	avgrating = 0
	if taletotal+scptotal+goitotal is not 0: #just so no division by zero
		avgrating = totalrating/(taletotal+scptotal+goitotal)
	if not authpages: #if no author pages are added 
		return "Author not found."
	final = authorpage+""+author +" has written " + str(scptotal) + " SCPs, "+str(taletotal)+" tales, and. "+str(goitotal)+" GOI formats. They have " + str(totalrating)+ " net upvotes with an average rating of " + str(avgrating) + ". Their most recent article is " + pagetitle + "(Rating:" + str(pagerating) + ")"
	return final
@hook.command("ad")
@hook.command("authordetails")
def authordetails(inp,nick=None):
	authpages = []
	totalrating = 0
	taletotal = 0
	scptotal = 0
	goitotal = 0
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
	pagetitle = ""
	scprating = 0
	try:
		for page in scppages:
			if "scp" in taglist[page] or "tale" in taglist[page] or "goi-format" in taglist[page]: #makes sure only articles are counted
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
						scprating+=pagerating
					if  "tale" in taglist[page]:
						taletotal+=1
					if  "goi-format" in taglist[page]:
						goitotal+=1
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
								scprating+=pagerating
							if  "tale" in taglist[page]:
								taletotal+=1
							if  "goi-format" in taglist[page]:
								goitotal+=1
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
		return final
	avgrating = 0
	if taletotal+scptotal+goitotal is not 0: #just so no division by zero
		avgrating = totalrating/(taletotal+scptotal+goitotal)
	if not authpages: #if no author pages are added 
		return "Author not found."
	api = wikidotapi.connection()
	api.Site = "alexandra-scp"
	table = ""
	for page in authpages:
		table+="||**"+titlelist[page]+"**||Rating: "+str(ratinglist[page])+"||Tags: "+str(taglist[page])+"|| http://scp-wiki.net/"+page+"||\n"
	api.set_page_item(author.replace(" ","-").lower(), "content", "**Pages Authored:"+str(len(authpages))+"**\n \n**Number of SCPs Written:** "+str(scptotal)+"\n**Number of Tales Written:** "+str(taletotal)+"\n**Number of GOI Formats Written:** "+str(goitotal)+"\n \n**Net Upvotes Received:** "+str(totalrating)+"\n**Average Rating per Page:** "+str(avgrating)+"\n**Average SCP Rating:** "+str(scprating/scptotal)+"\n++ Articles\n||Title||Rating||Tags||Link||\n"+table, create=True)
	return "Author detail page created http://alexandra-scp.wikidot.com/"+author.replace(" ","-").lower()
