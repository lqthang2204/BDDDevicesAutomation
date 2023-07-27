import logging
import os
import re
import sys
from glob import glob
from pathlib import Path

logging.basicConfig(level=logging.INFO)

user_ands = []
user_ors = []
no_run_list = []


def process_tags_expression(user_tag_expression):
    global user_ands
    global user_ors
    global no_run_list

    user_ands = []
    user_ors = []

    cleanup_pattern = r'[\[\]{})]'
    copyUserArgs = re.sub(cleanup_pattern, '', user_tag_expression)
    copyUserArgs = re.sub(r'\s+', ' ', copyUserArgs)

    # Extract tags containing '~@' or 'and ~@' or '~@norun'
    no_run_list = re.findall(r'(?:and )?~@(?:\w+|norun)', copyUserArgs)

    # Remove extracted tags from the expression
    for tag in no_run_list:
        copyUserArgs = copyUserArgs.replace(tag, '')

    copyUserArgs = ' '.join(copyUserArgs.split())
    # remove the unwanted and in the no_run_list
    no_run_list = [item.lstrip('and ~') for item in no_run_list]

    if 'and (' in copyUserArgs:
        andBracket = copyUserArgs.split('and (')
        andAry = andBracket[0].split('and')
        if len(andAry) == 1 and andAry[0] == '':
            pass
        else:
            for strItm in andAry:
                if len(strItm.strip()) > 0:
                    if not strItm.strip().startswith('@'):
                        print('Incorrect Expression in ANDs')
                        sys.exit(1)
                    user_ands.append(strItm.strip())

        orAry = andBracket[1].split(' or ')
        if len(orAry) == 1 and orAry[0] == '':
            pass
        else:
            for strItm in orAry:
                if not strItm.strip().startswith('@'):
                    print('Incorrect Expression in ORs')
                    sys.exit(1)
                user_ors.append(strItm.strip())

    elif ' or' in copyUserArgs:
        orAry = copyUserArgs.split(' or ')
        if len(orAry) == 1 and orAry[0] == '':
            pass
        else:
            for strItm in orAry:
                if len(strItm.strip()) > 0 and not strItm.strip().startswith('@'):
                    print('Incorrect Expression in ORs')
                    sys.exit(1)
                user_ors.append(strItm.strip())

    else:
        if copyUserArgs.strip() != '':
            andAry = copyUserArgs.split(' and ')
            if len(andAry) == 1 and andAry[0] == '':
                pass
            else:
                for strItm in andAry:
                    if len(strItm.strip()) > 0:
                        if not strItm.strip().startswith('@'):
                            print('Incorrect Expression in ANDs')
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

        filename_head = f'{result_dir}/par_{os.path.splitext(os.path.basename(feature_file))[0]}_'
        feature_blocks = feature_content.split('\n\n')

        feature_header = feature_blocks[0] + '\n\n\n'
        feature_tags = set(feature_header.split('\n')[0].strip().split())
        all_cases = [case.strip() for case in feature_blocks[1:]]
        feature_cases = [case for case in all_cases if not case.startswith('#  Scenario') or case.startswith('#  @')]

        # re-initialize the feature file buffer
        sequence_cases = []

        sequence_cases.append(feature_header)
        found_cases = 0
        for case in feature_cases:
            case_as_list = case.split('\n')
            case_tags = set(case_as_list[0].strip().split())

            buffer_tags = case_as_list[0].strip() if case.strip().startswith('@') else ''
            buffer_case = '\n'.join(case_as_list[1:]) if case.strip().startswith('@') else case

            all_tags = feature_tags | case_tags

            if no_run_list and set(no_run_list).issubset(all_tags):
                continue
            if user_ands and not set(user_ands).issubset(all_tags):
                continue
            if user_ors and not (feature_tags.intersection(user_ors) or case_tags.intersection(user_ors)):
                continue

            sequence_cases.append(buffer_tags + ' @final\n')
            sequence_cases.append(buffer_case + ' \n\n')
            found_cases += 1

        # Only when at least 1 Scenario has been identified, flush the buffer into new file
        if found_cases > 0:
            total_features += 1
            total_scenarios += found_cases
            with open(f'{filename_head}.feature', 'w', encoding='utf-8') as result:
                result.writelines(sequence_cases)

    logging.info(f'{total_scenarios} Scenarios found in {total_features} Features files')

    return total_scenarios


if __name__ == '__main__':

    test_expressions = ['{~@norun and (@test1 or @test2)}', '{@web and ~@browser and @sanity and ~@norun}', '{~@norun}',
                        '{@sanity or @regression}', '{@web and @browser and ~@norun and (@regression or @Sanity)}',
                        '{  ~@web   and   @browser   and   @checkout   and    ~@norun and (  @regression   or   @Sanity    )}',
                        '{  ~@web   and   @browser   and   @checkout   and    @norun and (  @regression   or   @Sanity    )}',
                        '{  @web   and   ~@browser   and   ~@checkout   and    @norun and (  @regression   or   @Sanity    )}',
                        '{@web}', '{~@norun}', '{@web and ~@norun and (@p1)}', '@web', '',
                        '  {  @web    and @regression    and ~@norun}']


    def verify_only_tag_process_output():
        for expression in test_expressions:
            process_tags_expression(expression)
            print(no_run_list, user_ands, user_ors)


    def verify_extracted_files():
        for expression in test_expressions:
            filter_feature_and_scenarios('features/scenarios/web', 'features/final', expression)
            print('completed.. please check')


    # verify_only_tag_process_output()
    verify_extracted_files()
