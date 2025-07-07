from bson import ObjectId
from db.base import BaseCRUD


class OrderItemsCRUD(BaseCRUD):
    async def get_by_id(self, _id, fields_limit: list = None, query: dict = None) -> dict | None:
        """
        Retrieves a document from the collection based on its ID, with optional field limitations and additional query.

        Args:
            _id (str): The ID of the document to be retrieved.
            fields_limit (str, optional): A comma-separated string of field names to include in the result.
                                        If None, all fields are included.
            query (dict, optional): Additional query criteria to further refine the search.

        Returns:
            dict | None: The retrieved document with `_id` converted to a string, or None if no document is found.
        """
        # Chuyển đổi fields_limit thành định dạng dictionary với giá trị là 1 cho mỗi trường
        fields_limit = await self.build_field_projection(fields_limit=fields_limit)

        # Xây dựng điều kiện truy vấn
        query = {"_id": ObjectId(_id)}
        if query:
            query.update(query)

        pipeline = [
            {"$match": query},
            {"$addFields": {"convertedUserId": {"$toObjectId": "$created_by"}}},
            {"$lookup": {"from": "tickets", "localField": "ConvertObjectId", "foreignField": "_id", "as": "ticketInfo"}},
            {"$unwind": {"path": "$ticketInfo", "preserveNullAndEmptyArrays": True}},  
            # Convert event_id to ObjectId for the next lookup
            {"$addFields": {"convertedEventId": {"$toObjectId": "$ticketInfo.event_id"}}},
            # Lookup to events collection
            {"$lookup": {"from": "events", "localField": "convertedEventId", "foreignField": "_id", "as": "eventInfo"}},
            # Unwind the eventInfo array
            {"$unwind": {"path": "$eventInfo", "preserveNullAndEmptyArrays": True}},
            # Add the needed fields
            {
                "$addFields": {
                    "ticket_title": "$ticketInfo.title",
                    "event_id": "$ticketInfo.event_id",
                    "event_title": "$eventInfo.title",
                    "event_thumbnail": "$eventInfo.thumbnail",
                    "event_address": "$eventInfo.address",
                    "event_start_date": "$eventInfo.start_date",
                    "event_end_date": "$eventInfo.end_date",
                    "_id": {"$toString": "$_id"}
                }
            },
            # Remove the intermediate fields we don't need
            {"$project": {"ticketInfo": 0, "eventInfo": 0, "ConvertObjectId": 0, "convertedEventId": 0}},
        ]

        # Thêm trường giới hạn nếu có
        if fields_limit:
            pipeline.append({"$project": fields_limit})

        # Thực thi pipeline
        results = await self.aggregate_by_pipeline(pipeline)
        return results[0] if results else None

    async def get_all(
        self, query: dict = None, search: str = None, search_in: list = None, page: int = None, limit: int = None, fields_limit: list = None, sort_by: str = None, order_by: str = None
    ) -> dict:
        # Chuyển đổi fields_limit thành dictionary với giá trị 1 cho mỗi trường
        fields_limit = await self.build_field_projection(fields_limit=fields_limit)
        order_by = -1 if order_by == "desc" else 1
        sorting = {sort_by: order_by}

        # Loại bỏ các tham số phân trang và sắp xếp phổ biến khỏi query dictionary
        common_params = {"sort_by", "page", "limit", "fields", "order_by"}
        query = {k: v for k, v in (query or {}).items() if k not in common_params}

        # Xử lý tìm kiếm `$regex` nếu có `search`
        search_query = None
        if "search" in query:
            search = self.replace_special_chars(value=query.pop("search"))
            search_query = {"$or": [{search_key: {"$regex": f".*{search}.*", "$options": "i"}} for search_key in search_in]}

        # Chuyển đổi boolean string thành giá trị boolean
        query = self.convert_bools(query)

        # Xây dựng pipeline
        pipeline = [
            {"$match": query},
            {"$addFields": {"ConvertObjectId": {"$toObjectId": "$ticket_id"}}},
            {"$lookup": {"from": "tickets", "localField": "ConvertObjectId", "foreignField": "_id", "as": "ticketInfo"}},
            {"$unwind": {"path": "$ticketInfo", "preserveNullAndEmptyArrays": True}},  # Giữ giá trị null nếu không tìm thấy document tương ứng
            # Convert event_id to ObjectId for the next lookup
            {"$addFields": {"convertedEventId": {"$toObjectId": "$ticketInfo.event_id"}}},
            # Lookup to events collection
            {"$lookup": {"from": "events", "localField": "convertedEventId", "foreignField": "_id", "as": "eventInfo"}},
            # Unwind the eventInfo array
            {"$unwind": {"path": "$eventInfo", "preserveNullAndEmptyArrays": True}},
            {
                "$replaceRoot": {
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
                }
            },
        ]

        # Chèn `search_query` vào pipeline sau khi `lookup` hoàn tất
        if search_query:
            pipeline.append({"$match": search_query})

        # Tiếp tục các bước phân trang, sắp xếp, và đếm kết quả
        pipeline.extend(
            [
                {
                    "$facet": {
                        "total_items": [{"$count": "count"}],
                        "results": [
                            {"$sort": sorting},
                            {"$skip": (page - 1) * limit},
                            {"$limit": limit},
                            {
                                "$project": {
                                    "ticketInfo": 0,
                                    "eventInfo": 0,
                                    "convertedUserId": 0,
                                    "ConvertObjectId": 0,
                                    "convertedEventId": 0,
                                    **fields_limit
                                }
                            },
                        ],
                    }
                },
                {"$addFields": {"total_items": {"$ifNull": [{"$arrayElemAt": ["$total_items.count", 0]}, 0]}}},
                {
                    "$addFields": {
                        "total_page": {
                            "$cond": {
                                "if": {"$eq": ["$total_items", 0]},
                                "then": 1,
                                "else": {"$ceil": {"$divide": ["$total_items", limit]}}
                            }
                        },
                        "records_per_page": limit,
                    }
                },
                {
                    "$addFields": {
                        "results": {
                            "$map": {
                                "input": "$results",
                                "as": "result",
                                "in": {
                                    "$mergeObjects": ["$$result", {"_id": {"$toString": "$$result._id"}}]
                                }
                            }
                        }
                    }
                },
            ]
        )
        results = await self.aggregate_by_pipeline(pipeline)
        return results[0] if results else None