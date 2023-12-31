import os
import shutil
from datetime import datetime

class CodeInjector:
    def __init__(self, user_permissions, code_verifier, logger):
        """
        Initialize the CodeInjector.

        Parameters:
            - user_permissions: An instance of a UserPermissions class to check user privileges.
            - code_verifier: An instance of a CodeVerifier class to verify the safety of injected code.
            - logger: An instance of a Logger class for logging code injection events.
        """
        self.user_permissions = user_permissions
        self.code_verifier = code_verifier
        self.logger = logger

    def inject_code(self, target_file, code_to_inject, user, backup=True):
        """
        Inject code into the specified target file.

        Parameters:
            - target_file: The path to the target file.
            - code_to_inject: The code to be injected into the file.
            - user: The user attempting to inject the code.
            - backup: Whether to create a backup before injection. Default is True.

        Returns:
            - Tuple: (success: bool, message: str)
              - success: True if code injection is successful, False otherwise.
              - message: A descriptive message indicating the result of the code injection attempt.
        """
        try:
            # Check user permissions
            if not self.user_permissions.has_permission(user, "inject_code"):
                return False, "Permission denied. User lacks the necessary privileges."

            # Verify code safety
            if not self.code_verifier.verify_code_safety(code_to_inject):
                return False, "Code verification failed. Unsafe code detected."

            # Backup the target file before injection if backup is requested
            backup_path = ""
            if backup:
                backup_path = self._create_backup(target_file)

            # Inject code into the target file as specified
            with open(target_file, "a") as file:
                file.write("\n" + code_to_inject)

            # Log the code injection event
            self.logger.log_injection_event(user, target_file, backup_path)

            return True, "Code injected successfully."

        except Exception as e:
            # Log any exceptions during the code injection process
            self.logger.log_error(f"Code injection failed: {str(e)}")
            return False, f"Code injection failed. Error: {str(e)}"

    def _create_backup(self, target_file):
        """
        Create a backup of the target file before code injection.

        Parameters:
            - target_file: The path to the target file.

        Returns:
            - str: The path to the created backup file.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            backup_path = f"{target_file}.{timestamp}.bak"
            shutil.copy2(target_file, backup_path)
            return backup_path
        except Exception as e:
            # Log any exceptions during the backup creation process
            self.logger.log_error(f"Backup creation failed: {str(e)}")
            return ""
