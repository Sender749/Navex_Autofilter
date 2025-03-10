import pymongo
from info import DATABASE_URI, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]


class UserTracker:
    def __init__(self):
        self.user_collection = mydb["referusers"]
        self.refer_collection = mydb["refers"]
        self.premium_collection = mydb["premium_users"]

    def add_user(self, user_id):
        if not self.is_user_in_list(user_id):
            self.user_collection.insert_one({'user_id': user_id})

    def remove_user(self, user_id):
        self.user_collection.delete_one({'user_id': user_id})

    def is_user_in_list(self, user_id):
        return bool(self.user_collection.find_one({'user_id': user_id}))

    def add_refer_points(self, user_id: int, points: int):
        current_points = self.get_refer_points(user_id) + points
        self.refer_collection.update_one(
            {'user_id': user_id},
            {'$set': {'points': current_points}},
            upsert=True
        )
        
        # ✅ Check if user qualifies for premium
        self.grant_premium_if_eligible(user_id, current_points)

    def get_refer_points(self, user_id: int):
        user = self.refer_collection.find_one({'user_id': user_id})
        return user.get('points', 0) if user else 0

    def is_premium(self, user_id):
        return bool(self.premium_collection.find_one({'user_id': user_id}))

    def grant_premium_if_eligible(self, user_id, points):
        REQUIRED_POINTS = 10  # Set required points for premium

        if points >= REQUIRED_POINTS and not self.is_premium(user_id):
            self.premium_collection.insert_one({'user_id': user_id, 'premium': True})
            print(f"✅ User {user_id} granted premium access!")
            return True
        return False

    def reset_refer_data(self):
        """
        Reset all referral data by clearing both collections.
        Returns the number of documents deleted from each collection.
        """
        # Clear the referusers collection
        user_result = self.user_collection.delete_many({})
        # Clear the refers collection
        refer_result = self.refer_collection.delete_many({})

        return {
            "referusers_deleted": user_result.deleted_count,
            "refers_deleted": refer_result.deleted_count
        }


referdb = UserTracker()
