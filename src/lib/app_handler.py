import pandas as pd
import re
import json

def merge_to_one(tables):
    table = []
    for index in range(len(tables)):
        if index == 0:
            table = tables[index]
        else:
            if (table['Blocks']):
                table['Blocks'].extend(tables[index]['Blocks'])
    return table

def get_valid_tables(json_tables):
    headers = ["Quantity", "Description", "Unit Cost","RCV","DEP","ACV"]
    valid_tables = []
    for table in json_tables:
        col_headers = table[1].values()
        valid_header_count = 0
        for col_header in col_headers:
            if (col_header.strip() in headers):
                valid_header_count += 1
        if(valid_header_count>0):
            valid_tables.append(table)
    return valid_tables

def create_rooms(valid_tables):
    temp_df = None
    rooms = []
    for table in valid_tables:
        df = pd.DataFrame(data=table)
        df = df.set_index(list(df)[0]).T  

        last_row = df.iloc[[-1]].values
        r = re.compile(r'Totals For*')
        end_line = list(filter(r.match, last_row[0]))
        if(len(end_line)>0):
            room_name = end_line[0].split("Totals For")[1]
            final_df = temp_df.iloc[:-1,:].reset_index(drop=True)
            items = final_df.to_json(orient='records')
            room = {
                "room_name": room_name,
                "items": json.loads(items)
            }
            rooms.append(room)
        else:
            if(temp_df is not None):
                temp_df = temp_df.append(df, sort=False)
            else:
                temp_df = df 
        
    return rooms
