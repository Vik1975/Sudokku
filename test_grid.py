import tkinter as tk

root = tk.Tk()
root.title("Test Grid")
root.geometry("600x800")

# Create a simple test grid
grid_frame = tk.Frame(root, bg="red", padx=2, pady=2)
grid_frame.pack(pady=20)

for i in range(9):
    for j in range(9):
        cell = tk.Label(grid_frame, text=f"{i},{j}", width=4, height=2,
                       font=("Arial", 18, "bold"),
                       bg="white", fg="black",
                       relief=tk.SOLID, bd=1)
        cell.grid(row=i, column=j, padx=2, pady=2)

print("Grid created successfully")
root.mainloop()
