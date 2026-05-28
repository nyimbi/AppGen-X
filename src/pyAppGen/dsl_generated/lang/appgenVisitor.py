# Generated from lang/appgen.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
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


    # Visit a parse tree produced by appgenParser#tableDirective.
    def visitTableDirective(self, ctx:appgenParser.TableDirectiveContext):
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


    # Visit a parse tree produced by appgenParser#flowItem.
    def visitFlowItem(self, ctx:appgenParser.FlowItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#flowStep.
    def visitFlowStep(self, ctx:appgenParser.FlowStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#flowDirective.
    def visitFlowDirective(self, ctx:appgenParser.FlowDirectiveContext):
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


    # Visit a parse tree produced by appgenParser#agentItem.
    def visitAgentItem(self, ctx:appgenParser.AgentItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#pbcDecl.
    def visitPbcDecl(self, ctx:appgenParser.PbcDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#pbcItem.
    def visitPbcItem(self, ctx:appgenParser.PbcItemContext):
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


    # Visit a parse tree produced by appgenParser#deploymentItem.
    def visitDeploymentItem(self, ctx:appgenParser.DeploymentItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#deployUnit.
    def visitDeployUnit(self, ctx:appgenParser.DeployUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#deployScale.
    def visitDeployScale(self, ctx:appgenParser.DeployScaleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#deployHealth.
    def visitDeployHealth(self, ctx:appgenParser.DeployHealthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#deployCheck.
    def visitDeployCheck(self, ctx:appgenParser.DeployCheckContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#deployResource.
    def visitDeployResource(self, ctx:appgenParser.DeployResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#deployBinding.
    def visitDeployBinding(self, ctx:appgenParser.DeployBindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#deployDirective.
    def visitDeployDirective(self, ctx:appgenParser.DeployDirectiveContext):
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


    # Visit a parse tree produced by appgenParser#apiDecl.
    def visitApiDecl(self, ctx:appgenParser.ApiDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#eventDecl.
    def visitEventDecl(self, ctx:appgenParser.EventDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#jobDecl.
    def visitJobDecl(self, ctx:appgenParser.JobDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#reportDecl.
    def visitReportDecl(self, ctx:appgenParser.ReportDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#menuDecl.
    def visitMenuDecl(self, ctx:appgenParser.MenuDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#componentDecl.
    def visitComponentDecl(self, ctx:appgenParser.ComponentDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#packageDecl.
    def visitPackageDecl(self, ctx:appgenParser.PackageDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#testDecl.
    def visitTestDecl(self, ctx:appgenParser.TestDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#contractItem.
    def visitContractItem(self, ctx:appgenParser.ContractItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#handlerDecl.
    def visitHandlerDecl(self, ctx:appgenParser.HandlerDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#contractArrow.
    def visitContractArrow(self, ctx:appgenParser.ContractArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#contractDirective.
    def visitContractDirective(self, ctx:appgenParser.ContractDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#agenticOption.
    def visitAgenticOption(self, ctx:appgenParser.AgenticOptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#agenticValue.
    def visitAgenticValue(self, ctx:appgenParser.AgenticValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#valueAtom.
    def visitValueAtom(self, ctx:appgenParser.ValueAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleItem.
    def visitRuleItem(self, ctx:appgenParser.RuleItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleExpression.
    def visitRuleExpression(self, ctx:appgenParser.RuleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleOr.
    def visitRuleOr(self, ctx:appgenParser.RuleOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleAnd.
    def visitRuleAnd(self, ctx:appgenParser.RuleAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleUnary.
    def visitRuleUnary(self, ctx:appgenParser.RuleUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#rulePredicate.
    def visitRulePredicate(self, ctx:appgenParser.RulePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleValueList.
    def visitRuleValueList(self, ctx:appgenParser.RuleValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleTerm.
    def visitRuleTerm(self, ctx:appgenParser.RuleTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#directiveValue.
    def visitDirectiveValue(self, ctx:appgenParser.DirectiveValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#ruleOperator.
    def visitRuleOperator(self, ctx:appgenParser.RuleOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#literal.
    def visitLiteral(self, ctx:appgenParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by appgenParser#qualifiedName.
    def visitQualifiedName(self, ctx:appgenParser.QualifiedNameContext):
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