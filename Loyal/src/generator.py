import copy
import math
import random
from collections import defaultdict
import json
import sys

sys.path.append('config')
from config_test import config

class testGenerator :
    def __init__(self, n_replicas, n_twins, n_rounds, n_partitions, is_leader_faulty, partition_num_limit, n_test_cases,
                            leader_partitions_num_limit, random_seed, is_deterministic =  True) :
        self.partitions_list = []
        random.seed(random_seed)
        self.partition_generation_algorithm (n_replicas + n_twins, n_partitions)
        for i in range(len(self.partitions_list)) :
            for j in range(n_partitions) :
                for k in range(len(self.partitions_list[i][j])) :
                    if self.partitions_list[i][j][k] <= n_replicas :
                        self.partitions_list[i][j][k] = "replica_" + str(self.partitions_list[i][j][k] - 1)
                    else :
                        self.partitions_list[i][j][k] = "replica_" + str(self.partitions_list[i][j][k] - 1 - n_replicas)  + "f"
        self.adjustPartitions(n_replicas, n_twins, n_partitions)
        if is_deterministic == True :
            self.partitions_list = self.partitions_list[: min(partition_num_limit, len(self.partitions_list))]
        else :
            self.partitions_list = random.choices(self.partitions_list, k = min(partition_num_limit, len(self.partitions_list)))
        self.low_partition_list = []
        pop_list = []
        for i,partition_combination in enumerate(self.partitions_list) :
            is_quorum = False
            for j in range(n_partitions) :
                if len(partition_combination[j]) >= 2*n_twins + 1  :
                    is_quorum = True
                    break
            if not is_quorum :
                self.low_partition_list.append(partition_combination)
                pop_list.append(partition_combination)

        if len(pop_list) == 0 :
            for i,partition_combination in enumerate(self.partitions_list) :
                c_quorum = 0
                for j in range(n_partitions) :
                    if len(partition_combination[j]) >= 2*n_twins + 1  :
                        c_quorum = c_quorum +  1
                if c_quorum == 1 :
                    self.low_partition_list.append(partition_combination)
                    pop_list.append(partition_combination)

        for i in range(len(pop_list)) :
            self.partitions_list.remove(pop_list[i])


        partition_leader_combination = []
        for i in range(n_twins,n_replicas) :
            for j in range(len(self.partitions_list)):
                partition_leader_combination.append(["replica_" + str(i), self.partitions_list[j]])

        low_partition_leader_combination = []
        for i in range(n_twins,n_replicas) :
            for j in range(len(self.low_partition_list)):
                low_partition_leader_combination.append(["replica_" + str(i), self.low_partition_list[j]])


        if is_leader_faulty == True:
            for i in range(n_twins) :
                for j in range(len(self.partitions_list)):
                    partition_leader_combination.append(["replica_" + str(i), self.partitions_list[j]])


            for i in range(n_twins) :
                for j in range(len(self.low_partition_list)):
                    low_partition_leader_combination.append(["replica_" + str(i), self.low_partition_list[j]])

        ratio = len(partition_leader_combination) /( len(partition_leader_combination) + len(low_partition_leader_combination))
        if is_deterministic == True :
            partition_leader_combination = partition_leader_combination[:math.ceil(ratio * leader_partitions_num_limit)]
            low_partition_leader_combination = low_partition_leader_combination[:math.ceil((1 - ratio) * leader_partitions_num_limit)]
        else :
            partition_leader_combination = random.choices(partition_leader_combination, k = math.ceil(ratio * leader_partitions_num_limit))
            low_partition_leader_combination = random.choices(low_partition_leader_combination, k = math.ceil((1 - ratio) * leader_partitions_num_limit))

        i = 0
        live = 0
        no_live = 0
        while i < n_test_cases :
            test_case_data = {}
            non_quorum_rounds = random.randint(0,n_rounds - 3)
            quorum_rounds =   n_rounds - non_quorum_rounds
            low_current_round_combination = random.choices(low_partition_leader_combination, k = non_quorum_rounds)
            current_round_combination = random.choices(partition_leader_combination, k = quorum_rounds)
            test_case_data['rounds'] = {}
            for j in range(0,non_quorum_rounds) :
                test_case_data['rounds'][j + 1] = {}
                test_case_data['rounds'][j + 1]['leader'] = low_current_round_combination[j][0]
                test_case_data['rounds'][j + 1]['partitions'] = low_current_round_combination[j][1]
                test_case_data['rounds'][j + 1]['messageType'] = random.randint(0,2)
                test_case_data['rounds'][j + 1]['failType'] = random.randint(0,2)
                test_case_data['rounds'][j + 1]['src_to_dest'] = self.get_src_dest_combs(low_current_round_combination[j])

            for j in range(non_quorum_rounds, n_rounds) :
                test_case_data['rounds'][j + 1] = {}
                test_case_data['rounds'][j + 1]['leader'] = current_round_combination[j - non_quorum_rounds][0]
                test_case_data['rounds'][j + 1]['partitions'] = current_round_combination[j - non_quorum_rounds][1]
                test_case_data['rounds'][j + 1]['messageType'] = random.randint(0,2)
                test_case_data['rounds'][j + 1]['failType'] = random.randint(0,2)
                test_case_data['rounds'][j + 1]['src_to_dest'] = self.get_src_dest_combs(current_round_combination[j - non_quorum_rounds])


            is_valid_test_case = self.is_valid_test(test_case_data, n_replicas,n_twins, n_rounds )
            if is_valid_test_case :
                live = live + 1
                test_case_data['n_replicas'] = n_replicas
                test_case_data['n_twins'] = n_twins
                test_case_data['n_rounds'] = n_rounds
                with open('tests/test_case_' + str(i) + '.json', 'w', encoding='utf-8') as f:
                    json.dump(test_case_data, f, ensure_ascii=False, indent=4)
                i = i + 1
            else :
                no_live = no_live + 1
        print("live", live,no_live)


    def get_src_dest_combs(self, partition_combination) :
        leader = partition_combination[0]
        partition = []
        for i in range(len(partition_combination[1])) :
            found = False
            for j in range(len(partition_combination[1][i])) :
                if leader == partition_combination[1][i][j] :
                    partition = partition_combination[1][i]
                    found = True
                    break
            if found :
                break

        srcs = random.choices(partition, k = 2*len(partition))
        src_to_dests = defaultdict(lambda: [])
        dests = random.choices(partition, k = 2*len(partition))
        for i in range(len(srcs)) :
            choice = random.randint(0,2)
            if choice == 0 or choice == 1 :
                src_to_dests[srcs[i]].append(dests[i])
                src_to_dests[srcs[i]] = list(set(src_to_dests[srcs[i]]))
        return src_to_dests

    def  is_valid_test(self, test_data, n_replicas,n_twins, n_rounds ) :
            is_quorum = {}
            for  i in range(n_replicas) :
                is_quorum['replica_' + str(i)] = False
                if i < n_twins :
                    is_quorum['replica_' + str(i) + 'f'] = False
            quorum_rounds = {}
            for  i in range(n_replicas) :
                quorum_rounds['replica_' + str(i)] = []
                if i < n_twins :
                    quorum_rounds['replica_' + str(i) + 'f'] = []
            whole_count = 0
            for round in test_data['rounds'] :
                leader = test_data['rounds'][round]['leader']
                partitions = []
                for i in range(len( test_data['rounds'][round]['partitions'])) :
                    found = False
                    for j in range(len( test_data['rounds'][round]['partitions'][i])) :
                        if leader == test_data['rounds'][round]['partitions'][i][j] :
                            partitions.append(test_data['rounds'][round]['partitions'][i])
                            found = True
                            break
                failType = test_data['rounds'][round]['failType']
                src_to_dest  = test_data['rounds'][round]['src_to_dest']
                for partition in partitions :
                    partition_len = len(partition)
                    if partition_len == n_twins + n_replicas :
                        whole_count = whole_count + 1
                    if failType == 0 or failType == 1 :
                        for src in src_to_dest.keys() :
                            for dest in src_to_dest[src] :
                                if src in partition and dest in partition :
                                    partition_len = partition_len - 1
                    if(partition_len  >= 2*n_twins + 1) :
                        for replica in partition :
                            quorum_rounds[replica].append(round)
            if whole_count > 1  :
               return False


            for replica in quorum_rounds :
                if len(quorum_rounds[replica]) >= 2*n_twins + 1 :
                    i = 0
                    while i < len(quorum_rounds[replica]) - 2 :
                        if (quorum_rounds[replica][i] == quorum_rounds[replica][i + 1]  - 1) and (quorum_rounds[replica][i] == quorum_rounds[replica][i + 2] - 2) :
                             is_quorum[replica] = True
                        i = i + 1
            for replica in is_quorum :
                if is_quorum[replica] == False :
                    return False
            return True

    def partition_generation_algorithm(self, n, k) :
        answer = []
        for i in range(k) :
            answer.append([])
        self.solution(1, n, k, 0,  answer)

    def powerset(self, s):
        x = len(s)
        subset_list = []
        for i in range(1 << x):
            subset_list.append([s[j] for j in range(x) if (i & (1 << j))])
        return subset_list

    def adjustPartitions(self, n_replicas, n_twins, n_partitions) :
        replica_list = []
        for  i in range(n_replicas) :
            replica_list.append('replica_' + str(i))
            if i < n_twins :
                replica_list.append('replica_' + str(i) + 'f')
        subset_list = self.powerset(replica_list)
        visited = defaultdict(lambda: False)
        for i in range(len(self.partitions_list)) :
            for j in range(len(subset_list)) :
                new_partition_list =  copy.deepcopy(self.partitions_list[i])
                if len(subset_list[j]) <= 1 :
                    new_partition_list[0].extend(subset_list[j])
                    new_partition_list[0] =  copy.deepcopy(list(set(new_partition_list[0])))
                    if len(new_partition_list[0]) > len(self.partitions_list[i][0]) :
                        key_str = ""
                        for k in range(len(new_partition_list)) :
                            key_str = key_str + " ".join(new_partition_list[k]) + " |"
                        if visited[key_str] == False :
                            self.partitions_list.append(new_partition_list)
                            visited[key_str] = True

    def solution(self, i, n, k, nums, answer) :
        if i > n :
            if nums == k :
                self.partitions_list.append(copy.deepcopy(answer))
            return
        for j in range(0, len(answer))  :
            if len(answer[j]) > 0 :
                answer[j].append(i)
                results = self.solution(i + 1 , n, k, nums, answer)
                if len(answer) > 0  : answer[j].pop()
            else :
                answer[j].append(i)
                results = self.solution(i + 1, n, k, nums + 1, answer)
                if len(answer) > 0 : answer[j].pop()
                break

n_replicas  = config['n_replicas']
n_twins =  config['n_twins']
n_rounds = config['n_rounds']
n_partitions  = config['n_partitions']
is_leader_faulty = config['is_leader_faulty']
partition_num_limit = config['partition_num_limit']
n_test_cases = config['n_test_cases']
leader_partitions_num_limit  = config['leader_partitions_num_limit']
random_seed = config['random_seed']
is_deterministic = config['is_deterministic']
my_test_generator = testGenerator(n_replicas, n_twins, n_rounds, n_partitions, is_leader_faulty, partition_num_limit, n_test_cases,
                        leader_partitions_num_limit, random_seed, is_deterministic)
