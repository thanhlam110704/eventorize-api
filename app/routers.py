from auth import routers as auth_routers
from fastapi import APIRouter
from modules.v1.agendas import routers as agendas_routers
from modules.v1.attendees import routers as attendees_routers
from modules.v1.dashboard import routers as dashboard_routers
from modules.v1.events import routers as events_routers
from modules.v1.health import routers as health_routers
from modules.v1.location import routers as location_routers
from modules.v1.orders import routers as orders_routers
from modules.v1.organizers import routers as organizers_routers
from modules.v1.payments import routers as payments_routers
from modules.v1.permissions import routers as permissions_routers
from modules.v1.roles import routers as roles_routers
from modules.v1.tasks import routers as tasks_routers
from modules.v1.tickets import routers as tickets_routers
from modules.v1.favorites import routers as favorites_routers
from users import routers as users_routers

api_routers = APIRouter()

# Healthy check
api_routers.include_router(health_routers.router)

# Users
api_routers.include_router(users_routers.router)

# Modules
api_routers.include_router(tasks_routers.router)
api_routers.include_router(permissions_routers.router)
api_routers.include_router(roles_routers.router)

# Organizers
api_routers.include_router(organizers_routers.router)

# Agendas
api_routers.include_router(agendas_routers.router)

# Events
api_routers.include_router(events_routers.router)

# Tickets
api_routers.include_router(tickets_routers.router)

# Attendees
api_routers.include_router(attendees_routers.router)

# Orders
api_routers.include_router(orders_routers.router)

# Location
api_routers.include_router(location_routers.router)

# Payments
api_routers.include_router(payments_routers.router)

# Auth
api_routers.include_router(auth_routers.router)

# Dashboard
api_routers.include_router(dashboard_routers.router)

# Favorites
api_routers.include_router(favorites_routers.router)

