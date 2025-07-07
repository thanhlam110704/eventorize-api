from bson import ObjectId
from db.base import BaseCRUD


class OrderItemsCRUD(BaseCRUD):
    async def get_by_id(self, _id, fields_limit: list = None, query: dict = None) -> dict | None:
        _id = ObjectId(_id)
        fields_limit = await self.build_field_projection(fields_limit=fields_limit)
        _query = {"_id": _id}
        if query:
            _query.update(query)

        pipeline = [
            {"$match": _query},
            {"$addFields": {"ConvertObjectId": {
                "$cond": {
                    "if": {"$and": [{"$ne": ["$ticket_id", None]}, {"$regexMatch": {"input": "$ticket_id", "regex": "^[0-9a-fA-F]{24}$"}}]},
                    "then": {"$toObjectId": "$ticket_id"},
                    "else": None
                }
            }}},
            {"$lookup": {"from": "tickets", "localField": "ConvertObjectId", "foreignField": "_id", "as": "ticketInfo"}},
            {"$unwind": {"path": "$ticketInfo", "preserveNullAndEmptyArrays": True}},
            {"$addFields": {"convertedEventId": {
                "$cond": {
                    "if": {"$and": [{"$ne": ["$ticketInfo.event_id", None]}, {"$regexMatch": {"input": "$ticketInfo.event_id", "regex": "^[0-9a-fA-F]{24}$"}}]},
                    "then": {"$toObjectId": "$ticketInfo.event_id"},
                    "else": None
                }
            }}},
            {"$lookup": {"from": "events", "localField": "convertedEventId", "foreignField": "_id", "as": "eventInfo"}},
            {"$unwind": {"path": "$eventInfo", "preserveNullAndEmptyArrays": True}},
            {"$addFields": {
                "ticket_title": "$ticketInfo.title",
                "event_id": "$ticketInfo.event_id",
                "event_title": "$eventInfo.title",
                "event_thumbnail": "$eventInfo.thumbnail",
                "event_address": "$eventInfo.address",
                "event_start_date": "$eventInfo.start_date",
                "event_end_date": "$eventInfo.end_date",
                "_id": {"$toString": "$_id"}
            }},
            {"$project": {"ticketInfo": 0, "eventInfo": 0, "ConvertObjectId": 0, "convertedEventId": 0}},
        ]

        if fields_limit:
            pipeline.append({"$project": fields_limit})

        results = await self.aggregate_by_pipeline(pipeline)
        return results[0] if results else None

    async def get_all(
        self, query: dict = None, search: str = None, search_in: list = None, page: int = None, limit: int = None, fields_limit: list = None, sort_by: str = None, order_by: str = None
    ) -> dict:
        fields_limit = await self.build_field_projection(fields_limit=fields_limit)
        order_by = -1 if order_by == "desc" else 1
        sorting = {sort_by: order_by}

        common_params = {"sort_by", "page", "limit", "fields", "order_by"}
        query = {k: v for k, v in (query or {}).items() if k not in common_params}

        search_query = None
        if "search" in query:
            search = self.replace_special_chars(value=query.pop("search"))
            search_query = {"$or": [{search_key: {"$regex": f".*{search}.*", "$options": "i"}} for search_key in search_in]}

        query = self.convert_bools(query)

        pipeline = [
            {"$match": query},
            {"$addFields": {"ConvertObjectId": {"$toObjectId": "$ticket_id"}}},
            {"$lookup": {"from": "tickets", "localField": "ConvertObjectId", "foreignField": "_id", "as": "ticketInfo"}},
            {"$unwind": {"path": "$ticketInfo", "preserveNullAndEmptyArrays": True}},
            {"$addFields": {"convertedEventId": {"$toObjectId": "$ticketInfo.event_id"}}},
            {"$lookup": {"from": "events", "localField": "convertedEventId", "foreignField": "_id", "as": "eventInfo"}},
            {"$unwind": {"path": "$eventInfo", "preserveNullAndEmptyArrays": True}},
            {"$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [
                        "$$ROOT",
                        {
                            "ticket_title": "$ticketInfo.title",
                            "event_id": "$ticketInfo.event_id",
                            "event_title": "$eventInfo.title",
                            "event_thumbnail": "$eventInfo.thumbnail",
                            "event_address": "$eventInfo.address",
                            "event_start_date": "$eventInfo.start_date",
                            "event_end_date": "$eventInfo.end_date"
                        }
                    ]
                }
            }},
        ]

        if search_query:
            pipeline.append({"$match": search_query})

        pipeline.extend([
            {
                "$facet": {
                    "total_items": [{"$count": "count"}],
                    "results": [
                        {"$sort": sorting},
                        {"$skip": (page - 1) * limit},
                        {"$limit": limit},
                        {"$project": {
                            "ticketInfo": 0,
                            "eventInfo": 0,
                            "ConvertObjectId": 0,
                            "convertedEventId": 0,
                            **fields_limit
                        }},
                    ],
                }
            },
            {"$addFields": {"total_items": {"$ifNull": [{"$arrayElemAt": ["$total_items.count", 0]}, 0]}}},
            {
                "$addFields": {
                    "total_page": {"$cond": {"if": {"$eq": ["$total_items", 0]}, "then": 1, "else": {"$ceil": {"$divide": ["$total_items", limit]}}}},
                    "records_per_page": limit,
                }
            },
            {"$addFields": {"results": {"$map": {"input": "$results", "as": "result", "in": {"$mergeObjects": ["$$result", {"_id": {"$toString": "$$result._id"}}]}}}}},
        ])

        results = await self.aggregate_by_pipeline(pipeline)
        return results[0] if results else None
