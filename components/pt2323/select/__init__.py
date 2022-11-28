from esphome.components import select
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import CONF_OPTIONS
from .. import pt2323_ns, CONF_PT2323_ID, PT2323

DEPENDENCIES = ['pt2323']


PT2323Select = pt2323_ns.class_("PT2323Select", select.Select, cg.Component)


def ensure_option_map(value):
    cv.check_not_templatable(value)
    option = cv.All(cv.int_range(0, 2**8 - 1))
    mapping = cv.All(cv.string_strict)
    options_map_schema = cv.Schema({option: mapping})
    value = options_map_schema(value)

    all_values = list(value.keys())
    unique_values = set(value.keys())
    if len(all_values) != len(unique_values):
        raise cv.Invalid("Mapping values must be unique.")

    return value


CONFIG_SCHEMA = select.SELECT_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(PT2323Select),
        cv.GenerateID(CONF_PT2323_ID): cv.use_id(PT2323),
        cv.Required(CONF_OPTIONS): ensure_option_map,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    options_map = config[CONF_OPTIONS]
    var = await select.new_select(config, options=list(options_map.values()))
    await cg.register_component(var, config)
    cg.add(var.set_select_mappings(list(options_map.keys())))
    parent = await cg.get_variable(config[CONF_PT2323_ID])
    cg.add(var.set_parent(parent))