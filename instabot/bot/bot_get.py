"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

from tqdm import tqdm


def get_media_owner(self, media_id):
    self.api.media_info(media_id)
    try:
        return str(self.api.last_json["items"][0]["user"]["pk"])
    except Exception as ex:
        self.logger.error("Error: get_media_owner(%s)\n%s", media_id, ex)
        return False


def get_popular_medias(self):
    self.api.get_popular_feed()
    return [str(media['pk']) for media in self.api.last_json['items']]


def get_your_medias(self, as_dict=False):
    self.api.get_self_user_feed()
    if as_dict:
        return self.api.last_json["items"]
    return self.filter_medias(self.api.last_json["items"], False)


def get_archived_medias(self, as_dict=False):
    self.api.get_archive_feed()
    if as_dict:
        return self.api.last_json["items"]
    return self.filter_medias(self.api.last_json["items"], False)


def get_timeline_medias(self, filtration=True):
    if not self.api.get_timeline_feed():
        self.logger.warning("Error while getting timeline feed.")
        return []
    return self.filter_medias(self.api.last_json["items"], filtration)


def get_user_medias(self, user_id, filtration=True, is_comment=False):
    user_id = self.convert_to_user_id(user_id)
    self.api.get_user_feed(user_id)
    if self.api.last_json["status"] == 'fail':
        self.logger.warning("This is a closed account.")
        return []
    return self.filter_medias(self.api.last_json["items"], filtration, is_comment=is_comment)


