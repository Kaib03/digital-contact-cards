#!/usr/bin/env python3
import csv
import os
import re
from pathlib import Path


class ContactCardGenerator:
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        else:
            base_dir = Path(base_dir)
        
        self.base_dir = base_dir
        self.templates_dir = base_dir / "templates"
        self.output_dir = base_dir / "output"
        self.html_output_dir = self.output_dir / "html"
        self.vcf_output_dir = self.output_dir / "vcf"
        self.csv_file = base_dir / "team_data.csv"
        self.template_file = self.templates_dir / "example.html"
        
        self.html_output_dir.mkdir(parents=True, exist_ok=True)
        self.vcf_output_dir.mkdir(parents=True, exist_ok=True)
    
    def read_template(self):
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {self.template_file}")
    
    def generate_all(self):
        print("🚀 Starting Digital Contact Card Generation...")
        try:
            template = self.read_template()
            print("--- TEMPLATE CONTENT AS READ BY SCRIPT ---")
            print(template)
            print("------------------------------------------")
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            return False

def main():
    generator = ContactCardGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main() 