import datetime
from io import BytesIO

import xlsxwriter
from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.engine import app_engine
from fastapi import BackgroundTasks, Response
from utils import converter

from . import models, schemas
from .crud import EventCRUD


class EventServices(BaseServices):
    def __init__(self, service_name: str, crud: EventCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data["created_by"] = self.get_current_user(commons=commons)
        data["created_at"] = self.get_current_datetime()
        data_save = models.Events(**data).model_dump()
        return await self.save(data=data_save)

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        data["updated_by"] = self.get_current_user(commons=commons)
        data["updated_at"] = self.get_current_datetime()
        return await self.update_by_id(_id=_id, data=data)

    async def get_total_event(self, start_date, end_date):
        return await self.crud.get_total_event(start_date=start_date, end_date=end_date)

    async def get_count_event(self, start_date, end_date):
        return await self.crud.get_count_event(start_date=start_date, end_date=end_date)

    async def export_events(self, data) -> dict:
        date = self.get_current_datetime()
        date_str = converter.convert_datetime_to_str(date)
        filename = f"{date_str}-ReportEvents.xlsx"

        buffer = BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet("Events")

        # Define styles
        header_format = workbook.add_format({"bold": True, "bg_color": "#4F81BD", "color": "white", "align": "center", "valign": "vcenter", "border": 1})

        cell_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1})

        date_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "num_format": "yyyy-mm-dd hh:mm:ss"})

        url_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "color": "blue", "underline": 1})

        boolean_format = workbook.add_format({"align": "center", "valign": "vcenter", "border": 1})

        # Define necessary fields
        fields = [
            "title",
            "organizer_id",
            "description",
            "start_date",
            "end_date",
            "is_online",
            "link",
            "address",
            "city",
            "district",
            "ward",
            "country",
            "thumbnail",
            "created_at",
            "updated_at",
        ]

        # Column titles (can be customized)
        column_titles = {
            "title": "Event Title",
            "organizer_id": "Organizer ID",
            "description": "Description",
            "start_date": "Start Date",
            "end_date": "End Date",
            "is_online": "Online Event",
            "link": "Online Link",
            "address": "Address",
            "city": "City",
            "district": "District",
            "ward": "Ward",
            "country": "Country",
            "thumbnail": "Thumbnail URL",
            "created_at": "Created Date",
            "updated_at": "Last Updated",
        }

        # Write headers
        for col, field in enumerate(fields):
            worksheet.write(0, col, column_titles.get(field, field.replace("_", " ").title()), header_format)

            # Set column width based on content type
            if field in ["description"]:
                worksheet.set_column(col, col, 40)  # Wider for description
            elif field in ["thumbnail", "link"]:
                worksheet.set_column(col, col, 30)  # Wider for URLs
            elif field in ["is_online"]:
                worksheet.set_column(col, col, 15)  # Narrower for boolean
            else:
                worksheet.set_column(col, col, 20)  # Default width

        # Write data
        for row, event in enumerate(data, start=1):
            for col, field in enumerate(fields):
                value = event.get(field, "")

                # Handle empty values
                if value is None or value == "":
                    worksheet.write(row, col, "", cell_format)
                    continue

                # Handle date strings
                if field in ["start_date", "end_date"] and value:
                    try:
                        # Try to parse the date string
                        date_value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                        worksheet.write_datetime(row, col, date_value, date_format)
                    except (ValueError, TypeError):
                        # If parsing fails, write as is
                        worksheet.write(row, col, value, cell_format)

                # Handle datetime objects
                elif field in ["created_at", "updated_at"] and value:
                    worksheet.write_datetime(row, col, value, date_format)

                # Handle boolean values
                elif field == "is_online":
                    worksheet.write(row, col, "Yes" if value else "No", boolean_format)

                # Handle URL fields with clickable links
                elif field in ["thumbnail", "link"] and value:
                    worksheet.write_url(row, col, value, url_format, string=value)

                # Handle other values
                else:
                    worksheet.write(row, col, value, cell_format)

        # Add a summary section
        summary_row = len(data) + 3
        worksheet.write(summary_row, 0, "Total Events:", header_format)
        worksheet.write(summary_row, 1, len(data), cell_format)

        # Count online vs offline events
        online_count = sum(1 for event in data if event.get("is_online", False))
        offline_count = len(data) - online_count

        worksheet.write(summary_row + 1, 0, "Online Events:", header_format)
        worksheet.write(summary_row + 1, 1, online_count, cell_format)

        worksheet.write(summary_row + 2, 0, "Offline Events:", header_format)
        worksheet.write(summary_row + 2, 1, offline_count, cell_format)

        # Calculate event duration statistics
        durations = []
        for event in data:
            try:
                start = datetime.datetime.strptime(event.get("start_date", ""), "%Y-%m-%d %H:%M:%S")
                end = datetime.datetime.strptime(event.get("end_date", ""), "%Y-%m-%d %H:%M:%S")
                duration_days = (end - start).days
                durations.append(duration_days)
            except (ValueError, TypeError):
                continue

        if durations:
            avg_duration = sum(durations) / len(durations)
            max_duration = max(durations)
            min_duration = min(durations)

            worksheet.write(summary_row + 4, 0, "Event Duration Statistics (days):", header_format)
            worksheet.write(summary_row + 5, 0, "Average Duration:", cell_format)
            worksheet.write(summary_row + 5, 1, round(avg_duration, 1), cell_format)

            worksheet.write(summary_row + 6, 0, "Longest Event:", cell_format)
            worksheet.write(summary_row + 6, 1, max_duration, cell_format)

            worksheet.write(summary_row + 7, 0, "Shortest Event:", cell_format)
            worksheet.write(summary_row + 7, 1, min_duration, cell_format)

        # Close workbook and return response
        workbook.close()
        buffer.seek(0)

        return Response(
            buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
            background=BackgroundTasks(buffer.close()),
        )

    async def get_event_by_organizer_id(self, organizer_id: str, commons: CommonsDependencies = None) -> list:
        return await self.get_all(query={"organizer_id": organizer_id}, commons=commons)


event_crud = EventCRUD(database_engine=app_engine, collection="events")
event_services = EventServices(service_name="events", crud=event_crud)
