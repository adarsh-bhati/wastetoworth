def calculate_metrics(materials):

    total_items = len(materials)

    waste_reused = total_items

    co2_saved = round(
        total_items * 0.15,
        2
    )

    landfill_reduction = round(
        total_items * 0.30,
        2
    )

    return {

        "waste_reused": f"{waste_reused} Items",

        "co2_saved": co2_saved,

        "landfill_reduction": landfill_reduction

    }