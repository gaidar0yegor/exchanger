import os
import sys

def check_environment_variables():
    """Check if all required environment variables are set."""
    required_vars = [
        'BOT_TOKEN',
    ]
    
    optional_vars = [
        'ADMIN_ID',
        'ANKET_SEND',
        'SUPPORT_LINK',
        'LINK_SUBSRIBE',
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Error: The following required environment variables are not set:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or in your Railway project settings.")
        return False
    
    # Check optional vars and provide warnings
    for var in optional_vars:
        if not os.getenv(var):
            print(f"Warning: Optional environment variable {var} is not set.")
    
    return True

if __name__ == "__main__":
    # This can be run directly to check environment variables
    if check_environment_variables():
        print("All required environment variables are set.")
        sys.exit(0)
    else:
        sys.exit(1)
