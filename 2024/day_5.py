from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 5
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    rules = []
    page_updates = []

    mode = "r"
    while stuff:
        line = stuff.pop(0)
        if not line:
            mode = "p"
            continue
        if mode == "r":
            rules.append(line)
        else:
            page_updates.append(line)

    valid_updates = []

    for page in page_updates:
        page_nums = [int(p) for p in page.split(",")]
        # print(f"working on {page_nums=}")

        try:
            for rule in rules:
                before, after = (int(r) for r in rule.split("|"))
                if before not in page_nums:
                    # print(f"{before=} not in pages")
                    continue
                if after not in page_nums:
                    # print(f"{after=} not in pages")
                    continue
                if not page_nums.index(before) < page_nums.index(after):
                    # print("err")
                    raise ValueError()
                # print(f"{page_nums} passes {rule}")
        except Exception as e:
            continue

        valid_updates.append(page_nums)

    def _middle(pages):
        x = len(pages) // 2
        return int(pages[x])

    return sum(_middle(pages) for pages in valid_updates)


def _do_pages_pass(page_nums, rules):
    try:
        for rule in rules:
            before, after = (int(r) for r in rule.split("|"))
            if before not in page_nums:
                # print(f"{before=} not in pages")
                continue
            if after not in page_nums:
                # print(f"{after=} not in pages")
                continue
            if not page_nums.index(before) < page_nums.index(after):
                # print("err")
                raise ValueError()
            # print(f"{page_nums} passes {rule}")
    except Exception as e:
        return False

    return True


def _fix_pages(page_nums, rules):
    while not _do_pages_pass(page_nums, rules):
        for rule in rules:
            before, after = (int(r) for r in rule.split("|"))
            if before not in page_nums:
                continue
            if after not in page_nums:
                continue
            if not page_nums.index(before) < page_nums.index(after):
                bix = page_nums.index(before)
                aix = page_nums.index(after)
                page_nums[bix] = after
                page_nums[aix] = before

    return page_nums


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    rules = []
    page_updates = []

    mode = "r"
    while stuff:
        line = stuff.pop(0)
        if not line:
            mode = "p"
            continue
        if mode == "r":
            rules.append(line)
        else:
            page_updates.append(line)

    bad_updates = []

    for page in page_updates:
        page_nums = [int(p) for p in page.split(",")]
        if not _do_pages_pass(page_nums, rules):
            bad_updates.append(page_nums)

    fixed_updates = [_fix_pages(pages, rules) for pages in bad_updates]

    def _middle(pages):
        x = len(pages) // 2
        return int(pages[x])

    return sum(_middle(pages) for pages in fixed_updates)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)
