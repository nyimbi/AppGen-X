from DBML4Visitor import DBML4Visitor

class FlaskAppBuilderGenerator(DBML4Visitor):
    def __init__(self):
        self.table_name = None
        self.columns = []

    def visitTable(self, ctx):
        self.table_name = ctx.ID().getText()

        if ctx.mixin():
            for mixin_ctx in ctx.mixin():
                mixin_name = mixin_ctx.ID().getText()
                self.columns.extend(self.visit(mixin_ctx))

        class_def = f"class {self.table_name}(Base):"
        class_def += "\n\t__tablename__ = '{}'\n".format(self.table_name)
        class_def += "\tid = Column(Integer, primary_key=True, autoincrement=True)\n"

        for column in self.columns:
            class_def += f"\t{column}\n"

        return class_def

    def visitMixin(self, ctx):
        return [self.visit(column_ctx) for column_ctx in ctx.column()]

    def visitColumn(self, ctx):
        name = ctx.ID().getText()
        col_type = self.visit(ctx.type_)
        options = [self.visit(o) for o in ctx.property()]

        if "pk" in options:
            col_type = "IntegerField(primary_key=True)"
            options.remove("pk")
        elif "?" in col_type:
            col_type = col_type.replace("?", "")
            options.append("nullable=True")

        sqla_type = f"{col_type[0].upper()}{col_type[1:]}"
        definition = f"Column({sqla_type}{', '.join(options)}, unique=False, nullable=False)"

        return f"{name} = {definition}"

    def visitProperty(self, ctx):
        if ctx.getText() == "pk":
            return ""
        elif ctx.getText() == "default":
            return f"default={self.visit(ctx.STRING())}"
        elif ctx.getText() == "required":
            return ""
        elif ctx.getText() == "note":
            return f"comment='{self.visit(ctx.STRING())[1:-1]}'"
        elif ctx.ref():
            target_table = ctx.ref().ID(0).getText()
            target_col = ".".join(ref_ctx.ID().getText() for ref_ctx in ctx.ref().ID()[1:])
            return f"ForeignKey('{target_table}.{target_col}')"
        elif ctx.display():
            display_option = self.visit(ctx.display())
            if display_option.startswith("widget"):
                return f""
            elif display_option.startswith("hide"):
                return f""
            elif display_option.startswith("hint"):
                return f""
            elif display_option.startswith("display"):
                return f"info='{display_option.split('=')[1]}'"
            elif display_option.startswith("tab"):
                return f""
            elif display_option.startswith("sequence"):
                return f"order={display_option.split('=')[1]}"
        elif ctx.min():
            return f""
        elif ctx.max():
            return f""
        else:
            return ""

    def generate_flask_appbuilder_models(self, tree):
        models = ""
        for statement_context in tree.statement():
            if statement_context.table():
                models += self.visit(statement_context.table()) + "\n\n"
        return models