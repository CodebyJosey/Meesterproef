from fishingreporter import Reporter


def main():
    reporter = Reporter()
    reporter.database.restore_state()


if __name__ == "__main__":
    main()
