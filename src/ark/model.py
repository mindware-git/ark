from .entity import Entity
from .solver import SimpleSolver


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

    def compile(self):
        """
        Run solver to resolve dependencies and then lower to OpenSCAD.
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

        for ent in self.entities.values():
            # clamp None -> 0
            z_val = ent.z if ent.z is not None else 0
            scad_lines.append(
                f"translate([{ent.x}, {ent.y}, {z_val}]) cube([{ent.width}, {ent.depth}, {ent.height}]);"
            )

        result.openscad = "\n".join(scad_lines)

        return result
