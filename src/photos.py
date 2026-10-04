# Header photos for inner pages, keyed by page path.
# Each value is (Unsplash photo id, what the photo shows). All are free-licence Unsplash photos,
# loaded by link. They are placeholders until Southern Design supplies its own.
# Manufacturer pages deliberately have no photo: a stock pump would look like that brand's product.
PHOTO = {
    # problem guides
    "problems/mechanical-seal-keeps-failing/": ("1769147339214-076740872485", "Machined metal parts resting on engineering drawings"),
    "problems/pump-cavitation/": ("1664087783968-0cd7deee8390", "Blue process pipework, valves and vessels in a plant"),
    "problems/pump-running-off-curve/": ("1744302570296-d4bcb55b7002", "Pressure gauges and valves on pipework"),
    "problems/pump-bearing-failure/": ("1643933871541-090062935680", "Tapered roller bearing"),
    "problems/calculate-pump-mtbf/": ("1738918937796-743064feefa1", "Control room panel with rows of gauges and indicators"),
    "problems/water-hammer-pulsation/": ("1538474705339-e87de81450e8", "Runs of flanged industrial pipe"),
    "problems/mag-drive-pump-failure/": ("1513828583688-c52646db42da", "Motor-driven equipment among stainless steel process pipework"),
    "problems/repair-or-replace-pump/": ("1723022208597-a641bdadf60c", "Old machine with worn, rusted gears"),
    "problems/pump-reliability-program/": ("1738918937796-743064feefa1", "Control room panel with rows of gauges and indicators"),
    # services
    "services/pump-repair/": ("1776090188130-26c7253ff423", "Lathe in a machine shop"),
    "services/mechanical-seal-repair/": ("1745449064670-94bd0fc13df8", "Workshop tools laid out on a bench"),
    "services/field-service/": ("1595856898575-9d187bd32fd6", "Technician in protective gear working from a tool case on site"),
    "services/hydraulic-system-analysis/": ("1581092160562-40aa08e78837", "Engineer marking up technical drawings at a desk"),
    "services/reliability-management/": ("1509390288171-ce2088f7d08e", "Industrial plant lit at night"),
    "services/lubrication-training-audits/": ("1524514587686-e2909d726e9b", "Close-up of machine gears"),
    # industries
    "industries/chemical/": ("1601045774958-305ae15032c8", "Chemical plant seen across water"),
    "industries/pulp-paper/": ("1727517786578-ff2bb896b852", "Workers at a large paper machine"),
    "industries/water-wastewater/": ("1622322977879-af6982dcba00", "Aerial view of circular tanks at a water treatment plant"),
    "industries/power-generation/": ("1630142896875-d71a6ee6db03", "Cooling towers at a power station"),
    "industries/pharmaceutical/": ("1621954938124-02e637ba3584", "Stainless steel equipment in a clean production hall"),
    "industries/steel/": ("1624027492684-327af1fb7559", "Interior of a steel mill"),
    "industries/bio-energy/": ("1673208769691-e74104d853fd", "Aerial view of digester tanks at a biogas plant"),
    # locations
    "locations/arkansas/": ("1605027628030-9bb6f83535e6", "Sunset over wooded hills"),
    "locations/maryland-dc-delaware/": ("1611316491868-a683302aa917", "Baltimore Inner Harbor skyline at dusk"),
    "locations/virginia-carolinas/": ("1648571990036-782b88dd6a1a", "City skyline and bridge over a river"),
    # product categories
    "products/pumps/": ("1720670996646-2f5d69a10ee7", "Large industrial pumps installed in a plant room"),
    "products/mechanical-seals/": ("1769147339214-076740872485", "Machined metal parts resting on engineering drawings"),
    "products/valves/": ("1607472586893-edb57bdc0e39", "Pipework with valves against a brick wall"),
    "products/motors-drives/": ("1655874837055-7adc909ae602", "Electric motor on a vertical pump"),
    "products/reliability-accessories/": ("1643933871541-090062935680", "Tapered roller bearing"),
}


def photo_url(pid, w):
    return f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w={w}&q=70"