def get_total_user_medias(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    medias = self.api.get_total_user_feed(user_id)
    if self.api.last_json["status"] == 'fail':
        self.logger.warning("This is a closed account.")
        return []
    return self.filter_medias(medias, filtration=False)


def get_user_likers(self, user_id, media_count=10):
    your_likers = set()
    media_items = self.get_user_medias(user_id, filtration=False)
    if not media_items:
        self.logger.warning("Can't get %s medias." % user_id)
        return []
    for media_id in tqdm(media_items[:media_count],
                         desc="Getting %s media likers" % user_id):
        media_likers = self.get_media_likers(media_id)
        your_likers |= set(media_likers)
    return list(your_likers)


def get_hashtag_medias(self, hashtag, filtration=True):
    if not self.api.get_hashtag_feed(hashtag):
        self.logger.warning("Error while getting hashtag feed.")
        return []
    return self.filter_medias(self.api.last_json["items"], filtration)


def get_total_hashtag_medias(self, hashtag, amount=100, filtration=False):
    medias = self.api.get_total_hashtag_feed(hashtag, amount)

    return self.filter_medias(medias, filtration=filtration)


def get_geotag_medias(self, geotag, filtration=True):
    # TODO: returns list of medias from geotag
    pass


def get_locations_from_coordinates(self, latitude, longitude):
    self.api.search_location(lat=latitude, lng=longitude)
    all_locations = self.api.last_json["items"]
    filtered_locations = []

    for location in all_locations:
        location_lat = location["location"]["lat"]
        location_lng = location["location"]["lng"]

        if int(location_lat) == int(latitude) and int(location_lng) == longitude:
            filtered_locations.append(location)

    return filtered_locations


def get_media_info(self, media_id):
    if isinstance(media_id, dict):
        return media_id
    self.api.media_info(media_id)
    if "items" not in self.api.last_json:
        self.logger.info("Media with %s not found." % media_id)
        return []
    return self.api.last_json["items"]


def get_timeline_users(self):
    if not self.api.get_timeline_feed():
        self.logger.warning("Error while getting timeline feed.")
        return []
    return [str(i['user']['pk']) for i in self.api.last_json['items'] if i.get('user')]


def get_hashtag_users(self, hashtag):
    self.api.get_hashtag_feed(hashtag)
    return [str(i['user']['pk']) for i in self.api.last_json['items']]


def get_geotag_users(self, geotag):
    # TODO: returns list user_ids who just posted on this geotag
    pass


def get_user_id_from_username(self, username):
    if username not in self._usernames:
        self.api.search_username(username)
        self.very_small_delay()
        if "user" in self.api.last_json:
            self._usernames[username] = str(self.api.last_json["user"]["pk"])
        else:
            return None
    return self._usernames[username]


def get_username_from_user_id(self, user_id):
    user_info = self.get_user_info(user_id)
    if user_info and "username" in user_info:
        return str(user_info["username"])
    return None  # Not found


def get_user_info(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if user_id not in self._user_infos:
        self.api.get_username_info(user_id)
        last_json = self.api.last_json
        if last_json is None or 'user' not in last_json:
            return False
        user_info = last_json['user']
        self._user_infos[user_id] = user_info
    return self._user_infos[user_id]

def get_profile_pic_url(self, user_id):
    user_info = self.get_user_info(user_id)
    if user_info and "username" in user_info:
        return str(user_info['profile_pic_url'])
    return None

def get_following_count(self, user_id):
    user_info = self.get_user_info(user_id)
    if user_info and "username" in user_info:
        return str(user_info['following_count'])
    return None

def get_follower_count(self, user_id):
    user_info = self.get_user_info(user_id)
    if user_info and "username" in user_info:
        return str(user_info['follower_count'])
    return None

def get_biography(self, user_id):
    user_info = self.get_user_info(user_id)
    if user_info and "username" in user_info:
        return str(user_info['biography'])
    return None


def get_user_followers(self, user_id, nfollows):
    user_id = self.convert_to_user_id(user_id)
    followers = self.api.get_total_followers(user_id, nfollows)
    return [str(item['pk']) for item in followers][::-1] if followers else []


def get_user_following(self, user_id, nfollows=None):
    user_id = self.convert_to_user_id(user_id)
    following = self.api.get_total_followings(user_id, nfollows)
    return [str(item['pk']) for item in following][::-1] if following else []


def get_media_likers(self, media_id):
    self.api.get_media_likers(media_id)
    if "users" not in self.api.last_json:
        self.logger.info("Media with %s not found." % media_id)
        return []
    return list(map(lambda user: str(user['pk']), self.api.last_json["users"]))


def get_media_comments(self, media_id, only_text=False):
    self.api.get_media_comments(media_id)
    if 'comments' not in self.api.last_json:
        return []
    if only_text:
        return [str(item["text"]) for item in self.api.last_json['comments']]
    return self.api.last_json['comments']


def get_media_commenters(self, media_id):
    self.get_media_comments(media_id)
    if 'comments' not in self.api.last_json:
        return []
    return [str(item["user"]["pk"]) for item in self.api.last_json['comments']]


def search_users(self, query):
    self.api.search_users(query)
    if "users" not in self.api.last_json:
        self.logger.info("Users with %s not found." % query)
        return []
    return [str(user['pk']) for user in self.api.last_json['users']]


def get_comment(self):
    try:
        return self.comments_file.random().strip()
    except IndexError:
        return "Wow!"


def get_media_id_from_link(self, link):
    if 'instagram.com/p/' not in link:
        self.logger.error('Unexpected link')
        return False
    link = link.split('/')
    code = link[link.index('p') + 1]

    alphabet = {
        '-': 62, '1': 53, '0': 52, '3': 55, '2': 54, '5': 57, '4': 56,
        '7': 59, '6': 58, '9': 61, '8': 60, 'A': 0, 'C': 2, 'B': 1,
        'E': 4, 'D': 3, 'G': 6, 'F': 5, 'I': 8, 'H': 7, 'K': 10, 'J': 9,
        'M': 12, 'L': 11, 'O': 14, 'N': 13, 'Q': 16, 'P': 15, 'S': 18,
        'R': 17, 'U': 20, 'T': 19, 'W': 22, 'V': 21, 'Y': 24, 'X': 23,
        'Z': 25, '_': 63, 'a': 26, 'c': 28, 'b': 27, 'e': 30, 'd': 29,
        'g': 32, 'f': 31, 'i': 34, 'h': 33, 'k': 36, 'j': 35, 'm': 38,
        'l': 37, 'o': 40, 'n': 39, 'q': 42, 'p': 41, 's': 44, 'r': 43,
        'u': 46, 't': 45, 'w': 48, 'v': 47, 'y': 50, 'x': 49, 'z': 51,
    }

    result = 0
    for char in code:
        result = result * 64 + alphabet[char]
    return result


def get_messages(self):
    if self.api.getv2Inbox():
        return self.api.last_json
    else:
        self.logger.info("Messages were not found, something went wrong.")
        return None


def convert_to_user_id(self, x):
    x = str(x)
    if not x.isdigit():
        x = x.lstrip('@')
        x = self.get_user_id_from_username(x)
    # if type is not str than it is int so user_id passed
    return x
