# Copyright 2025 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from openupgradelib import openupgrade, openupgrade_180

_logger = logging.getLogger(__name__)


def _table_exists(env, table_name: str) -> bool:
    """Return True if a table exists in the current schema."""
    # Works on Postgres: returns True if the regclass exists, else False
    env.cr.execute("SELECT to_regclass(%s) IS NOT NULL", (table_name,))
    return bool(env.cr.fetchone()[0])


@openupgrade.migrate()
def migrate(env, version):
    # En instalaciones limpias de Odoo 18 la tabla ir_property ya no existe.
    # Si no está, no hay nada que convertir y el script debe salir sin fallar.
    if not _table_exists(env, "ir_property"):
        _logger.info(
            "Skipping convert_company_dependent: table 'ir_property' not found "
            "(clean 18.0 database)."
        )
        return

    # Bases actualizadas (p.ej. 17 -> 18) sí tendrán ir_property y necesitan la conversión
    openupgrade_180.convert_company_dependent(
        env, "res.partner", "supplier_payment_mode_id"
    )
    openupgrade_180.convert_company_dependent(
        env, "res.partner", "customer_payment_mode_id"
    )
