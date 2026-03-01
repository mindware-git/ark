class SimpleSolver:
    """
    Minimal deterministic solver for V0
    Supports:
        - top_of dependency: sets child.z = parent.z + parent.height
        - align_x, align_y optional
    """

    def __init__(self, model):
        self.model = model
        self.errors = []

    def resolve(self):
        # First, validate all entities
        for entity in self.model.entities.values():
            if entity.width < 0 or entity.depth < 0 or entity.height < 0:
                self.errors.append(
                    f"Constraint violation: Entity '{entity.id}' has negative dimensions."
                )

        # top_of resolution
        for dep in getattr(self.model, "dependencies", []):
            child = self.model.entities.get(dep["child"])
            parent = self.model.entities.get(dep["parent"])
            if not child or not parent:
                self.errors.append(f"Dependency unresolved: {dep}")
                continue
            if dep["type"] == "top_of":
                # The dependency solver should set the position
                child.z = parent.z + parent.height
