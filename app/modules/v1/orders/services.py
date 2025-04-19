from datetime import datetime
from io import BytesIO

import xlsxwriter
from core.schemas import CommonsDependencies
from core.services import BaseServices
from db.engine import app_engine
from fastapi import BackgroundTasks, Response
from utils import converter

from . import models, schemas
from .config import settings
from .crud import OrdersCRUD


class OrderServices(BaseServices):
    def __init__(self, service_name: str, crud: OrdersCRUD = None) -> None:
        super().__init__(service_name, crud)

    async def _generate_order_no(self, counter):
        current_year = str(datetime.now().year)[2:]
        current_month = str(datetime.now().month).zfill(2)
        total = await self.crud.count_documents(query={}) + counter
        last_four_digits = str(total)[-4:].zfill(4)
        order_no = current_year + current_month + last_four_digits
        return order_no

    async def create(self, data: schemas.CreateRequest, commons: CommonsDependencies) -> dict:
        # Calculate tax rate, vat amount, and total amount
        order = {}
        order["amount"] = 0
        order["discount_amount"] = 0
        order["vat_amount"] = 0
        order["total_amount"] = 0
        order["tax_rate"] = settings.vat

        for order_item in data["order_items"]:
            order["amount"] += order_item["price"] * order_item["quantity"]
        order["vat_amount"] = order["amount"] * order["tax_rate"]
        order["total_amount"] = order["amount"] + order["vat_amount"]

        order["status"] = "pending"
        order["created_by"] = self.get_current_user(commons=commons)
        order["created_at"] = self.get_current_datetime()
        counter = 0
        while True:
            order["order_no"] = await self._generate_order_no(counter)
            data_save = models.Orders(**order).model_dump()
            result = await self.save_unique(data_save, "order_no", ignore_error=True)
            if result:
                break
            counter += 1
        return result

    async def active(self, order_id: str, commons: CommonsDependencies) -> dict:
        data = {}
        data["status"] = "active"
        data["updated_by"] = self.get_current_user(commons=commons)
        data["updated_at"] = self.get_current_datetime()
        return await self.update_by_id(_id=order_id, data=data)

    async def get_top_buyer(self, start_date, end_date, limit: int = 3):
        return await self.crud.get_top_buyer(start_date=start_date, end_date=end_date, limit=limit)

    async def get_revenue(self, start_date, end_date):
        return await self.crud.get_revenue(start_date=start_date, end_date=end_date)

    async def get_total_orders(self, start_date, end_date):
        return await self.crud.get_total_orders(start_date=start_date, end_date=end_date)

    async def get_total_buyers(self, start_date, end_date):
        return await self.crud.get_total_buyers(start_date=start_date, end_date=end_date)

    async def export_orders(self, data) -> dict:
        date = self.get_current_datetime()
        date_str = converter.convert_datetime_to_str(date)
        filename = f"{date_str}-ReportOrders.xlsx"
        buffer = BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet("Orders")

        # Define styles
        header_format = workbook.add_format({"bold": True, "bg_color": "#4F81BD", "color": "white", "align": "center", "valign": "vcenter", "border": 1})

        cell_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1})

        date_format = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "num_format": "yyyy-mm-dd hh:mm:ss"})

        money_format = workbook.add_format({"align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0 ₫"})

        percent_format = workbook.add_format({"align": "right", "valign": "vcenter", "border": 1, "num_format": "0.0%"})

        status_format_active = workbook.add_format({"align": "center", "valign": "vcenter", "border": 1, "bg_color": "#C6EFCE", "color": "#006100"})

        status_format_pending = workbook.add_format({"align": "center", "valign": "vcenter", "border": 1, "bg_color": "#FFEB9C", "color": "#9C5700"})

        # Define necessary fields
        fields = ["order_no", "status", "user_name", "user_email", "user_phone", "amount", "discount_amount", "tax_rate", "vat_amount", "total_amount", "promotion_code", "notes", "created_at"]

        # Column titles (can be customized)
        column_titles = {
            "order_no": "Order Number",
            "status": "Status",
            "user_name": "Customer Name",
            "user_email": "Customer Email",
            "user_phone": "Customer Phone",
            "amount": "Amount (VND)",
            "discount_amount": "Discount (VND)",
            "tax_rate": "Tax Rate",
            "vat_amount": "VAT Amount (VND)",
            "total_amount": "Total Amount (VND)",
            "promotion_code": "Promotion Code",
            "notes": "Notes",
            "created_at": "Order Date",
        }

        # Write headers
        for col, field in enumerate(fields):
            worksheet.write(0, col, column_titles.get(field, field.replace("_", " ").title()), header_format)

            # Set column width based on content type
            if field in ["user_email", "notes"]:
                worksheet.set_column(col, col, 25)  # Wider for emails and notes
            elif field in ["status", "tax_rate"]:
                worksheet.set_column(col, col, 12)  # Narrower for status and tax rate
            elif field in ["amount", "discount_amount", "vat_amount", "total_amount"]:
                worksheet.set_column(col, col, 15)  # Medium for money amounts
            else:
                worksheet.set_column(col, col, 18)  # Default width

        # Write data
        for row, order in enumerate(data, start=1):
            for col, field in enumerate(fields):
                value = order.get(field, "")

                # Skip None values
                if value is None:
                    worksheet.write(row, col, "", cell_format)
                    continue

                # Handle datetime objects
                if field == "created_at" and value:
                    worksheet.write_datetime(row, col, value, date_format)

                # Handle money fields
                elif field in ["amount", "discount_amount", "vat_amount", "total_amount"]:
                    worksheet.write_number(row, col, value, money_format)

                # Handle tax rate as percentage
                elif field == "tax_rate":
                    worksheet.write_number(row, col, value, percent_format)

                # Handle status with color coding
                elif field == "status":
                    if value.lower() == "active":
                        worksheet.write(row, col, value.upper(), status_format_active)
                    elif value.lower() == "pending":
                        worksheet.write(row, col, value.upper(), status_format_pending)
                    else:
                        worksheet.write(row, col, value, cell_format)

                # Handle other values
                else:
                    worksheet.write(row, col, value, cell_format)

        # Add a summary section
        summary_row = len(data) + 3
        worksheet.write(summary_row, 0, "Order Summary:", header_format)
        worksheet.merge_range(summary_row, 0, summary_row, 1, "Order Summary:", header_format)

        # Total orders
        worksheet.write(summary_row + 1, 0, "Total Orders:", cell_format)
        worksheet.write(summary_row + 1, 1, len(data), cell_format)

        # Status count
        status_counts = {}
        for order in data:
            status = order.get("status", "").lower()
            status_counts[status] = status_counts.get(status, 0) + 1

        row_offset = 2
        for status, count in status_counts.items():
            worksheet.write(summary_row + row_offset, 0, f"{status.title()} Orders:", cell_format)
            worksheet.write(summary_row + row_offset, 1, count, cell_format)
            worksheet.write(summary_row + row_offset, 2, f"{count/len(data):.1%}", percent_format)
            row_offset += 1

        # Financial summary
        finance_row = summary_row + row_offset + 1
        worksheet.write(finance_row, 0, "Financial Summary:", header_format)
        worksheet.merge_range(finance_row, 0, finance_row, 1, "Financial Summary:", header_format)

        # Calculate totals
        total_amount_sum = sum(order.get("amount", 0) for order in data)
        total_discount_sum = sum(order.get("discount_amount", 0) for order in data)
        total_vat_sum = sum(order.get("vat_amount", 0) for order in data)
        total_final_sum = sum(order.get("total_amount", 0) for order in data)

        worksheet.write(finance_row + 1, 0, "Total Order Amount:", cell_format)
        worksheet.write(finance_row + 1, 1, total_amount_sum, money_format)

        worksheet.write(finance_row + 2, 0, "Total Discounts:", cell_format)
        worksheet.write(finance_row + 2, 1, total_discount_sum, money_format)

        worksheet.write(finance_row + 3, 0, "Total VAT:", cell_format)
        worksheet.write(finance_row + 3, 1, total_vat_sum, money_format)

        worksheet.write(finance_row + 4, 0, "Total Revenue:", cell_format)
        worksheet.write(finance_row + 4, 1, total_final_sum, money_format)

        # Average order value
        avg_order_value = total_final_sum / len(data) if data else 0
        worksheet.write(finance_row + 6, 0, "Average Order Value:", cell_format)
        worksheet.write(finance_row + 6, 1, avg_order_value, money_format)

        # Close workbook and return response
        workbook.close()
        buffer.seek(0)

        return Response(
            buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
            background=BackgroundTasks(buffer.close()),
        )


order_crud = OrdersCRUD(database_engine=app_engine, collection="orders")
order_services = OrderServices(service_name="orders", crud=order_crud)
