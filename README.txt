# dist_project
Platform:
 	python : 3.7
  	DistAlgo : 1.1.0b15
  	Host : Laptop
  	Operating Systems and version: Ubuntu ,20
  
Workload Generation:
	Generate random strings of length and append it to client_id-command_id: to generate transactions.
	ex : client_1-0:hdtuosplne
	number of transactions to generate is set through test case config file as mentioned in user manual.
	Files used : client.da

Timeouts:
	Replica:
	replica timeout formula for a round : 4 * network delta
	path in code: /src/replica.da/Pacemaker_get_round_timer
	network delta is set from test case config file. Check user manual.
	Client:
	timeout for client to terminate if did not receive appropriate responses from replicas.
	Set using attribute 'client_timeout' in test case config file. Check user manual.
	Implemented in client.da


Main files:
	Driver code : main.da
	Client code : dist_project/src/client.da
	Replica code : dist_project/src/replica.da 
	Faulty Replica code : dist_project/src/replica_fault.da
	Ledger code : dist_project/src/ledger.py
	Timeout classes : dist_project/src/timeout.py
	Generic Tree module : dist_project/src/tree.py
	Block Tree classes : dist_project/src/block_tree.py
	Utils (signature verifications) : dist_project/src/utils.py

Code size:
	(1) Non blank, non comment lines of code (LOC):
		algorithm : 779
		others : 132
		total : 911
	(2) Lines of code obtained from CLOC (https://github.com/AIDanial/cloc)
	(3) replica algorithm : 90 % other 10 %

Language feature Usage:
	awaits - 5
	receive handlers - 3
	sets - 8
	Cacheout cache - 2
	dict - 9
	namedtuple -2
	list - 5

Contributions:
	Manikanta Sathwik Yeluri(113785603): Event processing, Leader Election, PaceMaker, BlockTree, Mempool, Tree for storing pending block tree, 
	Preetham Reddy Katta(113504974): Client, Safety, Ledger, Replica, Hashing, signature verification, main
	Sai Bhavana Ambati(114353386): Pseudo Codes, Fault Replica, test cases, helped in design of other modules
	


	



  
  
