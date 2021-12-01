import copy
import math
import random
from collections import defaultdict
import json
class testGenerator :
    def __init__(self, n_replicas, n_twins, n_rounds, n_partitions, is_leader_faulty, partition_num_limit, n_test_cases,
                            leader_partitions_num_limit, random_seed) :
        self.partitions_list = []
        self.partition_generation_algorithm (n_replicas + n_twins, n_partitions)
        for i in range(len(self.partitions_list)) :
            for j in range(n_partitions) :
                for k in range(len(self.partitions_list[i][j])) :
                    if self.partitions_list[i][j][k] <= n_replicas :
                        self.partitions_list[i][j][k] = "replica_" + str(self.partitions_list[i][j][k] - 1)
                    else :
                        self.partitions_list[i][j][k] = "replica_" + str(self.partitions_list[i][j][k] - 1 - n_replicas)  + "f"
        print("results", self.partitions_list)
        self.partitions_list = self.partitions_list[: min(partition_num_limit, len(self.partitions_list))]

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
            for j in range(len(self.partitions_list)):
                low_partition_leader_combination.append(["replica_" + str(i), self.low_partition_list[j]])


        if is_leader_faulty == True:
            for i in range(n_twins) :
                for j in range(len(self.partitions_list)):
                    partition_leader_combination.append(["replica_" + str(i), self.partitions_list[j]])

            for i in range(n_twins) :
                for j in range(len(self.partitions_list)):
                    partition_leader_combination.append(["replica_" + str(i) + "f", self.partitions_list[j]])


            for i in range(n_twins) :
                for j in range(len(self.partitions_list)):
                    low_partition_leader_combination.append(["replica_" + str(i), self.low_partition_list[j]])

            for i in range(n_twins) :
                for j in range(len(self.partitions_list)):
                    low_partition_leader_combination.append(["replica_" + str(i) + "f", self.low_partition_list[j]])

        ratio = len(partition_leader_combination) /( len(partition_leader_combination) + len(low_partition_leader_combination))
        partition_leader_combination = partition_leader_combination[:math.ceil(ratio * leader_partitions_num_limit)]
        low_partition_leader_combination = low_partition_leader_combination[:math.ceil((1 - ratio) * leader_partitions_num_limit)]

        i = 0
        while i < n_test_cases :
            test_case_data = {}
            non_quorum_rounds = random.randint(0,n_rounds)
            quorum_rounds =   n_rounds - non_quorum_rounds
            low_current_round_combination = random.choices(low_partition_leader_combination, k = non_quorum_rounds)
            current_round_combination = random.choices(partition_leader_combination, k = quorum_rounds)
            test_case_data['rounds'] = {}
            for j in range(0,non_quorum_rounds) :
                test_case_data['rounds'][j] = {}
                test_case_data['rounds'][j]['leader'] = low_current_round_combination[j][0]
                test_case_data['rounds'][j]['partitions'] = low_current_round_combination[j][1]
                test_case_data['rounds'][j]['messageType'] = random.randint(0,3)
                test_case_data['rounds'][j]['failType'] = random.randint(0,2)
                test_case_data['rounds'][j]['src_to_dest'] = self.get_src_dest_combs(low_current_round_combination[j])

            for j in range(non_quorum_rounds, n_rounds) :
                test_case_data['rounds'][j] = {}
                test_case_data['rounds'][j]['leader'] = current_round_combination[j - non_quorum_rounds][0]
                test_case_data['rounds'][j]['partitions'] = current_round_combination[j - non_quorum_rounds][1]
                test_case_data['rounds'][j]['messageType'] = random.randint(0,3)
                test_case_data['rounds'][j]['failType'] = random.randint(0,2)
                test_case_data['rounds'][j]['src_to_dest'] = self.get_src_dest_combs(current_round_combination[j - non_quorum_rounds])


            is_valid_test_case = self.is_valid_test(test_case_data, n_replicas,n_twins, n_rounds )
            if is_valid_test_case :
                test_case_data['n_replicas'] = n_replicas
                test_case_data['n_twins'] = n_twins
                test_case_data['n_rounds'] = n_rounds
                with open('tests/test_case_' + str(i) + '.json', 'w', encoding='utf-8') as f:
                    json.dump(test_case_data, f, ensure_ascii=False, indent=4)
                i = i + 1


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
            choice = random.randint(0,3)
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

            for round in test_data['rounds'] :
                leader = test_data['rounds'][round]['leader']
                partition = []
                for i in range(len( test_data['rounds'][round]['partitions'])) :
                    found = False
                    for j in range(len( test_data['rounds'][round]['partitions'][i])) :
                        if leader == test_data['rounds'][round]['partitions'][i][j] :
                            partition = test_data['rounds'][round]['partitions'][i]
                            found = True
                            break
                    if found :
                        break
                if(len(partition) >= 2*n_twins + 1) :
                    for replica in partition :
                        quorum_rounds[replica].append(round)

            for replica in quorum_rounds :
                if len(quorum_rounds[replica]) >= 2*n_twins + 1 :
                    i = 0
                    while i < len(quorum_rounds[replica]) - 2 :
                        if (quorum_rounds[replica][i] == quorum_rounds[replica][i + 1]  - 1) and (quorum_rounds[replica][i] == quorum_rounds[replica][i + 2] - 2) :
                             is_quorum[replica] = True
                        i = i + 1
            for replica in is_quorum :
                if is_quorum[replica] == True :
                    return True
            return False


    def partition_generation_algorithm(self, n, k) :
        answer = []
        for i in range(k) :
            answer.append([])
        self.solution(1, n, k, 0,  answer)


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

my_test_generator = testGenerator(5,1, 5, 2, True, 100, 5, 100, 125)