from nltk.grammar import is_nonterminal,PCFG,is_terminal,ProbabilisticProduction
from numpy.random import choice
from numpy import sum, log, matrix, identity,array,arange
from itertools import chain
from nltk.tree import Tree


def NonTerminalsPCFG(pcfg):
	return set(r.lhs() for r in pcfg.productions())


def PreterminalizeTree(tr):
	if type(tr) is str:
		return None
	elif len(tr)==1 and type(tr[0]) is str:
		return tr.label()
	else:
		return Tree(tr.label(),\
			[PreterminalizeTree(t) for t in tr])


def PreterminalizePCFG(grammar):
	if grammar.is_nonlexical():
		start = grammar.start()
		productions = [p for p in grammar.productions() if p.is_nonlexical()]
		terminals = set(p.lhs() for p in productions)
		productions = [_makeTerminal(p,terminals) for p in productions]
		return PCFG(start=start,productions=productions)
	else:
		return grammar

def SampleFromPCFG(grammar,start=None):
	if start==None:
		tupleSymbols = (grammar.start(),)
	else:
		tupleSymbols = (start,)
	lprob = 0.0
	while any(is_nonterminal(symbol) for symbol in tupleSymbols):
		tupleSymbols,lprob1 = _expand_seq(tupleSymbols,grammar)
		lprob += lprob1
	return (tupleSymbols,lprob)

def SampleTreeFromPCFG(grammar,start=None):
    if start==None:
        start = grammar.start()
    if type(start) is str:
        return start
    else:
        rules = grammar.productions(lhs=start)
        probs = [p.prob() for p in rules]
        rule = choice(rules,p=probs)
        return Tree(str(rule.lhs()),[SampleTreeFromPCFG(grammar,s) for s in rule.rhs()])

def CharacteristicPCFG(pcfg):
	nonterminals = NonTerminalsPCFG(pcfg)
	char_matrix = matrix( \
		[ [ sum(r.prob() * r.rhs().count(nt_col) for r in pcfg.productions(lhs=nt_row))
			for nt_col in nonterminals ] for nt_row in nonterminals ] )
	return char_matrix

def EntropyPCFG(pcfg,char_matrix=None,ruleset_ents=None):
	nonterminals = NonTerminalsPCFG(pcfg)
	if ruleset_ents==None:
		ruleset_ents = _EntropyVector(pcfg)
	if char_matrix==None:
		char_matrix = CharacteristicPCFG(pcfg)
	dim = len(nonterminals)
	expansion_ents = array((identity(dim) - char_matrix).I * ruleset_ents)
	expansion_ents.shape = (len(nonterminals,))
	results = dict(zip(nonterminals,list(expansion_ents)))
	return results

def MeanLengthPCFG(pcfg,char_matrix=None,ruleset_lens=None,character=None):
	nonterminals = NonTerminalsPCFG(pcfg)
	if ruleset_lens==None:
		ruleset_lens = _LengthVector(pcfg,character)
	if char_matrix==None:
		char_matrix = CharacteristicPCFG(pcfg)
	dim = len(nonterminals)
	expansion_ents = array((identity(dim) - char_matrix).I * ruleset_lens)
	expansion_ents.shape = (len(nonterminals,))
	results = dict(zip(nonterminals,list(expansion_ents)))
	return results


def MeanYngve(pcfg,char_matrix=None):
    nonterminals = NonTerminalsPCFG(pcfg)
    if char_matrix==None:
        char_matrix = CharacteristicPCFG(pcfg)
    lengths = array(MeanLengthPCFG(pcfg,char_matrix=char_matrix).values())
    y = _YngveVector(pcfg,lengths)
    yngve = array((identity(dim) - char_matrix).I * y)
    yngve.shape = (len(nonterminals,))
    results = dict(zip(nonterminals,list(yngve/lengths)))
    return results

def YngveTree(t,seed=0.0,root=True):
    if type(t) is str:
        return seed
    else:
        w=seed+arange(len(t)-1.,-1,-1)
        res = sum([YngveTree(t[i],seed=w[i],root=False) for i in range(len(t))])
        if root:
            res/=float(len(t.leaves()))
        return res

#########################################
# Auxiliary functions
#########################################

def _EntropyVector(pcfg):
	nonterminals = NonTerminalsPCFG(pcfg)
	ruleset_ents = matrix([[-sum(r.prob()*log(r.prob()) for r in pcfg.productions(lhs=nt))] \
		 for nt in nonterminals])
	return ruleset_ents

def _LengthVector(pcfg,character=None):
	nonterminals = NonTerminalsPCFG(pcfg)
	if character == None:
		ruleset_lens = matrix([[sum([r.prob()*len([s for s in r.rhs() if is_terminal(s)])\
			for r in pcfg.productions(lhs=nt)])] \
			 for nt in nonterminals])
	else:
		ruleset_lens = matrix([[sum([r.prob()*len([s for s in r.rhs() if s==character])\
			for r in pcfg.productions(lhs=nt)])] \
			 for nt in nonterminals])		
	return ruleset_lens

def _YngveVector(pcfg,lengths):
    nonterminals = list(NonTerminalsPCFG(pcfg))
    return matrix([[sum([sum(arange(float(len(r.rhs())))*lengths[[nonterminals.index(s2)\
                                                                  for s2 in r.rhs()]])*r.prob()\
                         for r in pcfg.productions(lhs=s)])]\
                   for s in nonterminals])

def _expand_seq(symbol_l,grammar):
	lista = [_expand(s,grammar) for s in symbol_l]
	symbols,lprobs = zip(*lista)
	newchain = list(chain.from_iterable(symbols)) 
	newprob  = sum(lprobs)
	return (newchain,newprob)

def _expand(symbol,grammar):
	if is_nonterminal(symbol):
		rules = grammar.productions(lhs=symbol)
		probs = [r.prob() for r in rules]
		rule = choice(rules,p=probs)
		return (rule.rhs(),log(rule.prob()))
	else:
		return ((symbol,),0.0)

def _makeTerminal(rule,terminals):
	lhs = rule.lhs()
	rhs = [_auxTerminal(s,terminals) for s in rule.rhs()]
	prob = rule.prob()
	return ProbabilisticProduction(lhs=lhs,rhs=rhs,prob=prob)

def _auxTerminal(character,charset):
	if character in charset:
		return character
	else:
		return str(character)


