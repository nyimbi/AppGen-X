# Generated from lang/appgen.g4 by ANTLR 4.13.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .appgenParser import appgenParser
else:
    from appgenParser import appgenParser

# This class defines a complete listener for a parse tree produced by appgenParser.
class appgenListener(ParseTreeListener):

    # Enter a parse tree produced by appgenParser#schema.
    def enterSchema(self, ctx:appgenParser.SchemaContext):
        pass

    # Exit a parse tree produced by appgenParser#schema.
    def exitSchema(self, ctx:appgenParser.SchemaContext):
        pass


    # Enter a parse tree produced by appgenParser#appDecl.
    def enterAppDecl(self, ctx:appgenParser.AppDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#appDecl.
    def exitAppDecl(self, ctx:appgenParser.AppDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#appBlock.
    def enterAppBlock(self, ctx:appgenParser.AppBlockContext):
        pass

    # Exit a parse tree produced by appgenParser#appBlock.
    def exitAppBlock(self, ctx:appgenParser.AppBlockContext):
        pass


    # Enter a parse tree produced by appgenParser#appOption.
    def enterAppOption(self, ctx:appgenParser.AppOptionContext):
        pass

    # Exit a parse tree produced by appgenParser#appOption.
    def exitAppOption(self, ctx:appgenParser.AppOptionContext):
        pass


    # Enter a parse tree produced by appgenParser#element.
    def enterElement(self, ctx:appgenParser.ElementContext):
        pass

    # Exit a parse tree produced by appgenParser#element.
    def exitElement(self, ctx:appgenParser.ElementContext):
        pass


    # Enter a parse tree produced by appgenParser#tableDecl.
    def enterTableDecl(self, ctx:appgenParser.TableDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#tableDecl.
    def exitTableDecl(self, ctx:appgenParser.TableDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#tableBody.
    def enterTableBody(self, ctx:appgenParser.TableBodyContext):
        pass

    # Exit a parse tree produced by appgenParser#tableBody.
    def exitTableBody(self, ctx:appgenParser.TableBodyContext):
        pass


    # Enter a parse tree produced by appgenParser#tableItem.
    def enterTableItem(self, ctx:appgenParser.TableItemContext):
        pass

    # Exit a parse tree produced by appgenParser#tableItem.
    def exitTableItem(self, ctx:appgenParser.TableItemContext):
        pass


    # Enter a parse tree produced by appgenParser#fieldDecl.
    def enterFieldDecl(self, ctx:appgenParser.FieldDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#fieldDecl.
    def exitFieldDecl(self, ctx:appgenParser.FieldDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#spreadDecl.
    def enterSpreadDecl(self, ctx:appgenParser.SpreadDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#spreadDecl.
    def exitSpreadDecl(self, ctx:appgenParser.SpreadDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#groupDecl.
    def enterGroupDecl(self, ctx:appgenParser.GroupDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#groupDecl.
    def exitGroupDecl(self, ctx:appgenParser.GroupDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#derivedExpr.
    def enterDerivedExpr(self, ctx:appgenParser.DerivedExprContext):
        pass

    # Exit a parse tree produced by appgenParser#derivedExpr.
    def exitDerivedExpr(self, ctx:appgenParser.DerivedExprContext):
        pass


    # Enter a parse tree produced by appgenParser#typeRef.
    def enterTypeRef(self, ctx:appgenParser.TypeRefContext):
        pass

    # Exit a parse tree produced by appgenParser#typeRef.
    def exitTypeRef(self, ctx:appgenParser.TypeRefContext):
        pass


    # Enter a parse tree produced by appgenParser#modifier.
    def enterModifier(self, ctx:appgenParser.ModifierContext):
        pass

    # Exit a parse tree produced by appgenParser#modifier.
    def exitModifier(self, ctx:appgenParser.ModifierContext):
        pass


    # Enter a parse tree produced by appgenParser#relationDecl.
    def enterRelationDecl(self, ctx:appgenParser.RelationDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#relationDecl.
    def exitRelationDecl(self, ctx:appgenParser.RelationDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#relationCardinality.
    def enterRelationCardinality(self, ctx:appgenParser.RelationCardinalityContext):
        pass

    # Exit a parse tree produced by appgenParser#relationCardinality.
    def exitRelationCardinality(self, ctx:appgenParser.RelationCardinalityContext):
        pass


    # Enter a parse tree produced by appgenParser#target.
    def enterTarget(self, ctx:appgenParser.TargetContext):
        pass

    # Exit a parse tree produced by appgenParser#target.
    def exitTarget(self, ctx:appgenParser.TargetContext):
        pass


    # Enter a parse tree produced by appgenParser#enumDecl.
    def enterEnumDecl(self, ctx:appgenParser.EnumDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#enumDecl.
    def exitEnumDecl(self, ctx:appgenParser.EnumDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#viewDecl.
    def enterViewDecl(self, ctx:appgenParser.ViewDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#viewDecl.
    def exitViewDecl(self, ctx:appgenParser.ViewDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#viewItem.
    def enterViewItem(self, ctx:appgenParser.ViewItemContext):
        pass

    # Exit a parse tree produced by appgenParser#viewItem.
    def exitViewItem(self, ctx:appgenParser.ViewItemContext):
        pass


    # Enter a parse tree produced by appgenParser#componentPlacement.
    def enterComponentPlacement(self, ctx:appgenParser.ComponentPlacementContext):
        pass

    # Exit a parse tree produced by appgenParser#componentPlacement.
    def exitComponentPlacement(self, ctx:appgenParser.ComponentPlacementContext):
        pass


    # Enter a parse tree produced by appgenParser#flowDecl.
    def enterFlowDecl(self, ctx:appgenParser.FlowDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#flowDecl.
    def exitFlowDecl(self, ctx:appgenParser.FlowDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#flowStep.
    def enterFlowStep(self, ctx:appgenParser.FlowStepContext):
        pass

    # Exit a parse tree produced by appgenParser#flowStep.
    def exitFlowStep(self, ctx:appgenParser.FlowStepContext):
        pass


    # Enter a parse tree produced by appgenParser#roleDecl.
    def enterRoleDecl(self, ctx:appgenParser.RoleDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#roleDecl.
    def exitRoleDecl(self, ctx:appgenParser.RoleDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#permission.
    def enterPermission(self, ctx:appgenParser.PermissionContext):
        pass

    # Exit a parse tree produced by appgenParser#permission.
    def exitPermission(self, ctx:appgenParser.PermissionContext):
        pass


    # Enter a parse tree produced by appgenParser#ruleDecl.
    def enterRuleDecl(self, ctx:appgenParser.RuleDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#ruleDecl.
    def exitRuleDecl(self, ctx:appgenParser.RuleDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#llmDecl.
    def enterLlmDecl(self, ctx:appgenParser.LlmDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#llmDecl.
    def exitLlmDecl(self, ctx:appgenParser.LlmDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#agentDecl.
    def enterAgentDecl(self, ctx:appgenParser.AgentDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#agentDecl.
    def exitAgentDecl(self, ctx:appgenParser.AgentDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#pbcDecl.
    def enterPbcDecl(self, ctx:appgenParser.PbcDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#pbcDecl.
    def exitPbcDecl(self, ctx:appgenParser.PbcDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#compositionDecl.
    def enterCompositionDecl(self, ctx:appgenParser.CompositionDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#compositionDecl.
    def exitCompositionDecl(self, ctx:appgenParser.CompositionDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#compositionItem.
    def enterCompositionItem(self, ctx:appgenParser.CompositionItemContext):
        pass

    # Exit a parse tree produced by appgenParser#compositionItem.
    def exitCompositionItem(self, ctx:appgenParser.CompositionItemContext):
        pass


    # Enter a parse tree produced by appgenParser#auditDecl.
    def enterAuditDecl(self, ctx:appgenParser.AuditDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#auditDecl.
    def exitAuditDecl(self, ctx:appgenParser.AuditDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#deploymentDecl.
    def enterDeploymentDecl(self, ctx:appgenParser.DeploymentDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#deploymentDecl.
    def exitDeploymentDecl(self, ctx:appgenParser.DeploymentDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#versionDecl.
    def enterVersionDecl(self, ctx:appgenParser.VersionDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#versionDecl.
    def exitVersionDecl(self, ctx:appgenParser.VersionDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#operationDecl.
    def enterOperationDecl(self, ctx:appgenParser.OperationDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#operationDecl.
    def exitOperationDecl(self, ctx:appgenParser.OperationDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#operationItem.
    def enterOperationItem(self, ctx:appgenParser.OperationItemContext):
        pass

    # Exit a parse tree produced by appgenParser#operationItem.
    def exitOperationItem(self, ctx:appgenParser.OperationItemContext):
        pass


    # Enter a parse tree produced by appgenParser#securityDecl.
    def enterSecurityDecl(self, ctx:appgenParser.SecurityDeclContext):
        pass

    # Exit a parse tree produced by appgenParser#securityDecl.
    def exitSecurityDecl(self, ctx:appgenParser.SecurityDeclContext):
        pass


    # Enter a parse tree produced by appgenParser#securityItem.
    def enterSecurityItem(self, ctx:appgenParser.SecurityItemContext):
        pass

    # Exit a parse tree produced by appgenParser#securityItem.
    def exitSecurityItem(self, ctx:appgenParser.SecurityItemContext):
        pass


    # Enter a parse tree produced by appgenParser#agenticOption.
    def enterAgenticOption(self, ctx:appgenParser.AgenticOptionContext):
        pass

    # Exit a parse tree produced by appgenParser#agenticOption.
    def exitAgenticOption(self, ctx:appgenParser.AgenticOptionContext):
        pass


    # Enter a parse tree produced by appgenParser#agenticValue.
    def enterAgenticValue(self, ctx:appgenParser.AgenticValueContext):
        pass

    # Exit a parse tree produced by appgenParser#agenticValue.
    def exitAgenticValue(self, ctx:appgenParser.AgenticValueContext):
        pass


    # Enter a parse tree produced by appgenParser#ruleItem.
    def enterRuleItem(self, ctx:appgenParser.RuleItemContext):
        pass

    # Exit a parse tree produced by appgenParser#ruleItem.
    def exitRuleItem(self, ctx:appgenParser.RuleItemContext):
        pass


    # Enter a parse tree produced by appgenParser#ruleValue.
    def enterRuleValue(self, ctx:appgenParser.RuleValueContext):
        pass

    # Exit a parse tree produced by appgenParser#ruleValue.
    def exitRuleValue(self, ctx:appgenParser.RuleValueContext):
        pass


    # Enter a parse tree produced by appgenParser#ruleOperator.
    def enterRuleOperator(self, ctx:appgenParser.RuleOperatorContext):
        pass

    # Exit a parse tree produced by appgenParser#ruleOperator.
    def exitRuleOperator(self, ctx:appgenParser.RuleOperatorContext):
        pass


    # Enter a parse tree produced by appgenParser#literal.
    def enterLiteral(self, ctx:appgenParser.LiteralContext):
        pass

    # Exit a parse tree produced by appgenParser#literal.
    def exitLiteral(self, ctx:appgenParser.LiteralContext):
        pass


    # Enter a parse tree produced by appgenParser#expression.
    def enterExpression(self, ctx:appgenParser.ExpressionContext):
        pass

    # Exit a parse tree produced by appgenParser#expression.
    def exitExpression(self, ctx:appgenParser.ExpressionContext):
        pass


    # Enter a parse tree produced by appgenParser#expressionAtom.
    def enterExpressionAtom(self, ctx:appgenParser.ExpressionAtomContext):
        pass

    # Exit a parse tree produced by appgenParser#expressionAtom.
    def exitExpressionAtom(self, ctx:appgenParser.ExpressionAtomContext):
        pass


    # Enter a parse tree produced by appgenParser#operator.
    def enterOperator(self, ctx:appgenParser.OperatorContext):
        pass

    # Exit a parse tree produced by appgenParser#operator.
    def exitOperator(self, ctx:appgenParser.OperatorContext):
        pass



del appgenParser