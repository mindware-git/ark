from .entity import Entity
from .solver import SimpleSolver

# simple semantic-to-color default for visualization purposes
DEFAULT_COLOR = [0.5, 0.5, 0.5]
# note: semantic color map is no longer hard-coded here; callers may
# provide their own map when calling compile().  We keep DEFAULT_COLOR
# as fallback for any unmapped semantics.


class CompileResult:
    """
    Minimal compile result object for V0.
    Includes deterministic solver errors.
    """

    def __init__(self, success: bool, openscad: str = ""):
        self.success = success
        self.openscad = openscad
        self.errors = []
        self.warnings = []

    def add_error(self, message: str):
        self.errors.append(message)
        self.success = False

    def add_warning(self, message: str):
        self.warnings.append(message)


class Model:
    """
    Core internal representation (IR) of ark with minimal solver.
    Supports Entity management, top_of dependency, and deterministic compile.
    """

    def __init__(self, name: str):
        self.name = name
        self.entities = {}  # id -> Entity
        self.dependencies = []  # list of {'type':'top_of', 'child':id, 'parent':id}

    def add_cube(
        self,
        id: str,
        width: float,
        depth: float,
        height: float,
        x: float = 0,
        y: float = 0,
        z: float = 0,
        semantic: str = None,
    ):
        if id in self.entities:
            raise ValueError(f"Duplicate entity id '{id}'")
        ent = Entity(id, width, depth, height, x, y, z, semantic)
        self.entities[id] = ent
        return ent

    def add_top_of(self, child_id: str, parent_id: str):
        if child_id not in self.entities or parent_id not in self.entities:
            raise ValueError(
                f"Both child '{child_id}' and parent '{parent_id}' must exist in the model"
            )
        self.dependencies.append(
            {"type": "top_of", "child": child_id, "parent": parent_id}
        )

    def add_align_x(self, child_id: str, parent_id: str):
        if child_id not in self.entities or parent_id not in self.entities:
            raise ValueError(
                f"Both child '{child_id}' and parent '{parent_id}' must exist in the model"
            )
        self.dependencies.append(
            {"type": "align_x", "child": child_id, "parent": parent_id}
        )

    def add_align_y(self, child_id: str, parent_id: str):
        if child_id not in self.entities or parent_id not in self.entities:
            raise ValueError(
                f"Both child '{child_id}' and parent '{parent_id}' must exist in the model"
            )
        self.dependencies.append(
            {"type": "align_y", "child": child_id, "parent": parent_id}
        )

    def add_right_of(self, right_id: str, left_id: str):
        if right_id not in self.entities or left_id not in self.entities:
            raise ValueError(
                f"Both right '{right_id}' and left '{left_id}' must exist in the model"
            )
        self.dependencies.append(
            {"type": "right_of", "child": right_id, "parent": left_id}
        )

    def compile(self, semantic_color_map: dict | None = None):
        """
        Run solver to resolve dependencies and then lower to OpenSCAD.

        :param semantic_color_map: optional mapping from semantic string to
            [r,g,b] colour.  If not provided, we only use DEFAULT_COLOR for
            all semantics (no named variables will be emitted).
        """
        result = CompileResult(success=True)

        # Run minimal deterministic solver
        solver = SimpleSolver(self)
        solver.resolve()
        if solver.errors:
            result.success = False
            result.errors.extend(solver.errors)

        # Lower to OpenSCAD
        scad_lines = [
            f"// ark generated file",
            f"// model: {self.name}",
        ]

        # declare color variables for any semantics we have in the model
        semantics = {ent.semantic for ent in self.entities.values() if ent.semantic}
        color_vars = {}
        if semantic_color_map:
            for sem in sorted(semantics):
                var_name = f"{sem.replace(' ', '_')}_color"
                color = semantic_color_map.get(sem, DEFAULT_COLOR)
                scad_lines.append(f"{var_name} = [{color[0]}, {color[1]}, {color[2]}];")
                color_vars[sem] = var_name
            if semantics:
                scad_lines.append("")  # blank line after declarations

        for ent in self.entities.values():
            if ent.semantic:
                scad_lines.append(f"// semantic: {ent.semantic}")
            # clamp None -> 0
            z_val = ent.z if ent.z is not None else 0
            cube_stmt = f"translate([{ent.x}, {ent.y}, {z_val}]) cube([{ent.width}, {ent.depth}, {ent.height}]);"
            if ent.semantic and ent.semantic in color_vars:
                cube_stmt = f"color({color_vars[ent.semantic]}) {cube_stmt}"
            scad_lines.append(cube_stmt)

        result.openscad = "\n".join(scad_lines)

        return result
