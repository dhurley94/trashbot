import logging
from datetime import datetime
from exceptions import SubmissionException, VoteException

from pynamodb.exceptions import DoesNotExist, TableDoesNotExist

from models.submission import Submissions, VoteMap

logging.basicConfig()
LOGGER = logging.getLogger("database")
LOGGER.setLevel(logging.INFO)


class Vote:
    def __init__(self, **kwargs):
        self.voter_id = kwargs["voter_id"]
        self.vote = kwargs["vote"]


class Submission:
    def __init__(self, **kwargs):
        self.uri = kwargs["uri"]
        self.url = kwargs["url"]
        self.twitch_user = kwargs["twitch_user"]
        self.voters = list()


class SubmissionManager:
    """
    Interface to cast votes and handle submissions within the table
    """

    @staticmethod
    def create_table():
        """

        :return:
        """
        return Submissions.create_table()

    @staticmethod
    def delete_table():
        """

        :return:
        """
        return Submissions.delete_table()

    @staticmethod
    def get_submission_by_uri(uri):
        LOGGER.info("Getting %s", uri)
        try:
            return Submissions.get(uri)
        except DoesNotExist as error:
            raise error
        except TableDoesNotExist as error:
            raise error

    @staticmethod
    def exists():
        return Submissions.exists()

    @staticmethod
    def get_submissions_by_user(twitch_user):
        submissions = list()
        for submission in Submissions.twitch_user_index.query(twitch_user):
            submissions.append(submission.__dict__["attribute_values"])
        return submissions

    @staticmethod
    def list_submissions():
        return Submissions.scan()

    @staticmethod
    def create_submission(*args, **kwargs):
        """

        :param url:
        :return:
        """
        try:
            SubmissionManager.get_submission_by_uri(kwargs["uri"])
            LOGGER.info("%s already exists.", kwargs["uri"])
        except DoesNotExist:
            LOGGER.info(
                "Creating a submission %s from %s", kwargs["uri"], kwargs["twitch_user"]
            )
            submission = Submissions(
                uri=kwargs["uri"], url=kwargs["url"], twitch_user=kwargs["twitch_user"]
            )
            submission.save()

    @staticmethod
    def has_voted(submission, *args, **kwargs):
        """

        :param submission:
        :param args:
        :param kwargs:
        :return:
        """
        LOGGER.info("%s has %d votes", submission.uri, len(submission.votes))
        for voter in submission.votes:
            voter = voter.__dict__["attribute_values"]
            if kwargs["voter_id"] in voter["voter_id"]:
                LOGGER.info("Found %s in %s", kwargs["voter_id"], submission.uri)
                return True
        LOGGER.info("User %s was not found in %s", kwargs["voter_id"], submission.uri)
        return False

    @staticmethod
    def cast_vote(*args, **kwargs):
        """
        If the submission exists and the voter has not yet voted submission a new vote is cast

        :param args:
        :param kwargs:
            - uri:URI of Twitch Clip
            - user_id:Twitch User ID
            - vote:Bool
        :return:
        """
        submission = SubmissionManager.get_submission_by_uri(uri=kwargs["uri"])
        if not SubmissionManager.has_voted(submission, voter_id=kwargs["voter_id"]):
            vote = VoteMap(
                voter_id=kwargs["voter_id"],
                vote=kwargs["vote"],
                voted_at=datetime.utcnow(),
            )
            submission.votes.append(vote)
            return submission.save()
        raise VoteException(400, f"Voter already has cast vote for {kwargs['uri']}")
