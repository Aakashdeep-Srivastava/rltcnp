#!/usr/bin/env python3
"""
Script to help with deployment to Vercel.
"""

import os
import sys
import subprocess
import shutil
import json

def check_vercel_cli():
    """Check if Vercel CLI is installed."""
    try:
        subprocess.run(['vercel', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def check_git():
    """Check if Git is installed."""
    try:
        subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def deploy_with_vercel_cli():
    """Deploy the application using Vercel CLI."""
    print("Deploying with Vercel CLI...")
    subprocess.run(['vercel'])

def prepare_for_github():
    """Prepare the repository for GitHub deployment."""
    if not os.path.exists('.git'):
        print("Initializing Git repository...")
        subprocess.run(['git', 'init'])
    
    print("Adding files to Git...")
    subprocess.run(['git', 'add', '.'])
    
    print("Committing changes...")
    subprocess.run(['git', 'commit', '-m', 'Prepare for Vercel deployment'])
    
    print("\nRepository is ready for GitHub!")
    print("Next steps:")
    print("1. Create a new repository on GitHub")
    print("2. Run the following commands:")
    print("   git remote add origin https://github.com/yourusername/rtl-depth-predictor.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("3. Import the repository in Vercel dashboard")

def main():
    """Main function to help with deployment."""
    print("RTL Combinational Depth Predictor - Deployment Helper")
    print("===================================================")
    
    # Check if Vercel CLI is installed
    vercel_cli_installed = check_vercel_cli()
    if vercel_cli_installed:
        print("✅ Vercel CLI is installed")
    else:
        print("❌ Vercel CLI is not installed")
        print("   Install it with: npm install -g vercel")
    
    # Check if Git is installed
    git_installed = check_git()
    if git_installed:
        print("✅ Git is installed")
    else:
        print("❌ Git is not installed")
        print("   Install it from: https://git-scm.com/downloads")
    
    print("\nDeployment Options:")
    print("1. Deploy with Vercel CLI")
    print("2. Prepare for GitHub deployment")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == '1':
        if vercel_cli_installed:
            deploy_with_vercel_cli()
        else:
            print("Vercel CLI is not installed. Please install it first.")
    elif choice == '2':
        if git_installed:
            prepare_for_github()
        else:
            print("Git is not installed. Please install it first.")
    elif choice == '3':
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main() 