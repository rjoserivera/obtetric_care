from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# Permitir compatibilidad con versiones locales de MariaDB (ej: XAMPP 10.4.x)
BaseDatabaseWrapper.check_database_version_supported = lambda self: None
DatabaseFeatures.can_return_columns_from_insert = False

