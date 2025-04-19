from io import BytesIO

import xlsxwriter
from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.base import BaseCRUD
from db.engine import app_engine
from fastapi import BackgroundTasks, Response
from utils import converter

from . import models, schemas

# from modules.v1.collaborators.services import collaborator_services


class OrganizerServices(BaseServices):
    def __init__(self, service_name: str, crud: BaseCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        data["created_by"] = self.get_current_user(commons=commons)
        data["created_at"] = self.get_current_datetime()
        data_save = models.Organizers(**data).model_dump()
        result = await self.save(data=data_save)
        # create collaborator with role Owner
        # await collaborator_services.create_owner(organizer_id=result["_id"], commons=commons)
        return result

    async def edit(self, _id: str, data: schemas.EditRequest, commons: CommonsDependencies) -> dict:
        data["updated_by"] = self.get_current_user(commons=commons)
        data["updated_at"] = self.get_current_datetime()
        return await self.update_by_id(_id=_id, data=data)

    async def export_organizers(self, data) -> dict:
        date = self.get_current_datetime()
        date_str = converter.convert_datetime_to_str(date)
        filename = f"{date_str}-ReportOrganizers.xlsx"

        buffer = BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet("Organizers")

        # Define styles
        header_format = workbook.add_format({"bold": True, "bg_color": "#4F81BD", "color": "white", "align": "center", "valign": "vcenter", "border": 1})

        cell_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1})

        date_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "num_format": "yyyy-mm-dd hh:mm:ss"})

        url_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "color": "blue", "underline": 1})

        # Define necessary fields
        fields = ["name", "email", "phone", "description", "country", "city", "district", "ward", "logo", "facebook", "twitter", "linkedin", "instagram", "created_at"]

        # Column titles (can be customized)
        column_titles = {
            "name": "Organization Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "description": "Description",
            "country": "Country",
            "city": "City",
            "district": "District",
            "ward": "Ward",
            "logo": "Logo URL",
            "facebook": "Facebook",
            "twitter": "Twitter",
            "linkedin": "LinkedIn",
            "instagram": "Instagram",
            "created_at": "Created Date",
        }

        # Write headers
        for col, field in enumerate(fields):
            worksheet.write(0, col, column_titles.get(field, field.replace("_", " ").title()), header_format)

            # Set column width based on content type
            if field in ["description"]:
                worksheet.set_column(col, col, 40)  # Wider for description
            elif field in ["logo", "facebook", "twitter", "linkedin", "instagram"]:
                worksheet.set_column(col, col, 30)  # Wider for URLs
            else:
                worksheet.set_column(col, col, 20)  # Default width

        # Write data
        for row, organizer in enumerate(data, start=1):
            for col, field in enumerate(fields):
                value = organizer.get(field, "")

                # Skip undefined values
                if value == "undefined":
                    value = ""

                # Handle datetime objects
                if field == "created_at" and value:
                    worksheet.write(row, col, value, date_format)
                # Handle URL fields with clickable links
                elif field in ["logo", "facebook", "twitter", "linkedin", "instagram"] and value:
                    worksheet.write_url(row, col, value, url_format, string=value)
                # Handle other values
                else:
                    worksheet.write(row, col, value, cell_format)

        # Add a summary section
        summary_row = len(data) + 3
        worksheet.write(summary_row, 0, "Total Organizations:", header_format)
        worksheet.write(summary_row, 1, len(data), cell_format)

        # Count by country
        countries = {}
        for org in data:
            country = org.get("country", "")
            if country and country != "undefined":
                countries[country] = countries.get(country, 0) + 1

        # Write country distribution
        if countries:
            worksheet.write(summary_row + 1, 0, "Country Distribution:", header_format)
            row_offset = 2
            for country, count in countries.items():
                worksheet.write(summary_row + row_offset, 0, country, cell_format)
                worksheet.write(summary_row + row_offset, 1, count, cell_format)
                row_offset += 1

        # Count by city
        cities = {}
        for org in data:
            city = org.get("city", "")
            if city and city != "undefined":
                cities[city] = cities.get(city, 0) + 1

        # Write city distribution
        if cities:
            city_row = summary_row + len(countries) + 3 if countries else summary_row + 2
            worksheet.write(city_row, 0, "City Distribution:", header_format)
            row_offset = 1
            for city, count in cities.items():
                worksheet.write(city_row + row_offset, 0, city, cell_format)
                worksheet.write(city_row + row_offset, 1, count, cell_format)
                row_offset += 1

        # Close workbook and return response
        workbook.close()
        buffer.seek(0)

        return Response(
            buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
            background=BackgroundTasks(buffer.close()),
        )


organizer_crud = BaseCRUD(database_engine=app_engine, collection="organizers")
organizer_services = OrganizerServices(service_name="organizers", crud=organizer_crud)
