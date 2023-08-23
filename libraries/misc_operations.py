def sanitize_datatable(context_table):
    # Using list comprehension to create the context_table
    con_table = []
    if context_table:
        con_table = [[value.strip() if value.strip() else None for value in row.cells]
                     for row in context_table]

    return con_table
