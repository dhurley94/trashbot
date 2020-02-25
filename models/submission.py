from __future__ import print_function
import logging
from datetime import datetime
from pynamodb import models
from pynamodb.attributes import (BooleanAttribute, ListAttribute, MapAttribute,
                                 NumberAttribute, UnicodeAttribute,
                                 UTCDateTimeAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

logging.basicConfig()
LOGGER = logging.getLogger("dynamodb")
LOGGER.setLevel(logging.DEBUG)
LOGGER.propagate = True


class VoteMap(MapAttribute):

    voter_id = UnicodeAttribute(null=False)
    vote = BooleanAttribute(null=False)
    voted_at = UTCDateTimeAttribute(null=False)


class Submissions(models.Model):
    class Meta:
        table_name = "Submissions"
        region = "us-east-1"
        read_capacity_units = 2
        write_capacity_units = 1

    class TwitchUserIndex(GlobalSecondaryIndex):
        class Meta:
            read_capacity_units = 1
            write_capacity_units = 1
            projection = AllProjection()

        twitch_user = UnicodeAttribute(hash_key=True)

    uri = UnicodeAttribute(hash_key=True, null=False)
    twitch_user_index = TwitchUserIndex()
    twitch_user = UnicodeAttribute(null=False)
    url = UnicodeAttribute(null=False)
    votes = ListAttribute(of=VoteMap, default=list)
    created_at = UTCDateTimeAttribute(default=datetime.utcnow())
