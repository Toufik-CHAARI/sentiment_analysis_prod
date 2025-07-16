#!/usr/bin/env python3
"""
Script pour exécuter tous les tests
"""
import subprocess
import sys
import os


def run_tests(test_type="all", coverage=False):
    """Exécuter les tests"""
    cmd = ["python", "-m", "pytest"]

    if test_type == "unit":
        cmd.extend(["tests/unit/", "-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["tests/integration/", "-m", "integration"])
    else:
        cmd.extend(["tests/"])

    if coverage:
        cmd.extend(["--cov=app", "--cov-report=html", "--cov-report=term"])

    print(f"Exécution des tests: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Fonction principale"""
    import argparse

    parser = argparse.ArgumentParser(description="Exécuter les tests")
    parser.add_argument(
        "--type",
        choices=["all", "unit", "integration"],
        default="all",
        help="Type de tests à exécuter",
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Générer un rapport de couverture"
    )

    args = parser.parse_args()

    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("tests"):
        print(
            "Erreur: Répertoire 'tests' non trouvé"
            + "\n Exécutez depuis la racine du projet."
        )
        sys.exit(1)

    # Exécuter les tests
    exit_code = run_tests(args.type, args.coverage)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
