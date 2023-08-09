def sanitize_datatable(con_table):
    # Using list comprehension to create the context_table
    context_table = [[value.strip() if value.strip() else None for value in row.cells]
                     for row in con_table]

    return context_table
