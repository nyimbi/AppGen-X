# Generated from lang/appgen.g4 by ANTLR 4.13.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .appgenParser import appgenParser
else:
    from appgenParser import appgenParser

# This class defines a complete generic visitor for a parse tree produced by appgenParser.

class appgenVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by appgenParser#schema.
    def visitSchema(self, ctx:appgenParser.SchemaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#appDecl.
    def visitAppDecl(self, ctx:appgenParser.AppDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#appBlock.
    def visitAppBlock(self, ctx:appgenParser.AppBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#appOption.
    def visitAppOption(self, ctx:appgenParser.AppOptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#element.
    def visitElement(self, ctx:appgenParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#tableDecl.
    def visitTableDecl(self, ctx:appgenParser.TableDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#tableBody.
    def visitTableBody(self, ctx:appgenParser.TableBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#tableItem.
    def visitTableItem(self, ctx:appgenParser.TableItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#fieldDecl.
    def visitFieldDecl(self, ctx:appgenParser.FieldDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#spreadDecl.
    def visitSpreadDecl(self, ctx:appgenParser.SpreadDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#groupDecl.
    def visitGroupDecl(self, ctx:appgenParser.GroupDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#derivedExpr.
    def visitDerivedExpr(self, ctx:appgenParser.DerivedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#typeRef.
    def visitTypeRef(self, ctx:appgenParser.TypeRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#modifier.
    def visitModifier(self, ctx:appgenParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#relationDecl.
    def visitRelationDecl(self, ctx:appgenParser.RelationDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#relationCardinality.
    def visitRelationCardinality(self, ctx:appgenParser.RelationCardinalityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#target.
    def visitTarget(self, ctx:appgenParser.TargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#enumDecl.
    def visitEnumDecl(self, ctx:appgenParser.EnumDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#viewDecl.
    def visitViewDecl(self, ctx:appgenParser.ViewDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#viewItem.
    def visitViewItem(self, ctx:appgenParser.ViewItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#componentPlacement.
    def visitComponentPlacement(self, ctx:appgenParser.ComponentPlacementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#flowDecl.
    def visitFlowDecl(self, ctx:appgenParser.FlowDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#flowStep.
    def visitFlowStep(self, ctx:appgenParser.FlowStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#roleDecl.
    def visitRoleDecl(self, ctx:appgenParser.RoleDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#permission.
    def visitPermission(self, ctx:appgenParser.PermissionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleDecl.
    def visitRuleDecl(self, ctx:appgenParser.RuleDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#llmDecl.
    def visitLlmDecl(self, ctx:appgenParser.LlmDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#agentDecl.
    def visitAgentDecl(self, ctx:appgenParser.AgentDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#pbcDecl.
    def visitPbcDecl(self, ctx:appgenParser.PbcDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#compositionDecl.
    def visitCompositionDecl(self, ctx:appgenParser.CompositionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#compositionItem.
    def visitCompositionItem(self, ctx:appgenParser.CompositionItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#auditDecl.
    def visitAuditDecl(self, ctx:appgenParser.AuditDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#deploymentDecl.
    def visitDeploymentDecl(self, ctx:appgenParser.DeploymentDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#versionDecl.
    def visitVersionDecl(self, ctx:appgenParser.VersionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#operationDecl.
    def visitOperationDecl(self, ctx:appgenParser.OperationDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#operationItem.
    def visitOperationItem(self, ctx:appgenParser.OperationItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#securityDecl.
    def visitSecurityDecl(self, ctx:appgenParser.SecurityDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#securityItem.
    def visitSecurityItem(self, ctx:appgenParser.SecurityItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#agenticOption.
    def visitAgenticOption(self, ctx:appgenParser.AgenticOptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#agenticValue.
    def visitAgenticValue(self, ctx:appgenParser.AgenticValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleItem.
    def visitRuleItem(self, ctx:appgenParser.RuleItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleValue.
    def visitRuleValue(self, ctx:appgenParser.RuleValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleOperator.
    def visitRuleOperator(self, ctx:appgenParser.RuleOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#literal.
    def visitLiteral(self, ctx:appgenParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#expression.
    def visitExpression(self, ctx:appgenParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#expressionAtom.
    def visitExpressionAtom(self, ctx:appgenParser.ExpressionAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#operator.
    def visitOperator(self, ctx:appgenParser.OperatorContext):
        return self.visitChildren(ctx)



del appgenParser