import requests, threading, pickle, random, sys, glob, os
from utils import *
from pprint import pprint
from bs4 import BeautifulSoup

accounts_created = 0
accounts_joined = 0
accounts_favorited = 0
accounts_followed = 0
used_proxies = []


PATH = "./cookies/" # SERVER
PATH = ".\\cookies\\" # COMPUTER

class myThread(threading.Thread):
	global used_proxies
	global accounts_joined
	global accounts_favorited
	global accounts_followed

	def __init__(self, username=None, proxies=None, group=None, favorite=None, follow=None):
		threading.Thread.__init__(self)
		self.username = username or get_random_name()
		self.password = "Boasondas12@"
		self.email = "{0}@30wave.com".format(self.username)
		self.s = requests.Session()
		self.cookies = None
		self.proxies = proxies or self.scrape()
		self.proxy = None
		self.group = group
		self.should_create = not username
		self.favorite = favorite
		self.follow = follow
		self.successfully_created = True

	def run(self):
		if self.should_create:
			self.create()
			if self.successfully_created:
				print("{0.username} {0.favorite}".format(self))
		if self.group and self.successfully_created:
			self.cookies = self.get_cookies()
			self.join_group()
		if self.favorite and self.successfully_created:
			self.cookies = self.get_cookies()
			self.favorite_item()
		if self.follow and self.successfully_created:
			self.cookies = self.get_cookies()
			self.follow_user()
		# self.scrape()

	def follow_user(self, amount = 1):
		def retry():
			self.new_proxy()
			if amount < 5:
				try:
					self.follow_user(amount = amount + 1)
				except Exception as e2:
					print("{0.username} -> ERROR2 -> {1}".format(self, str(e2)))
			else:
				pass
		print("{0.username} following user attempt #{1}".format(self, amount))
		headers = """
			Connection: keep-alive
			Upgrade-Insecure-Requests: 1
			User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
			Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
			Accept-Encoding: gzip, deflate, sdch, br
			Accept-Language: en-US,en;q=0.8
		"""
		try:
			r = self.s.get(url = self.follow,
					headers = string_to_dict(headers),
					timeout = 10,
					cookies = self.cookies,
					# proxies = self.proxy,
					verify = False)
			csrf = r.text.split("setToken('")[1].split("'")[0]

			headers = """
				Host: www.roblox.com
				Connection: keep-alive
				Content-Length: {}
				Pragma: no-cache
				Cache-Control: no-cache
				Accept: */*
				Origin: https://www.roblox.com
				X-CSRF-TOKEN: {}
				User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
				Content-Type: application/x-www-form-urlencoded; charset=UTF-8
				Referer: {}
				Accept-Encoding: gzip, deflate, br
				Accept-Language: en-US,en;q=0.8
			"""
			data = "targetUserId={}".format(self.follow.split("/")[-2])
			headers = headers.format(len(data), csrf, self.follow)
			r = self.s.post(url = "https://www.roblox.com/user/follow",
							data = data,
							headers = string_to_dict(headers),
							cookies = self.cookies,
							# proxies = self.proxy,
							verify = False)
			if r.status_code == 200 and "{\"success\":true}" in r.text:
				print("{0.username} successfully followed user {0.follow}".format(self))
				with open("history.txt", "a") as f:
					f.write("{0.username}:{0.follow}\n".format(self))
				global accounts_followed
				accounts_followed += 1
				return True
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			retry()
			return

		if r.text == "{\"success\":false,\"message\":\"Whoa. Slow down.\"}":
			print("{0.username} going too fast, waiting 1 minute.".format(self))
			sleep(60)
			retry()
			return False
		print("{0.username} could not follow user {0.follow}. Reason: {1}".format(self, r.text))
		return False

	def favorite_item(self, amount = 1):
		def retry():
			self.new_proxy()
			if amount < 5:
				try:
					self.favorite_item(amount = amount + 1)
				except Exception as e2:
					print("{0.username} -> ERROR2 -> {1}".format(self, str(e2)))
			else:
				pass
		print("{0.username} favoriting item attempt #{1}".format(self, amount))
		headers = """
			Connection: keep-alive
			Upgrade-Insecure-Requests: 1
			User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
			Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
			Accept-Encoding: gzip, deflate, sdch, br
			Accept-Language: en-US,en;q=0.8
		"""
		try:
			r = self.s.get(url = self.favorite,
					headers = string_to_dict(headers),
					timeout = 10,
					cookies = self.cookies,
					# proxies = self.proxy,
					verify = False)
			csrf = r.text.split("setToken('")[1].split("'")[0]

			headers = """
				Host: www.roblox.com
				Connection: keep-alive
				Content-Length: {}
				Pragma: no-cache
				Cache-Control: no-cache
				Accept: */*
				Origin: https://www.roblox.com
				X-CSRF-TOKEN: {}
				User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
				Content-Type: application/x-www-form-urlencoded; charset=UTF-8
				Referer: {}
				Accept-Encoding: gzip, deflate, br
				Accept-Language: en-US,en;q=0.8
			"""
			data = "assetID={}".format(self.favorite.split("/")[-2])
			headers = headers.format(len(data), csrf, self.favorite)
			r = self.s.post(url = "https://www.roblox.com/favorite/toggle",
							data = data,
							headers = string_to_dict(headers),
							cookies = self.cookies,
							# proxies = self.proxy,
							verify = False)
			if r.status_code == 200 and "{\"success\":true}" in r.text:
				print("{0.username} successfully liked item {0.favorite}".format(self))
				with open("history.txt", "a") as f:
					f.write("{0.username}:{0.favorite}\n".format(self))
				global accounts_favorited
				accounts_favorited += 1
				return True
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			retry()
			return

		if r.text == "{\"success\":false,\"message\":\"Whoa. Slow down.\"}":
			print("{0.username} going too fast, waiting 1 minute.".format(self))
			sleep(60)
			retry()
			return False
		print("{0.username} could not like {0.favorite}. Reason: {1}".format(self, r.text))
		return False

	def get_cookies(self):
		# print("Logging in as {0.username}".format(self))
		# self.s.cookies.clear()
		# self.s.cookies.update(pickle.load(open("cookies\\{0.username}.p".format(self), "rb")))

		# return pickle.load(open("./cookies/{0.username}.p".format(self), "rb")) # server
		x = None
		with open(PATH + "{0.username}.p".format(self), "rb") as f:
			return pickle.load(f) #computer

	def join_group(self):
		print("{0.username} joining group {0.group}".format(self))
		try:
			headers = """
				Connection: keep-alive
				Upgrade-Insecure-Requests: 1
				User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
				Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
				Accept-Encoding: gzip, deflate, sdch, br
				Accept-Language: en-US,en;q=0.8
			"""
			r = self.s.get(url = self.group,
							headers = string_to_dict(headers),
							timeout = 20,
							cookies = self.cookies,
							verify = False)
			bs = BeautifulSoup(r.text.encode("utf-8"), "html.parser")
			# data = dict((elem.attrs["name"], elem.attrs["value"]) for elem in bs.find_all("input", {"type": "hidden"}) if elem.attrs["name"] and elem.attrs["value"])
			data = {}
			for elem in bs.find_all("input", {"type": "hidden"}):
				if "name" not in elem.attrs: continue
				if "value" not in elem.attrs: continue
				data[elem.attrs["name"]] = elem.attrs["value"]
			data.update({
						"__EVENTTARGET": "JoinGroupDiv",
						"__EVENTARGUMENT": "Click",
						"__LASTFOCUS": "",
						"ctl00$cphRoblox$GroupSearchBar$SearchKeyword": "Search all groups"
						# "ctl00$cphRoblox$rbxGroupRoleSetMembersPane$dlUsers_Footer$ctl01$PageTextBox": "1"
						# "ctl00$cphRoblox$GroupWallPane$GroupWallPager$ctl01$PageTextBox": "1"
						})
			inputs = ["ctl00$cphRoblox$rbxGroupRoleSetMembersPane$dlRolesetList",
					  "ctl00$cphRoblox$rbxGroupRoleSetMembersPane$currentRoleSetID",
					  "ctl00$cphRoblox$rbxGroupRoleSetMembersPane$RolesetCountHidden"]
			data[inputs[0]] = data[inputs[1]]
			data[inputs[2]] = bs.find("input", {"name": inputs[2]}).attrs["value"]

			headers = """
				Connection: keep-alive
				Content-Length: {}
				Pragma: no-cache
				Cache-Control: no-cache
				Origin: https://www.roblox.com
				Upgrade-Insecure-Requests: 1
				User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
				Content-Type: application/x-www-form-urlencoded
				Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
				Referer: {}
				Accept-Encoding: gzip, deflate, br
				Accept-Language: en-US,en;q=0.8
			""".format(len(str(data)), self.group)
			r = self.s.post(url = self.group,
							headers = string_to_dict(headers),
							data = data,
							timeout = 20,
							allow_redirects = True,
							cookies = self.cookies,
							# proxies = self.proxy,
							verify = False)

			if r.status_code == 200 and "/My/" in r.url:
				print("{0.username} successfully joined {0.group}".format(self))
				with open("history.txt", "a") as f:
					f.write("{0.username}:{0.group}\n".format(self))
				global accounts_joined
				accounts_joined += 1
				return True
			# pprint(data)
			dump(r.text)
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			pass
		print("{0.username} could not join {0.group}".format(self))
		return False

	def create(self, amount = 1):
		def retry():
			self.new_proxy()
			if amount < 10:
				try:
					self.create(amount = amount + 1)
				except Exception as e2:
					self.successfully_created = False
					print("{0.username} -> ERROR2 -> {1}".format(self, str(e2)))
			else:
				self.successfully_created = False
				# print("Tried 5 proxies, none of them worked.")
				pass
		print("Creating {0.username}... attempt #{1}".format(self, amount))
		self.s = requests.Session()
		headers = """
			Host: api.roblox.com
			Connection: keep-alive
			Content-Length: {}
			Accept: application/json, text/plain, */*
			Origin: https://www.roblox.com
			User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36
			Content-Type: application/x-www-form-urlencoded
			Referer: https://www.roblox.com/
			Accept-Encoding: gzip, deflate, br
			Accept-Language: en-US,en;q=0.8
		"""
		data = "isEligibleForHideAdsAbTest=True&username={0.username}&password={0.password}&birthday=18+Dec+1941&gender={1}&context=RollerCoasterSignupForm"
		data = data.format(self, random.randint(2, 3))
		headers = headers.format(len(data))

		r = None

		try:
			r = self.s.post(url = "https://api.roblox.com/signup/v1",
							data = data,
							headers = string_to_dict(headers),
							proxies = self.proxy,
							timeout = 10,
							verify = False)
		except Exception as e:
			# print("{0.username} -> ERROR -> {1}".format(self, str(e)))
			self.successfully_created = False
			retry()
			return

		try:
			userID = r.json()["userId"]
			if userID:
				self.userID = userID
				with open("accounts.txt", "a") as f:
					f.write("{0.username}:{0.password}:{0.email}:{0.userID}:{1}\n".format(self, self.proxy["https"].replace("https://", "").replace(":", ",")))
				self.successfully_created = True
				print("Successfully created {0.username}:{0.password}:{0.email}:{0.userID}:{1}".format(self, (self.proxy["https"] or "None").replace("https://", "").replace(":", ",")))
				global accounts_created
				accounts_created += 1
				used_proxies.append(self.proxy)
				self.save_cookies()
		except Exception as e:
			if r.json()["reasons"][0] == "Captcha":
				print("{0.username} -> CAPTCHA".format(self))
				self.successfully_created = False
				retry()
				return
			else:
				self.successfully_created = False
				print("{0.username} -> ERROR -> {1}, {2}".format(self, str(e), r.json()))


	def save_cookies(self):
		pickle.dump(self.s.cookies, open(PATH + "{0.username}.p".format(self), "wb"))

	def new_proxy(self):
		self.proxy = random.choice(self.proxies)
		self.proxy = {"https": "https://" + self.proxy}
		if self.proxy in used_proxies:
			self.new_proxy()
			return
		return self.proxy


