from datetime import datetime, timedelta
import pytz
from db.base import BaseCRUD
from core.schemas import CommonsDependencies

class EventCRUD(BaseCRUD):
    async def get_events_by_date_filter(self, date_filter: str, is_online: bool = None, city: str = None, page: int = 1, limit: int = 20, commons: CommonsDependencies = None):
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        current_date = datetime.now(timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        
        if date_filter == "today":
            start_date = current_date
            end_date = current_date + timedelta(days=1)
        elif date_filter == "tomorrow":
            start_date = current_date + timedelta(days=1)
            end_date = current_date + timedelta(days=2)
        elif date_filter == "this_week":
            # Tính ngày thứ Hai của tuần hiện tại
            days_to_monday = (current_date.weekday() % 7)  # weekday(): 0 = Thứ Hai, 6 = Chủ Nhật
            start_date = current_date - timedelta(days=days_to_monday)
            # Tính ngày Chủ Nhật (cuối tuần)
            end_date = start_date + timedelta(days=7)
        else:
            raise ValueError("Invalid date filter. Use 'today', 'tomorrow', or 'this_week'.")

        filter_conditions = {
            "start_date": {
                "$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "$lt": end_date.strftime("%Y-%m-%d %H:%M:%S")
            },
            "deleted_at": None
        }

        if is_online is not None:
            filter_conditions["is_online"] = is_online
        
        if city is not None:
            filter_conditions["city"] = city

        pipeline = [
            {"$match": filter_conditions},
            {"$skip": (page - 1) * limit},
            {"$limit": limit},
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "title": 1,
                    "description": 1,
                    "is_online": 1,
                    "start_date": 1,
                    "end_date": 1,
                    "organizer_id": 1,
                    "thumbnail": 1,
                    "link": 1,
                    "address": 1,
                    "district": 1,
                    "ward": 1,
                    "city": 1,
                    "country": 1,
                    "created_at": 1,
                    "created_by": 1,
                    "updated_at": 1,
                    "updated_by": 1,
                }
            },
            {"$sort": {"start_date": 1}},
        ]

        count_pipeline = [
            {"$match": filter_conditions},
            {"$count": "total"}
        ]

        results = await self.aggregate_by_pipeline(pipeline)
        count_result = await self.aggregate_by_pipeline(count_pipeline)
        
        total_items = count_result[0]["total"] if count_result else 0
        total_page = 0 if total_items == 0 else (total_items + limit - 1) // limit

        return {
            "results": results,
            "total_items": total_items,
            "total_page": total_page,
            "records_per_page": len(results)
        }

    async def get_total_event(self, start_date, end_date):
        count_pipeline = [
            {"$match": {"start_date": {"$gte": start_date}, "end_date": {"$lte": end_date}, "deleted_at": None}},
            {"$group": {"_id": "$is_online", "count": {"$sum": 1}}},
        ]

        list_pipeline = [
            {"$match": {"start_date": {"$gte": start_date}, "end_date": {"$lte": end_date}, "deleted_at": None}},
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "title": 1,
                    "description": 1,
                    "is_online": 1,
                    "start_date": 1,
                    "end_date": 1,
                }
            },
            {"$sort": {"start_date": 1}},
        ]

        count_results = await self.aggregate_by_pipeline(count_pipeline)
        list_results = await self.aggregate_by_pipeline(list_pipeline)

        total_event_online = 0
        total_event_offline = 0

        for item in count_results:
            if item["_id"] is True:
                total_event_online = item["count"]
            else:
                total_event_offline = item["count"]

        list_event_online = []
        list_event_offline = []

        for event in list_results:
            if event["is_online"] is True:
                list_event_online.append(event)
            else:
                list_event_offline.append(event)

        return {
            "total_event_online": total_event_online,
            "total_event_offline": total_event_offline,
            "list_event_online": list_event_online,
            "list_event_offline": list_event_offline
        }

    async def get_count_event(self, start_date, end_date):
        pipeline = [
            {"$match": {"start_date": {"$gte": start_date}, "end_date": {"$lte": end_date}, "deleted_at": None}},
            {"$group": {"_id": None, "count": {"$sum": 1}}},
            {"$project": {"_id": 0, "total_events": "$count"}},
        ]

        results = await self.aggregate_by_pipeline(pipeline)
        return results[0] if results and len(results) > 0 else {"total_events": 0}