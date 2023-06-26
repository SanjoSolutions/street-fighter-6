def deduplicate(entries):
    dictionary = dict()
    result_entries = list()
    for entry in entries:
        from_ = entry[0]
        to = entry[1]
        if from_ not in dictionary or to not in dictionary[from_]:
            result_entries.append(entry)
            if from_ not in dictionary:
                dictionary[from_] = set()
            dictionary[from_].add(to)
    return result_entries
