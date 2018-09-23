
# -*- coding: utf-8 -*-
"""
EECS 348, Winter 2018

Lab 3 :::: STUDENT_CODE.PY ::::
    
@author: Jeremy Midivdy, jam658

"""

import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """

        
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact
        return False

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule or False is there is no rule
        """
        
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule
        return False

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB

        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added

        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)

        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)

    def kb_assert(self, statement):
        """Assert a fact or rule into the KB

        Args:
            statement (Statement): Statement we're asserting in the format produced by read.py
        """
        printv("Asserting {!r}", 0, verbose, [statement])
        self.kb_add(Fact(statement) if factq(statement) else Rule(statement))

    def kb_ask(self, statement):
        """Ask if a fact is in the KB

        Args:
            statement (Statement) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        printv("Asking {!r}", 0, verbose, [statement])
        if factq(statement):
            f = Fact(statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else False

        else:
            print "Invalid ask:", statement
            return False

    def kb_retract(self, statement):
        """Retract a fact from the KB

        Args:
            statement (Statement) - Statement to be asked (will be converted into a Fact)

        Returns:
            None
        """
        
        ####################################################
        
        # ----------- KB RETRACT IMPLEMENTATION ---------- #
        
        ####################################################
        
        printv("Retracting {!r}", 0, verbose, [statement])
        
        # -------------  HELPER FUNCTIONS ---------------- #
        
        def deleteTerm(term):
            if isinstance(term, Fact):
                new_facts = []
                for row in self.facts:
                    if row != term:
                        new_facts.append(row)
                self.facts = new_facts
            else:
                new_rules = []
                for row in self.rules:
                    if row != term:
                        new_rules.append(row)
                self.rules = new_rules
            
        # ----------------- TOP LEVEL ------------------ #        
        
        #initiate the inputted statement and check to see that 
        #this statement is a given statement within the KB
        #if this statement is not a FACT in the KB, return
        
        #if statement is a rule, RETURN
        if isinstance(statement, Rule):
            return
        
        #if statement is a Statement object
        elif isinstance(statement, Statement):
            tempFact = Fact(statement)
            s = self._get_fact(tempFact)
            
        #if statement is a Fact
        elif isinstance(statement, Fact):
            s = self._get_fact(tempFact)
            
        #if statement is a list
        elif isinstance(statement, list):
            #if the inputted list has NO terms, do nothing
            if statement == []:
                return
            temp = Statement(statement)
            tempFact = Fact(temp)
            s = self._get_fact(tempFact)
        
        else:
            #input is not of the correct type [either a list --> statement --> fact]
            return
        
        #input is not in the KB, so return
        if s == False:
            return
        
        #ONLY asserted Facts can be retracted
        if s.asserted == False:
            return
        
        deleteTerm(s)  
        TOP_NODE = s
        
        # -------------- RECURSIVE CHECKER ------------------------ #
        # helper function that checks the rest of the KB
        # to see if any more facts should be deleted
        
        def retractTree(s):
            
            #initialize useful variables
            numSupportedBy = len(s.supported_by)
            numFactsSupports = len(s.supports_facts)
            numRulesSupports = len(s.supports_rules)
            
            # ----- CHECK TO SEE WHETHER CURRENT FACT/RULE SHOULD BE DELETED IN TREE ----- #
                                        
            #base case
            #if this fact/rule isn't supported by other FACTS/RULES
            #delete it
            if numSupportedBy == 0 and s.asserted == False and s != TOP_NODE:
                deleteTerm(s)
            
            #if this FACT is supported by other FACTS/RULES, check to see if any of the 
            #FACTS or RULES it is supported by are no longer in the KB
            #if all FACTS or RULES it is supported by are no longer in the KB, retract fact and return
            elif s!= TOP_NODE and s.asserted == False:
                bads = []
                for row in s.supported_by:
                    row_fact = row[0]
                    row_rule = row[1]
                    
                    if row_fact not in self.facts:
                        bads.append(row)
                    elif row_rule not in self.rules:
                        bads.append(row)
                
                #if all of the facts in supportedBy are BAD
                #remove this term from the KB
                #why does this work??
                if len(bads) == numSupportedBy:
                    deleteTerm(s)
                    
            # --------------- BUILD TREE --------------------------- #
            
            #recurse to build the tree from TOP to BOTTOM LEVEL
            #stop when at BOTTOM LEVEL: ergo, current depth
            #supports no facts or supports no rules (terminal)
            if numFactsSupports != 0:
                for row in s.supports_facts:
                    retractTree(row)
            if numRulesSupports != 0:
                for row in s.supports_rules:
                    retractTree(row)
              
            # ----- UPDATE SUPPORTS_FACTS AND SUPPORTS_RULES ----- #
            
            #initalize update lists
            new_supports_facts = []
            new_supports_rules = []
            
            #exclude facts and rules no longer in KB
            for row in s.supports_facts:
                if row in self.facts:
                    new_supports_facts.append(row)
            for row in s.supports_rules:
                if row in self.rules:
                    new_supports_rules.append(row)
            
            #update lists
            s.supports_facts = new_supports_facts
            s.supports_rules = new_supports_rules
            
            #end current recursion
            return
        
        #envoke recursive method to check the rest of the tree
        retractTree(s)
        retractTree(s)
        
 

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
      
        
        ####################################################
        
        # ------- FORWARD CHAINING IMPLEMENTATION -------- #
        
        ####################################################
        
        #get LHS and its first element
        LHS = rule.lhs
        first = LHS[0]
                
        #see if first and fact match with each other somewhere in the KB
        bindings = match(fact.statement, first)
        
        #if no bindings, return
        if not bindings:
            return
                
        #add either a FACT or a RULE to the kb
        if len(LHS) == 1:           
            
            # ---------------------- FACT --------------------------------- #
            
            #instanitate new facts accordingly to bindings
            c = instantiate(rule.rhs, bindings)  
            
            #create new fact and add it to KB
            #see if new inferred Fact is already in the KB
            newFact = Fact(c, [[fact, rule]])
            
            #if not in the KB, add to KB 
            if not kb._get_fact(newFact):
                kb.kb_add(newFact)
            else:
                #if fact is already in the KB - inferred previously
                #or supported by another Fact/Rule
                #add this [[fact, rule]] to the facts supported_by
                n = kb._get_fact(newFact)
                n.supported_by.append([fact, rule])
               
            
            #update lists
            fact.supports_facts.append(newFact)
            rule.supports_facts.append(newFact)
            
        else:
            
            # ---------------------- RULE ------------------------------ #
            
            #instantiate new facts accoridng to bindings, skipping first element of LHS
            newLHS = []
            for i in range(1, len(LHS)):
                newElem = instantiate(LHS[i], bindings)
                newLHS.append(newElem)
                
            #also instantiate RHS for new bindings
            newRHS = instantiate(rule.rhs, bindings)
            
            #create new rule and add it to the KB
            newRule = Rule([newLHS, newRHS], [[fact, rule]])

            if not kb._get_rule(newRule):
                kb.kb_add(newRule)
            else:
                n = kb._get_rule(newRule)
                n.supported_by.append([fact, rule])
                
            #update lists
            fact.supports_rules.append(newRule)
            rule.supports_rules.append(newRule)
                    
        
 
            
        
        
        
        
   
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        