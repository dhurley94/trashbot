

class Twitch:
    def __init__(self):
        pass


class TwitchUrl(Twitch):
    def __init__(self, url):
        self.url = url

    def parse_url(self):
        """

        '!"#$%&\'()*+,-./@:;<=>[\\]^_`{|}~' verifies url is valid
        twitch.tv\/[a-zA-Z0-9]*/clip/[a-zA-Z]* verifies url is twitch
        example url
        https://clips.twitch.tv/DistinctBenevolentTriangleKippa
        :return:
        """
        url = self.url.split("/")
        if "twitch" in url[-2]:
            return {"twitch_user": "undefined", "uri": url[-1], "url": self.url}
        return {"twitch_user": url[-3], "uri": url[-1], "url": self.url}
