import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from funcs import obter_similaridade

df = pd.read_csv("events.csv", sep=";")

class CardGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eventos históricos")
        self.root.geometry("800x600")

        # Set appearance
        ctk.set_appearance_mode("dark")  # Can be "light", "dark", or "system"
        ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Historical Events", 
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=(10, 20))
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill="x", padx=20, pady=10)
        
        # Content input
        self.content_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Enter card content...",
            width=400
        )
        self.content_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.content_entry.bind("<Return>", lambda event: self.generate_card())
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            self.input_frame, 
            text="Generate Card", 
            command=self.generate_card
        )
        self.generate_btn.pack(side="left", padx=5, pady=5)
        
        # Cards frame (scrollable)
        self.cards_frame = ctk.CTkScrollableFrame(
            self.main_frame, 
            orientation="vertical"
        )
        self.cards_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
    def generate_card(self):
        for card in self.cards_frame.winfo_children():
          card.destroy()
        content = self.content_entry.get()
        
        if not content:
          messagebox.showwarning("Warning", "Please enter card content")
          return
        
        recomendacao = obter_similaridade(content, df)
        
        for _, row in recomendacao[["Year", "Date", "Event"]].iterrows():
        #for _ in range(5):
          year =  row["Year"]
          date = row["Date"]
          event = row["Event"]

          # Create card frame
          card = ctk.CTkFrame(self.cards_frame, corner_radius=10)
          card.pack(fill="x", pady=5, padx=5)

          card_title = ctk.CTkLabel(
              card, 
              text=f"{year} ({date})",  # Auto-generated title
              font=("Arial", 16, "bold"),
              anchor="w"
          )
          card_title.pack(fill="x", padx=10, pady=(10, 5))
          
          # Card content
          card_content = ctk.CTkLabel(
              card, 
              text=event,
              font=("Arial", 12),
              anchor="w",
              wraplength=700
          )
          card_content.pack(fill="x", padx=10, pady=(0, 10))
          
          # Clear input
        self.content_entry.delete(0, "end")

if __name__ == "__main__":
    root = ctk.CTk()
    app = CardGeneratorApp(root)
    root.mainloop()