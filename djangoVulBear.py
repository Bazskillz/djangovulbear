from coalib.bears.LocalBear import LocalBear


class DjangoVulBear(LocalBear):

    LANGUAGES = {'Python3'}
    AUTHORS = {'Securify, Team #11'}

    def run(self, filename, file):
        """
        DjangoVulBear
        Checks your django project for common misconfigurations and vulnerable implementation.

        :param None:
        """

        # This part of the code will check for misconfigurations in the settings.py file of the django project.
        debug_misconfigurations = ["debug = true\n", "debug=true\n", "template_debug = true\n", "template_debug=true\n"]
        if "settings.py" in filename:
            # Debug option in settings.py
            for line in file:
                if str.lower(line) in debug_misconfigurations:
                    yield self.new_result(message="Are you running this django project in production?"
                                                  " If so, please disable debug options > " + line, file=filename)
            # CookieStorage option in settings.py
            for line in file:
                if "cookie.CookieStorage" in line:
                    yield self.new_result(message="Local message storage is enabled, CookieStorage allows malicious"
                                                  " users to read any session data, and if your SECRET_KEY is "
                                                  "compromised they can also manipulate session data. Sessions can be "
                                                  "implemented using the session module.", file=filename)
            for line in file:
                if "MD5PasswordHasher" in line:
                    yield self.new_result(message="Are you using MD5 for as a password hashing function? Please refrain"
                                                  " from using MD5 for password storage, instead use something"
                                                  " like Argon2 or BCrypt", file=filename)

        """
        Look for missing __init__.py files in directories
        containing python files.
        """
        dirs = {os.path.split(filename)[0]
                for filename in self.file_dict.keys()
                if filename.endswith('.py')}
    
        missing_inits = {directory for directory in dirs
                         if not os.path.join(directory, '__init__.py')
                                in self.file_dict}
    
        for missing_init_dir in missing_inits:
            yield Result(self,
                         'Directory "{}" does not contain __init__.py file'
                         .format(os.path.relpath(missing_init_dir,
                                                 self.get_config_dir())))
