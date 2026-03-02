"""Example script that reads a natural language prompt and constructs an
ARK model based on what the existing API supports.

This is intentionally naive/imperative – the goal is to expose the gaps in
ARK's current capabilities when you try to implement the kitchen description.

Run this file to see the OpenSCAD output that the simple solver generates.
"""

import ark as ak

# define our own semantic color map locally (not inside ark.model)
DEFAULT_COLOR = [0.5, 0.5, 0.5]
SEMANTIC_COLOR_MAP = {
    "Wall": [0.85, 0.85, 0.85],
    "Storage": [0.7, 0.5, 0.3],
    "Appliance": [0.2, 0.2, 0.2],
    "Water": [0.3, 0.6, 1.0],
}

PROMPT = """
Design a realistic kitchen interior suitable for a family apartment.

The kitchen should be rectangular, approximately 3.5m wide and 2.8m deep.

Wall Layout:
- The back wall (3.5m) will be the primary cabinet wall.
- The right wall (2.8m) should include a tall storage unit and refrigerator.
- Leave the left side open for dining access.

Base Cabinet Layout (Back Wall):
- Install continuous base cabinets along the full 3.5m back wall.
- Standard depth: 600mm.
- Height: 900mm including countertop.
- Place the sink slightly off-center toward the window (assume window above sink).
- Dishwasher should be placed directly to the right of the sink.
- Drawer units should be located near the cooking area.

Cooking Area:
- Install a built-in cooktop centered along the back wall.
- Oven directly below the cooktop.
- Range hood aligned above the cooktop.
- Maintain at least 400mm workspace on both sides of the cooktop.

Upper Cabinets:
- Install upper cabinets above base cabinets except above the window.
- Leave a 600mm vertical gap between countertop and upper cabinets.
- Above the cooktop, install a range hood cabinet instead of a standard cabinet.

Right Wall (Tall Units):
- Install a full-height pantry cabinet (2400mm high).
- Refrigerator placed next to pantry.
- Maintain clean alignment with base cabinet depth.

Lighting:
- Add under-cabinet LED strip lighting.
- Ceiling should include recessed lights.

Style:
- Modern, minimal, neutral tones.
- Light wood lower cabinets, matte white upper cabinets.
- White quartz countertop.

Functional Constraints:
- Maintain clear walking space of at least 900mm.
- Ensure ergonomic countertop height (900mm).
- Avoid overlapping or unrealistic placements.
"""


def build_model_from_prompt(prompt: str) -> ak.Model:
    # this implementation is completely manual and ignores most of the
    # instructions in the prompt because the current ARK API is extremely
    # limited.  it simply demonstrates the pieces we *can* create with
    # cubes and a couple of dependency types.

    model = ak.Model("kitchen_from_prompt")

    # map our informal area labels to the colors defined in the core library
    mapping = {
        "sink_area": "Water",
        "dishwasher": "Appliance",
        "cooktop_area": "Appliance",
        "work_space": "Wall",
        "oven": "Appliance",
        "range_hood": "Appliance",
        "pantry": "Storage",
        "refrigerator": "Appliance",
        "upper_cabinet": "Storage",
        # anything else defaults to Wall
    }

    # base cabinets (one long block, then subdivided for semantics)
    base_depth = 0.6  # metres
    base_height = 0.9

    # break the back wall into a few chunks so we can tag semantics later.
    # note: ARK doesn't know about "window" so we just leave a semantic gap.
    sink_width = 0.9
    dishwasher_width = 0.6
    cooktop_width = 0.8
    remaining = 3.5 - (sink_width + dishwasher_width + cooktop_width + 0.4)
    # put an empty segment for the workspace to the right of cooktop

    def sem(key: str) -> str:
        # translate our ad-hoc semantics into one of the canonical keys
        return mapping.get(key, "Wall")

    model.add_cube(
        "base_left",
        width=sink_width,
        depth=base_depth,
        height=base_height,
        x=0,
        y=0,
        semantic=sem("sink_area"),
    )
    model.add_cube(
        "dishwasher",
        width=dishwasher_width,
        depth=base_depth,
        height=base_height,
        x=sink_width,
        y=0,
        semantic=sem("dishwasher"),
    )
    model.add_cube(
        "cooktop",
        width=cooktop_width,
        depth=base_depth,
        height=base_height,
        x=sink_width + dishwasher_width + 0.2,
        y=0,
        semantic=sem("cooktop_area"),
    )
    model.add_cube(
        "workspace",
        width=remaining,
        depth=base_depth,
        height=base_height,
        x=sink_width + dishwasher_width + cooktop_width + 0.2,
        y=0,
        semantic=sem("work_space"),
    )

    # oven under cooktop using top_of dependency
    oven = model.add_cube(
        "oven",
        width=cooktop_width,
        depth=base_depth,
        height=0.7,
        x=model.entities["cooktop"].x,
        y=0,
        semantic=sem("oven"),
    )
    model.add_top_of("oven", "cooktop")

    # range hood above cooktop
    hood = model.add_cube(
        "range_hood",
        width=cooktop_width,
        depth=0.3,
        height=0.5,
        x=model.entities["cooktop"].x,
        y=0,
        z=base_height,
        semantic=sem("range_hood"),
    )
    model.add_top_of("range_hood", "cooktop")

    # tall units on right wall
    pantry = model.add_cube(
        "pantry",
        width=0.6,
        depth=base_depth,
        height=2.4,
        x=3.5 - 0.6,
        y=0,
        semantic=sem("pantry"),
    )
    fridge = model.add_cube(
        "fridge",
        width=0.7,
        depth=base_depth,
        height=1.8,
        x=3.5 - 0.6 - 0.7,
        y=0,
        semantic=sem("refrigerator"),
    )
    # align the tall units with the base cabinets' y-coordinate
    model.add_align_y("pantry", "base_left")
    model.add_align_y("fridge", "base_left")

    # upper cabinets – ARK currently has no notion of hanging cabinets or
    # vertical gaps, so we just create a second layer of cubes above the base
    upper_height = 0.8
    upper_gap = 0.6
    model.add_cube(
        "upper_left",
        width=sink_width,
        depth=base_depth,
        height=upper_height,
        x=0,
        y=0,
        z=base_height + upper_gap,
        semantic=sem("upper_cabinet"),
    )
    # skipping over the "window" area since we can't create a cutout
    model.add_cube(
        "upper_cooktop",
        width=cooktop_width,
        depth=base_depth,
        height=upper_height,
        x=model.entities["cooktop"].x,
        y=0,
        z=base_height + upper_gap,
        semantic=sem("upper_cabinet"),
    )

    # lighting and style are completely visual and cannot be expressed in
    # geometry; we would encode them as semantic tags only.
    for eid in model.entities:
        model.entities[eid].semantic = model.entities[eid].semantic or ""

    return model


if __name__ == "__main__":
    # build and compile the model
    model = build_model_from_prompt(PROMPT)
    # ensure the model name uses the try_ prefix
    model.name = "try_" + model.name
    result = model.compile(semantic_color_map=SEMANTIC_COLOR_MAP)

    # print to stdout and save to a .scad file so we can inspect it later
    print(result.openscad)
    out_path = f"examples/{model.name}.scad"
    with open(out_path, "w") as f:
        f.write(result.openscad)
    print(f"SCAD output written to {out_path}")

    if not result.success:
        print("compile errors:\n", "\n".join(result.errors))
    else:
        print("Compilation succeeded with", len(model.entities), "entities.")
