# from pseudeo_clique_caller.py import enumPseudoClique_1st_level
import util
from partition_new import mainPartition
import copy
# import numpy as np
import sys
import time
import pickle
import profile
from collections import defaultdict

def f_cover(SS):
	# print "SS", SS
	if len(SS) == 0:
		return 0
	covered_v = set()
	for S in SS:
		covered_v |= S

	return len(covered_v)

'''
def sieve(input_set):
	# print "LEAF NODE:", input_set
	global all_full 
	global max_gain
	global real_max_gain
	global O
	global S
	if max_gain < len(input_set):
		max_gain = len(input_set)
		# print "max_gain",max_gain, input_set
	if real_max_gain < len(input_set):
		real_max_gain = len(input_set)
		# print "real_max_gain",real_max_gain, input_set

	all_full = True
	# something_added = False
	num_no_full = 0
	O = []
	for i in range(real_max_gain, 2*k*real_max_gain + 1, 1):
		O.append(i)
		# S[i] = []
	# print "range", real_max_gain, 2*k*real_max_gain + 1, len(O)
	# print len(S)

	for non_key in S.keys():
		# print non_key
		if non_key < real_max_gain or non_key > 2*k*real_max_gain + 1:
			S.pop(non_key)
	
	# print "after remove",len(S)
	for v in O:
		# print "====v====", v

		covered_v = set()
		for subset in S[v]:
			covered_v |= subset

		marg_gain = 0
		for new_node in input_set:
			if new_node not in covered_v:
				marg_gain+=1

		# marg_gain = len(S_temp) - len(f_cover_old)
		# print "marg_gain", marg_gain
		


		# print "marg_gain", marg_gain

		# print v,"len:", len(S[v])
		
		if len(S[v]) < k:
			num_no_full +=1
			all_full = False
			if marg_gain >= (v/2.0 - len(covered_v))/(k - len(S[v])):
				# print "threshold",(v/2.0 - f_cover(S[v]))/(k - len(S[v]))
				# print "Adding", input_set, "to", v, S[v]
				S[v].append(input_set)
				# something_added=True

	# new covers added to track all covered vs
	# if something_added:
	# 	global covers
	# 	covers |= input_set
	# 	print "covers",len(covers)
	# print len(S)
	if float(num_no_full)/len(S) < 0.05:
		print "======== all full terminate ========"
		print "S len:"
		all_full = True
		for i in S.keys():
			print len(S[i]),
		print

def sieve_nonleaf(input_set, input_list):
	global max_gain
	global O
	# print "max_gain", max_gain

	flag = False
	v = O[-1]
	covered_v = set()

	for subset in S[v]:
		covered_v |= subset

	marg_gain = 0
	for new_node in input_set:
		if new_node not in covered_v:
			marg_gain+=1


	# S_temp = S[v] + [input_set]
	# marg_gain = f_cover( S_temp) - f_cover(S[v])
	max_potential_gain = max_gain - len(input_set) + marg_gain
	# print "####################", max_potential_gain
	if len(S[v]) < k:
		thre = (v/2.0 - len(covered_v))/(k - len(S[v]))
		if max_potential_gain > thre:
			# print "True",max_potential_gain, thre
			flag = True
			# else:
			# 	print "False",max_potential_gain, thre
		if flag == False:
			print "@@@@@@@@@@@@@@@@@@ pruned @@@@@@@@@@@@@@@@@@ ", input_list
	else:
		print "Full"
	return flag
'''
def N(S, E, V): # N(x)={y in V(G)| (x,y) in E(G)}, N(S)=U x in S N(x);
	# print "S,V",S,V
	N_S = set()
	for u in S:
		for v in set(V):
			if(frozenset([u, v]) in E): # neighbors
				N_S.add(v)
	return N_S

