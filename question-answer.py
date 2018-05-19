#!/usr/bin/env python


import sys, nltk
from nltk.tree import Tree


# See if our pattern matches the current root of the tree
def matches(pattern, root):
	# Base cases to exit our recursion
	# If both nodes are null we've matched everything so far
	if root is None and pattern is None: 
		return root
		
	# We've matched everything in the pattern we're supposed to (we can ignore the extra
	# nodes in the main tree for now)
	elif pattern is None:				
		return root
		
	# We still have something in our pattern, but there's nothing to match in the tree
	elif root is None:				   
		return None

	# A node in a tree can either be a string (if it is a leaf) or node
	plabel = pattern if isinstance(pattern, str) else pattern.label()
	rlabel = root if isinstance(root, str) else root.label()

	# If our pattern label is the * then match no matter what
	if plabel == "*":
		return root
	# Otherwise they labels need to match
	elif plabel == rlabel:
		# If there is a match we need to check that all the children match
		# Minor bug (what happens if the pattern has more children than the tree)
		for pchild, rchild in zip(pattern, root):
			match = matches(pchild, rchild) 
			if match is None:
				return None 
		return root
	
	return None
	
def pattern_matcher(pattern, tree):
	for subtree in tree.subtrees():
		node = matches(pattern, subtree)
		if node is not None:
			return node
	return None
	
def question_type(parsed, type="where"):
	if type == "where":
		pattern = nltk.ParentedTree.fromstring("(VP (*)* (PP))")
		subtree = pattern_matcher(pattern, parsed)
		pattern = nltk.ParentedTree.fromstring("(PP)")
		subtree2 = pattern_matcher(pattern, subtree)
		return " ".join(subtree2.leaves())
	

def prepare_pars(raw_pars):
    return Tree.fromstring("(ROOT "+raw_pars)
			
			
if __name__ == '__main__':

	tree = prepare_pars("(S (NP (DT A) (NN Crow)) (VP (VBD was) (VP (VBG sitting) (PP (IN on) (NP (NP (DT a) (NN branch)) (PP (IN of) (NP (NP (DT a) (NN tree)) (PP (IN with) (NP (NP (DT a) (NN piece)) (PP (IN of) (NP (NP (NN cheese)) (PP (IN in) (NP (PRP$ her) (NN beak))))))))))) (SBAR (WHADVP (WRB when)) (S (NP (DT a) (NNP Fox)) (VP (VP (VBD observed) (NP (PRP her))) (CC and) (VP (VB set) (NP (PRP$ his) (NNS wits)) (S (VP (TO to) (VP (VB work) (S (VP (TO to) (VP (VB discover) (NP (NP (DT some) (NN way)) (PP (IN of) (S (VP (VBG getting) (NP (DT the) (NN cheese)))))))))))))))))) (. .)))")

	
	print(question_type(tree))
