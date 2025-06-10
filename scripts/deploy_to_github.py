#!/usr/bin/env python3
"""
GitHub Pages Deployment Script

This script automatically deploys the generated HTML contact cards to GitHub Pages.
It commits all files in output/ and pushes them to the repository.

Usage:
    python3 scripts/deploy_to_github.py

Requirements:
    - Git repository already initialized
    - GitHub Pages repository configured
    - Files generated in output/ directory
"""

import os
import subprocess
import sys
from pathlib import Path


class GitHubDeployer:
    def __init__(self, base_dir=None):
        """Initialize the deployer with directory paths."""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        else:
            base_dir = Path(base_dir)
        
        self.base_dir = base_dir
        self.output_dir = base_dir / "output"
        self.html_output_dir = base_dir / "output" / "html"
        
    def check_git_status(self):
        """Check if we're in a git repository and get status."""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=self.base_dir, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            raise Exception("Not in a git repository or git not available")
    
    def check_output_files_exist(self):
        """Check if output files exist to deploy."""
        if not self.output_dir.exists():
            raise Exception(f"Output directory not found: {self.output_dir}")
        
        html_files = list(self.html_output_dir.glob("*.html")) if self.html_output_dir.exists() else []
        index_file = self.output_dir / "index.html"
        
        if not html_files and not index_file.exists():
            raise Exception("No HTML files found to deploy")
        
        return html_files, index_file.exists()
    
    def add_and_commit_files(self):
        """Add and commit all changes."""
        try:
            # Add all files in output directory
            subprocess.run(['git', 'add', 'output/'], 
                          cwd=self.base_dir, 
                          check=True)
            
            # Commit with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Update contact cards - {timestamp}"
            
            subprocess.run(['git', 'commit', '-m', commit_message], 
                          cwd=self.base_dir, 
                          check=True)
            
            return commit_message
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in str(e):
                return "No changes to commit"
            raise Exception(f"Git commit failed: {e}")
    
    def push_to_github(self):
        """Push changes to GitHub."""
        try:
            result = subprocess.run(['git', 'push'], 
                                  cwd=self.base_dir, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git push failed: {e}")
    
    def get_github_pages_url(self):
        """Try to determine the GitHub Pages URL."""
        try:
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  cwd=self.base_dir, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            remote_url = result.stdout.strip()
            
            # Extract username and repo name from git URL
            if 'github.com' in remote_url:
                if remote_url.startswith('https://'):
                    # https://github.com/username/repo.git
                    parts = remote_url.replace('https://github.com/', '').replace('.git', '').split('/')
                elif remote_url.startswith('git@'):
                    # git@github.com:username/repo.git
                    parts = remote_url.replace('git@github.com:', '').replace('.git', '').split('/')
                else:
                    return None
                
                if len(parts) >= 2:
                    username, repo = parts[0], parts[1]
                    return f"https://{username}.github.io/{repo}/"
            
            return None
        except subprocess.CalledProcessError:
            return None
    
    def deploy(self):
        """Main deployment process."""
        print("🚀 Starting GitHub Pages Deployment...")
        
        try:
            # Check if output files exist
            html_files, has_index = self.check_output_files_exist()
            total_files = len(html_files) + (1 if has_index else 0)
            print(f"📄 Found {total_files} HTML files to deploy")
            
            # Check git status
            git_status = self.check_git_status()
            if git_status:
                print("📝 Changes detected in repository")
            else:
                print("✅ No changes detected - repository is clean")
                return True
            
            # Add and commit files
            commit_message = self.add_and_commit_files()
            print(f"💾 {commit_message}")
            
            # Push to GitHub
            print("📤 Pushing to GitHub...")
            push_result = self.push_to_github()
            print("✅ Successfully pushed to GitHub")
            
            # Show GitHub Pages URLs
            pages_url = self.get_github_pages_url()
            if pages_url:
                print(f"🌐 Your contact cards website is available at:")
                print(f"   🏠 Main site: {pages_url}")
                if has_index:
                    print(f"   📋 Team index: {pages_url}output/index.html")
                
                if html_files:
                    print("📋 Individual contact card URLs:")
                    for html_file in html_files:
                        file_url = f"{pages_url}output/html/{html_file.name}"
                        print(f"   • {html_file.stem}: {file_url}")
            else:
                print("🌐 Unable to determine GitHub Pages URL automatically")
            
            print("\n🎉 Deployment completed successfully!")
            print("\n💡 Note: It may take a few minutes for changes to appear on GitHub Pages")
            return True
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False


def main():
    """Main function to run the deployer."""
    deployer = GitHubDeployer()
    success = deployer.deploy()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main() 