def comp_Potential(K, V_remain, E, theta, x, N_r, Union, AdjList):
	# return 1.0
	# N_r_S = compute_N_r(S, theta)
	# print "x", x, "K",K
	# N_x = set()
	# for v in Union:
	# 	if(frozenset([x, v]) in E): # neighbors
	# 		N_x.add(v)

	# print "Old",time.time()

	N_x = set()
	for edge_weight in AdjList[x]:
		if(edge_weight[0] in Union): # neighbors
			N_x.add(edge_weight[0])
	# print len(N_x), len(N_x_new)

	# print "New",time.time()
	N_r_x = N_x & N_r

	######### possible opt??? Need to go over all vs ###########
	# N_x2 = set()
	# for v in set(N_r):
	# 	if(frozenset([x, v]) in E): # neighbors
	# 		N_x2.add(v)
	# print "N_r_x", N_r_x, "N_x2", N_x2
	deg_x_S = len(N_x & K)

	
	# print "N_r_S",N_r, "N_x",N_x, N_r_x
	potential = len(N_r_x) + len(N_r)*(deg_x_S - theta*(len(K) +1.0 ))
	return potential


def sort_N_r(K, V_remain, E, theta, N_r, AdjList):
	potential_D = {}
	global D
	start_time = time.time()
	Union = K | V_remain
	for x in N_r:
		# potential_D[x] = 1.0
		potential_D[x] = comp_Potential(K, V_remain, E, theta, x, N_r, Union, AdjList)
		# print "potential:",x,potential_D[x]
		# print "g_degree:",x,D[x]
	# print "Done potential", time.time() - start_time
	return sorted(N_r, key = lambda k: (potential_D[k], D[k]), reverse = True)


def compute_N_r_New(K, V_remain, E, theta): # find all gamma neighbors on set S from V_remain
	# return set(V_remain)
	N_r = set()
	# print N_r

	if (len(K) == 1):
		u = K.pop()
		for v in V_remain:
			if(frozenset([u, v]) in E and E[frozenset([u, v])] >= theta):
				N_r.add(v)

		return N_r


	base_density = util.computeDensity(K, E, isWeight)
	n = len(K)
	edge_weight = base_density*(n-1)*n/2.0

	for v in V_remain:
		new_edge_weight = edge_weight
		for u in K:
			if(frozenset([u, v]) in E): # neighbors
				new_edge_weight+= E[frozenset([u, v])]
				# new_edge_weight+= 1

		new_density = new_edge_weight*2/((n+1)*n)
		if new_density >= theta:
			N_r.add(v)	

	return N_r	

# def compute_N_r(K, V_remain, E, theta): # find all gamma neighbors on set S from V_remain
# 	N_r = set()
# 	# print N_r
# 	for u in K:
# 		# print 'u',u
# 		for v in V_remain:
# 			if(frozenset([u, v]) in E): # neighbors
				
# 				S_temp = K.copy()
# 				S_temp.add(v)
# 				# r neighbor or not!!!!!!!! Change here
# 				if(util.computeDensity(S_temp, E) >= theta:
# 					N_r.add(v)	
# 					# print "v",v
# 	return N_r	

def grasp_sort(K, V_remain, E, theta, AdjList): #''' bottleneck! '''

	t0 = time.time()
	N_r = compute_N_r_New(K, V_remain, E, theta)

	# print "time of gamma neighbors new", time.time() - t0, len(N_r)

	
	t0 = time.time()

	# print "N_R here!!!!!!", len(N_r)
	N_r_sorted = sort_N_r(K, V_remain, E, theta, N_r, AdjList) #''' bottleneck! '''
	# print "time of N_r sort", time.time() - t0

	return N_r_sorted

def readGT(filename):
	fin = open(filename)
	groundTruth = set()
	for line in fin:
		line = line.rstrip().split("\t")
		groundTruth.add(frozenset(line))
	return groundTruth