def scrape():
	s = requests.Session()
	print("Scraping proxies.")
	proxies_urls = ["http://sslproxies24.blogspot.com/feeds/posts/default",
					"http://proxyserverlist-24.blogspot.com/feeds/posts/default"]
	proxies = []
	r = s.get(url = "http://proxieslounge.blogspot.com/")
	for proxy in r.text.split("style=\"background-color: #ffa123; font-size: 11px; height: 500px; overflow: auto; width: 140px;\">")[1].split("<")[0].split("\n"):
		if not proxy: continue
		proxies.append(proxy)

	for proxies_url in proxies_urls:
		r = s.get(url = proxies_url)

		for proxy in r.text.split("&lt;br /&gt;"):
			if not proxy: continue
			if (len(proxy) > 21 or len(proxy) < 10) or "span" in proxy: continue
			proxies.append(proxy)
	proxies = list(set(proxies))
	print("Found {} proxies".format(len(proxies)))
	return proxies


# for _ in range(40):
# 	manager.load(myThread(proxies=proxies))

# if len(sys.argv) == 3

def get_history():
	try:
		with open("history.txt", "r") as f:
			return f.read()
	except Exception as e:
		return ""

for _ in range(1):
	with open("config.txt", "r") as config:
		config = config.read()
		manager = ThreadManager(MAX_THREADS = int(config.split("\n")[0].split("=")[1]))
		proxies = None
		history = get_history()

		try:
			with open("proxies.txt", "r") as p:
				proxies = p.read().split("\n")
		except Exception as e:
			proxies = scrape()

		create_amount = int(config.split("\n")[1].split("=")[1])
		for _ in range(create_amount):
			manager.load(myThread(proxies=proxies))

		max_amount = 0
		if "amount=" in config:
			max_amount = int(config.split("amount=")[1].split("\n")[0])
			print(max_amount)

		reverse = 1
		offset = 0

		accounts = glob.glob(PATH + "*.p")[::reverse][offset:]
		print(len(accounts))
		random.shuffle(accounts)

		if "join=yes" in config:
			with open("groups.txt", "r") as groups:
				for group in groups.read().split("\n"):
					if not group: continue
					for account in accounts:
						if len(manager.threads) > max_amount: break
						account = account.replace(PATH, "").replace(".p", "")
						manager.load(myThread(proxies=proxies, username=account if not create_amount else None, group=group))

		if "follow=yes" in config:
			with open("follow.txt", "r") as follows:
				for follow in follows.read().split("\n"):
					if not follow: continue
					for account in accounts:
						if len(manager.threads) > max_amount: break
						account = account.replace(PATH, "").replace(".p", "")
						manager.load(myThread(proxies=proxies, username=account if not create_amount else None, follow=follow))

		if "favorite=yes" in config:
			with open("favorites.txt", "r") as favorites:
				for favorite in favorites.read().split("\n"):
					if not favorite: continue
					for account in accounts:
						if len(manager.threads) > max_amount: break
						account = account.replace(PATH, "").replace(".p", "")
						manager.load(myThread(proxies=proxies, username=account if not create_amount else None, favorite=favorite))

		manager.start()

print("{} accounts created.".format(accounts_created))
print("{} accounts joined to group.".format(accounts_joined))
print("{} accounts liked an item.".format(accounts_favorited))
print("{} accounts followed a user.".format(accounts_followed))
# for account in glob.glob("cookies\\*.p")[:10]:
# 	manager.load(myThread(proxies=proxies, username=account[8:-2], favorite="https://www.roblox.com/catalog/590588883/B-W-Nike-Shoes"))
