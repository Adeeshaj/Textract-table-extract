

def merge_to_one(tables):
    table = []
    for index in range(len(tables)):
        if index == 0:
            table = tables[index]
        else:
            if (table['Blocks']):
                table['Blocks'].extends(tables[index]['Blocks'])
    return table