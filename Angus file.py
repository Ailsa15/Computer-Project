
from openpyxl import load_workbook, Workbook

input_file = r"C:\Durham\Year 3\Computing Project\Angus\All of Campbell Prose words.xlsx"
output_file = r"C:\Durham\Year 3\Computing Project\Angus\odd_rows_only11.xlsx"

# Open input workbook
wb = load_workbook(input_file)
ws = wb.active

# Create output workbook
out_wb = Workbook()
out_ws = out_wb.active

out_row = 1

# Excel rows are 1-based
for row in range(2, ws.max_row + 1, 2):  # 1,3,5,...
    for col in range(1, ws.max_column + 1):
        out_ws.cell(row=out_row, column=col).value = ws.cell(row=row, column=col).value
    out_row += 1

out_wb.save(output_file)

print("ODD ROWS EXPORTED SUCCESSFULLY")
