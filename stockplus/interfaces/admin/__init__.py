# Import the AppConfig to ensure it's loaded
default_app_config = 'stockplus.interfaces.admin.apps.AdminInterfaceConfig'

# This file is intentionally left empty to avoid circular imports
# The actual admin registrations will be done in the ready() method of the AppConfig
