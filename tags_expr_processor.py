import logging
import os
import re
import sys
from glob import glob
from pathlib import Path

logging.basicConfig(level=logging.INFO)

has_no_run = False
user_ands = []
user_ors = []


def process_tags_expression(user_tag_expression):
    global has_no_run
    global user_ands
    global user_ors

    has_no_run = False
    user_ands = []
    user_ors = []

    cleanup_pattern = r"[\[\]{})]"
    copyUserArgs = re.sub(cleanup_pattern, '', user_tag_expression)

    has_no_run = copyUserArgs.__contains__(' and ~@norun') or copyUserArgs.__contains__('~@norun')
    if has_no_run:
        copyUserArgs = copyUserArgs.replace(' and ~@norun', '')
        copyUserArgs = copyUserArgs.replace('~@norun', '')

    if " and (" in copyUserArgs:
        andBracket = copyUserArgs.split(" and (")
        andAry = andBracket[0].split(" and ")
        for strItm in andAry:
            if len(strItm.strip()) > 0 and not strItm.strip().startswith("@"):
                print("Incorrect Expression in ANDs")
                sys.exit(1)
            user_ands.append(strItm.strip())

        orAry = andBracket[1].split(" or ")
        for strItm in orAry:
            if not strItm.strip().startswith("@"):
                print("Incorrect Expression in ORs")
                sys.exit(1)
            user_ors.append(strItm.strip())

    elif " or" in copyUserArgs:
        orAry = copyUserArgs.split(" or ")
        for strItm in orAry:
            if len(strItm.strip()) > 0 and not strItm.strip().startswith("@"):
                print("Incorrect Expression in ORs")
                sys.exit(1)
            user_ors.append(strItm.strip())

    else:
        if copyUserArgs is not '':
            andAry = copyUserArgs.split(" and ")
            for strItm in andAry:
                if len(strItm.strip()) > 0 and not strItm.strip().startswith("@"):
                    print("Incorrect Expression in ANDs")
                    sys.exit(1)
                user_ands.append(strItm.strip())

def filter_feature_and_scenarios(features_dir, result_dir, tags):
    Path(result_dir).mkdir(parents=True, exist_ok=True)
    for f in os.listdir(result_dir):
        os.remove(os.path.join(result_dir, f))

    process_tags_expression(tags)

    total_features = 0
    total_scenarios = 0

    if features_dir.endswith('.feature'):
        feature_files = [os.path.normpath(feature_path) for feature_path in glob(features_dir)]
    else:
        feature_files = [os.path.normpath(feature_path) for feature_path in glob(features_dir + '/*.feature')]

    for feature_file in feature_files:
        with open(feature_file, 'r') as f:
            feature_content = f.read().strip()

        filename_head = f"{result_dir}/par_{os.path.splitext(os.path.basename(feature_file))[0]}_"
        feature_blocks = feature_content.split('\n\n')

        feature_header = feature_blocks[0] + '\n\n\n'
        feature_tags = set(feature_header.split('\n')[0].strip().split())
        all_cases = [case.strip() for case in feature_blocks[1:]]
        feature_cases = [case for case in all_cases if not case.startswith('#  Scenario') or case.startswith('#  @')]
        sequence_cases = []

        sequence_cases.append(feature_header)
        found_cases = 0
        for case in feature_cases:
            case_as_list = case.split('\n')
            case_tags = set(case_as_list[0].strip().split())

            buffer_tags = case_as_list[0].strip() if case.strip().startswith('@') else ''
            buffer_case = '\n'.join(case_as_list[1:]) if case.strip().startswith('@') else case

            all_tags = feature_tags | case_tags

            if user_ands and not set(user_ands).issubset(all_tags):
                continue

            if user_ors and not (feature_tags.intersection(user_ors) or case_tags.intersection(user_ors)):
                continue

            sequence_cases.append(buffer_tags + ' @final\n')
            sequence_cases.append(buffer_case + ' \n\n')
            found_cases += 1

        if found_cases > 0:
            total_features += 1
            total_scenarios += found_cases
            with open(f"{filename_head}.feature", 'w', encoding='utf-8') as result:
                result.writelines(sequence_cases)

    logging.info(f'{total_scenarios} Scenarios found in {total_features} Features files')

    return total_scenarios


if __name__ == '__main__':
    process_tags_expression('{~@norun}')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('{@web and @browser and @sanity and ~@norun}')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('{@sanity or @regression}')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('{@web and @browser and ~@norun and (@regression or @Sanity)}')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('{@web and @browser and @checkout and ~@norun and (@regression or @Sanity)}')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('{@web}')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('{~@norun}')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('{@web and ~@norun and (@p1)}')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('@web')
    print(has_no_run, user_ands, user_ors)

    process_tags_expression('')
    print(has_no_run, user_ands, user_ors)

    # filter_feature_and_scenarios('features', 'features/final', "{@web}")
