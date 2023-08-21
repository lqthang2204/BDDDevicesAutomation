import logging
import subprocess
from importlib.metadata import version

logging.basicConfig(level=logging.INFO)


def ensure_package_versions():
    def parse_requirement_line(line):
        parts = line.strip().split("==") if "==" in line else line.strip().split(">=")
        if len(parts) == 2:
            package, expected_version = parts
            return package, expected_version
        else:
            raise ValueError(f"Invalid requirement format: {line}")

    def read_requirements():
        # Read requirements.txt file and create the required_packages dictionary
        required_packages = {}
        with open("requirements.txt") as file:
            for line in file:
                package, expected_version = parse_requirement_line(line)
                required_packages[package] = expected_version
        return required_packages

    required_packages = read_requirements()

    pkg_to_upgrade = {}
    for package, expected_version in required_packages.items():
        try:
            installed_version = version(package)
            if installed_version < expected_version:
                logging.info(f"Updating {package} from {installed_version} to {expected_version}")
                subprocess.run(["pip3", "install -U", f"{package}>={expected_version}"])
                pkg_to_upgrade[package] = expected_version
        except Exception:
            logging.info(f"Installing {package} version {expected_version}")
            subprocess.run(["pip3", "install", f"{package}>={expected_version}"])
            pkg_to_upgrade[package] = expected_version

    if pkg_to_upgrade:
        logging.info(f'Packages upgraded : {pkg_to_upgrade}')
    else:
        logging.info('All the packages are up to date')


if __name__ == "__main__":
    ensure_package_versions()
