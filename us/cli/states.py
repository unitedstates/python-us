import sys
import us


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Lookup state information")
    parser.add_argument("query", metavar="QUERY", nargs=1, help="name, abbreviation, or FIPS code")

    args = parser.parse_args()

    state = us.states.lookup(args.query[0])

    if not state:
        sys.stdout.write("Sorry, couldn't find a matching state.\n")

    else:
        data = state.__dict__.copy()

        region = "territory" if data.pop("is_territory") else "state"

        sys.stdout.write("\n")
        sys.stdout.write("*** The great %s of %s (%s) ***\n\n" % (region, data.pop("name"), data.pop("abbr")))

        sys.stdout.write("  FIPS code: %s\n" % data.pop("fips"))

        sys.stdout.write("\n")
        sys.stdout.write("  other attributes:\n")

        for key in sorted(data.keys()):
            val = data[key]

            if key == "counties":
                # counties is a list of County objects, not strings, so it
                # can't be joined like the other list attributes
                val = "%d counties" % len(val)
            elif isinstance(val, (list, tuple)):
                val = ", ".join(val)

            sys.stdout.write("    %s: %s\n" % (key, val))

        sys.stdout.write("\n")
        sys.stdout.write("  shapefiles:\n")
        urls = state.shapefile_urls()
        if urls is not None:
            for region, url in urls.items():
                sys.stdout.write("    %s: %s\n" % (region, url))

        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
