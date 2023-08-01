def sanitize_datatable(con_table):
    # Using list comprehension to create the context_table
    context_table = [
        [None if len(value.strip()) == 0 else value.strip() for value in row.cells]
        for row in con_table
    ]
    return context_table