def enumPseudoClique(K, V_remain, E, V, AdjList, theta, max_dense, dense, Ancestors, CoveredV):
	''' --------------@para: no of elem in K-------------- '''
	global max_gain
	global first_branch
	leaf_node = 1
	
	# for elem in K:
	# 	print str(elem) + "\t",
	# print float(dense)
	# print
	# if len(K) > min_elem_output:
	# print str(K) +"\t" + str(dense)
	# print "first_branch", first_branch
	# print "V_remain:", len(V_remain)
	if 0 == len(V_remain):
		print "===========reach base case ==========="
		first_branch = False
		K_set = set(K)
		CoveredV |= K_set
		# sieve(set(K))			
		all_first_branch.append(K_set)
	 	return


	if len(K) != 0: # 1st level
		# print "grasp_sort start"
		time_start = time.time()
		V_remain_in_seq = grasp_sort(set(K), set(V_remain), E, theta, AdjList)
		# print "grasp_sort end", time.time() - time_start
	
	# print "V_remain_in_seq", len(V_remain_in_seq)
	if len(K) == 1 and len(V_remain_in_seq) == 0:
		return
	for i in range(len(V_remain_in_seq)):
		# print "i", i
		v = V_remain_in_seq[i]

		K_new = copy.copy(K)
		# V_new = V_remain_in_seq[i+1:]
		# Ancestors = set(K_new) | set(V_remain_in_seq[:i])
		# print K,"sibling here ",V_remain_in_seq[:i]
		# print "V_remain_in_seq",V_remain_in_seq, " i",i
		
		# check connectivity, if v is not connect to K_new, pick another v
		v_deg = 0
		for u in K_new:
			# if v in AdjList[u]:
			if frozenset((u,v)) in E:
				# break
				v_deg+=1
		if K_new != [] and v_deg == 0:
			# print "pick another v"
			continue # pick another v
		# end	

		# D = util.computeDegree(list(K_new), E)
		# print "D",D,"K_new",K_new
		# min_deg = util.min_degree(D)

		K_new.append(v)

 		# print "K_new",K_new
 		start_time = time.time()
		new_dense = util.computeDensity(set(K_new), E, isWeight)
		# print "dense compute time", time.time() - start_time, new_dense

		# start_time = time.time()
		# new_dense = util.computeDensityNew(set(K_new), AdjList)
		# print "new dense compute time", time.time() - start_time, new_dense

		if new_dense >= theta:
			# print "Old Ancestors:", Ancestors
			if(not first_branch):
				# print "tracing back... "
				# continue
				return
			# print "v is", v
 			# print "Ancestors:", Ancestors_new
	 		if v in Ancestors:
	 			# print "In Ancestors......."
 				continue

			V_new = list(N(set(K_new), E, V)  - set(K_new) - Ancestors)
			Ancestors_new =  Ancestors | set(V_remain_in_seq[:i])

			# if (first_branch or sieve_nonleaf(set(K_new), K_new)):
			# if(first_branch):
			# if(True):

			leaf_node = 0
			# print "Next level"
			enumPseudoClique(K_new, V_new, E, V, AdjList, theta, max_dense, new_dense, Ancestors_new, CoveredV)

		else:
				print "stop enumerate due to dense"


	# print "leaf_node", leaf_node, set(K)
	if leaf_node:
		K_set = set(K)
		CoveredV |= K_set
		# sieve(set(K))
		all_first_branch.append(K_set)

	first_branch = False			
	# print "Reset Ancestors......"
	Ancestors = set()
	# print "S len:"
	# for i in range(k, k*m + 1, 1):
	# 	print len(S[i]),
	# print
	# should_add = True
	# for each_set in max_dense:
	# 	if set(each_set[0]).issuperset(set(K)):
	# 		# print "Here"
	# 		should_add = False
	# 		break
	# if should_add:
	# 	# print "leaf node", K, "dense", dense 
	# 	max_dense.append((K, dense))


