def pytest_addoption(parser):
    parser.addoption(
        "--timezone",
        action="store_true",
        dest="timezone",
        default=False,
        help="enable checking timezone data against IANA database",
    )
