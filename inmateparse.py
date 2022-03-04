import pandas as pd

tables = pd.read_html("http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html")

print(tables[0])