# main
def main():
	# input_file = "../data/input_enum.txt"
	# input_file = "../data_tweet/input_whole_enum.txt"
	# input_file = "../data_tweet/tweet_complete_processed.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/collins2007.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/krogan2006_core.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/krogan2006_extended.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/gavin2006_socioaffinities_rescaled.txt"
	# input_file = "../data_tweet/corenlp_news/result10k.txt"

	# input_file = "../data_bio/cl1_datasets/datasets/biogrid_yeast_physical_unweighted.txt"

	input_file = "../data_snap/dblp_whole.txt"
	global max_gain
	global D
	print "Reading from:", input_file
	start_time = time.time()
	PartitionList = mainPartition(input_file, partitionTimes = 10, threSize = 500)
	print "time in partitioning", time.time() - start_time

	partitionIdx = 0
	for elem in PartitionList:
		print
		print "In", partitionIdx, "partition......"
		partitionIdx+=1

		(V, E, AdjList, D) = (list(elem.vs), elem.es, elem.adjs, elem.ds)
		V.sort(key = lambda k: (D[k], k), reverse=True)
		# (V, E, AdjList, D) = util.readinput(input_file, mytype = "str", myDelimiter = "\t", isWeight = False)

		max_dense = []

		# time.sleep(0.5)
		print "V input length ", len(V)
		print "E input length ", len(E)

		global first_branch
		# D = util.computeDegree_dict(list(V),E)
		# print "D computed"

		CoveredV = set()
		Ancestors = set()
		for i in range(len(V)):
			# print "V[i]",V[i]
			curV = V[i]

			first_branch = True

			# if all_full:
				# continue

			# print "CoveredV", (curV in CoveredV), curV

			if (curV in CoveredV):
				print "***********Skip seed ***********: ", i
				continue

			K = [V[i]]
			V_new = copy.copy(V)
			V_new.pop(i)
			print "========= progress =========: ", i, len(V)
			# print "Ancestors:", set(V[:i])
			max_gain  = 0
			# print "S keys",len(S.keys())
			enumPseudoClique(K, V_new, E, V, AdjList, theta, max_dense, 1.0, Ancestors, CoveredV)
			Ancestors.add(curV)

		# pickle.dump( max_dense, open( "save-0.5.p", "wb" ) )
		# max_dense = pickle.load( open( "save-0.5.p", "rb" ) )
		# print "max_dense_graph:"

		# coverage_set = set()
		# for each_set in max_dense:
		# 	if(len(each_set[0]) > 2 and len(each_set[0]) <=10 ):
		# 		for elem in each_set[0]:
		# 			if elem not in coverage_set:
		# 				# print elem
		# 				coverage_set.add(elem)
		# 		print str(each_set[0]) + '\t' + str(each_set[1])

		# print "coverage: ",len(coverage_set)
		


		print "========================="
		print "All first_branch. threshold", theta
		print "========================="
		for elem in all_first_branch:
			if(len(elem) >= min_elem_output):
				# density = util.computeDensity(elem, E)
				# print elem, density
				aggregated_max_dense.add(frozenset(elem))

				for node in elem:
					print str(node) + "\t",
				print
		print "total MDS ", len(all_first_branch), "with size >=", min_elem_output


	# out of for



aggregated_max_dense = set()
k = 0
theta = 0.0
if(len(sys.argv) != 5):
	# print "Usage: **.py <inputfile> <k> <threshold> <min_elem_output>"
	# input_line  = raw_input("Exit? Y or N: ")
	# if(input_line in ['Y','y','Yes','YES','yes']):
	# 	sys.exit()
	# print "Running default... k=20, theta=0.97, min_elem_output=3"

	
	k = 50
	theta = 0.6
	min_elem_output = 5

else:
	# input_file = sys.argv[1]
	k = int(sys.argv[2])
	theta = float(sys.argv[3])
	min_elem_output = int(sys.argv[4])

# m = 10

D = {}
# covers = set()
first_branch = True
isWeight = False
all_first_branch = []
start_time = time.time()
groundTruth = readGT("../data_amazon/com-amazon.all.dedup.cmty.txt")

main()
tp = 0
print "Evaluating......"
for elem in aggregated_max_dense:
	print elem
	for gt in groundTruth:
		if elem.issubset(gt):
			tp+=1
			break



print "num of MDS found",len(aggregated_max_dense), tp
print("--- %s seconds ---" % (time.time() - start_time))







