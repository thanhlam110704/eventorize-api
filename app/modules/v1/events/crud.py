from db.base import BaseCRUD


class EventCRUD(BaseCRUD):
    async def get_total_event(self, start_date, end_date):
        # First pipeline to get counts by is_online status
        count_pipeline = [
            {"$match": {"start_date": {"$gte": start_date}, "end_date": {"$lte": end_date}, "deleted_at": None}},
            {"$group": {"_id": "$is_online", "count": {"$sum": 1}}},
        ]

        # Second pipeline to get actual event lists
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
                    # Add any other fields you want to include
                }
            },
            {"$sort": {"start_date": 1}},  # Sort by start date
        ]

        # Execute both pipelines
        count_results = await self.aggregate_by_pipeline(count_pipeline)
        list_results = await self.aggregate_by_pipeline(list_pipeline)

        # Process count results
        total_event_online = 0
        total_event_offline = 0

        for item in count_results:
            if item["_id"] is True:  # For online events
                total_event_online = item["count"]
            else:  # For offline events
                total_event_offline = item["count"]

        # Process list results
        list_event_online = []
        list_event_offline = []

        for event in list_results:
            if event["is_online"] is True:
                list_event_online.append(event)
            else:
                list_event_offline.append(event)

        # Return combined results
        return {"total_event_online": total_event_online, "total_event_offline": total_event_offline, "list_event_online": list_event_online, "list_event_offline": list_event_offline}

    async def get_count_event(self, start_date, end_date):
        pipeline = [
            {"$match": {"start_date": {"$gte": start_date}, "end_date": {"$lte": end_date}, "deleted_at": None}},
            {"$group": {"_id": None, "count": {"$sum": 1}}},
            {"$project": {"_id": 0, "total_events": "$count"}},
        ]

        results = await self.aggregate_by_pipeline(pipeline)

        # Handle the case where there might be no results
        if results and len(results) > 0:
            return results[0]  # Returns {"total_events": count}
        else:
            return {"total_events": 0}
