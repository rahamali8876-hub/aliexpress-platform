# #!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys
# from pathlib import Path

# # print("manage.py is called", os.getcwd())
# # print("manage.py __file__:", __file__)
# # print("manage.py __name__:", __name__)
# # BASE_DIR = Path(__file__).resolve()
# BASE_DIR = Path(__file__).resolve().parent[3]

# print("BASE_DIR in base.py in manage.py file ------>>>>>>:  ", BASE_DIR)

# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aliexpress_api.config.settings.base')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()


#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.base"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
