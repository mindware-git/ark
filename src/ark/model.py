class CompileResult:
    """
    Minimal compile result object for V0.

    Designed to evolve later into:
    - diagnostics (errors / warnings)
    - structured messages for LLM repair loops
    - multi-stage compilation metadata
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
    Core internal representation (IR) of ark.

    In V0:
        - Holds entities (currently none)
        - Can compile to minimal OpenSCAD output

    Future:
        - Dependency graph
        - Constraint graph
        - Hierarchy tree
        - Resolution engine
    """

    def __init__(self, name: str):
        self.name = name
        self.entities = []

    def add_cube(self, id: str, width: float, depth: float, height: float):
        from .entity import Entity

        self.entities.append(Entity(id, width=width, depth=depth, height=height))

    # ---- V0 Compile ----

    def compile(self):
        """
        Compile the model into OpenSCAD.

        V0 behavior:
            - Always succeeds
            - Emits minimal header
        """

        result = CompileResult(success=True)

        # Minimal OpenSCAD output
        scad_lines = [
            f"// ark generated file",
            f"// model: {self.name}",
        ]

        processed_ids = set()

        for entity in self.entities:
            if entity.id in processed_ids:
                result.add_error(f"Duplicate entity ID: {entity.id}")
                continue
            processed_ids.add(entity.id)

            if entity.width < 0 or entity.depth < 0 or entity.height < 0:
                result.add_error(f"Entity '{entity.id}' has negative dimensions.")
                continue

            scad_lines.append(
                f"cube([{entity.width}, {entity.depth}, {entity.height}]);"
            )

        # Set success to False if there are any errors
        if result.errors:
            result.success = False

        result.openscad = "\n".join(scad_lines)

        return result
