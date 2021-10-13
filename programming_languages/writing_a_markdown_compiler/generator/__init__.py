from .visitor import BodyVisitor


class Generator:
    body_generator = BodyVisitor()

    def generate(self, ast):
        return self.body_generator.visit(ast)
