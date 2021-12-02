from collections import defaultdict
def is_safe(directory_path, n_twins, n_replicas) :
    transaction_dictionary = defaultdict(lambda : 0)
    for i in range(0,n_twins) :
        filename = "validator_" + str(i) + ".ledger"
        fp = open(directory_path + "/" + filename, 'r')
        lines = fp.readlines()
        for line in lines :
            transaction_dictionary[line.strip()] = transaction_dictionary[line.strip()] + 1
        fp.close()
        filename = "validator_" + str(i) + "_twin.ledger"
        fp = open(directory_path + "/" + filename, 'r')
        lines = fp.readlines()
        for line in lines :
            transaction_dictionary[line.strip()] = transaction_dictionary[line.strip()] +  1
        fp.close()
    for i in range(n_twins, n_replicas) :
        filename = "validator_" + str(i) + ".ledger"
        fp = open(directory_path + "/" + filename, 'r')
        lines = fp.readlines()
        for line in lines :
            transaction_dictionary[line.strip()] = transaction_dictionary[line.strip()] +  1
        fp.close()
    for transaction in transaction_dictionary :
        if transaction_dictionary[transaction] < 2 * n_twins  + 1 :
            return False
    return True

def is_live(directory_path, n_twins, n_replicas) :
    validator_dict = defaultdict(lambda : 0)
    for i in range(0,n_twins) :
        filename = "validator_" + str(i) + ".ledger"
        fp = open(directory_path + "/" + filename, 'r')
        lines = fp.readlines()
        line_count = 0
        for line in lines :
            if '-' in line : line_count = line_count + 1
        fp.close()
        validator_dict[filename] = line_count
        filename = "validator_" + str(i) + "_twin.ledger"
        fp = open(directory_path + "/" + filename, 'r')
        lines = fp.readlines()
        line_count = 0
        for line in lines :
            if '-' in line : line_count = line_count + 1
        fp.close()
        validator_dict[filename] = line_count
    for i in range(n_twins, n_replicas) :
        filename = "validator_" + str(i) + ".ledger"
        fp = open(directory_path + "/" + filename, 'r')
        lines = fp.readlines()
        line_count = 0
        for line in lines :
            if '-' in line : line_count = line_count + 1
        fp.close()
        validator_dict[filename] = line_count
    validator_cnt = 0
    for validator in validator_dict :
        if validator_dict[validator] == 0  :
            validator_cnt = validator_cnt + 1
    if n_twins  + n_replicas - validator_cnt  > 2 * n_twins + 1 : return True
    return False


print(is_safe("ledgers/config0/test_case_0",1,5))
print(is_live("ledgers/config0/test_case_0",1,5))
